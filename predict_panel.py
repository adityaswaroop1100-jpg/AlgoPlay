"""
predict_panel.py - "What happens next?" interactive prediction widget for AlgoPlay.

Presents students with algorithmic branching decisions during visualizer steps,
reinforcing active recall with mascot-themed styling, instant visual feedback,
hints, and conceptual explanations.
"""

import tkinter as tk
from typing import Callable, List, Optional
from theme import FONTS, theme_manager
from widgets import FlatButton


class PredictPanel(tk.Frame):
    """Interactive prediction challenge widget styled with mascot accents."""

    def __init__(
        self,
        parent: tk.Widget,
        on_answer: Callable[[bool], None],
        on_hint: Optional[Callable[[], None]] = None,
        **kwargs,
    ) -> None:
        c = theme_manager.colors
        kwargs.setdefault("bg", c.get("bg_card", "#131926"))
        kwargs.setdefault("highlightthickness", 1)
        kwargs.setdefault("highlightbackground", c.get("border", "#1E2638"))
        super().__init__(parent, **kwargs)

        self.on_answer = on_answer
        self.on_hint = on_hint
        self._step = None
        self._mascot = None
        self._correct_index: int = -1
        self._explanation: str = ""
        self._hint_text: str = ""
        self._answered: bool = False
        self._accent_color: str = c.get("accent", "#2563EB")

        self._build_ui()
        theme_manager.register_listener(self.on_theme_changed)

    def _build_ui(self) -> None:
        c = theme_manager.colors
        bg = c.get("bg_card", "#131926")

        # Top Header Bar
        self.header_frame = tk.Frame(self, bg=bg)
        self.header_frame.pack(fill=tk.X, padx=12, pady=(10, 4))

        self.mascot_badge = tk.Label(
            self.header_frame,
            text="🤔 PREDICT NEXT STEP",
            font=FONTS["caption_bold"],
            fg=self._accent_color,
            bg=c.get("bg_card_inner", "#0D111A"),
            padx=8,
            pady=3,
        )
        self.mascot_badge.pack(side=tk.LEFT)

        self.hint_btn = FlatButton(
            self.header_frame,
            text="💡 Hint (-5 XP)",
            font=FONTS["caption_bold"],
            bg=c.get("btn_secondary_bg", "#1B2234"),
            fg="#F59E0B",
            padx=8,
            pady=2,
            command=self._on_hint_clicked,
        )
        self.hint_btn.pack(side=tk.RIGHT)

        # Question Prompt
        self.question_label = tk.Label(
            self,
            text="What will the algorithm do in the next step?",
            font=FONTS["body_bold"],
            fg=c.get("fg_primary", "#F8FAFC"),
            bg=bg,
            wraplength=640,
            justify=tk.LEFT,
            anchor="w",
        )
        self.question_label.pack(fill=tk.X, padx=14, pady=(4, 6))

        # Hint Reveal Label (collapsible)
        self.hint_label = tk.Label(
            self,
            text="",
            font=FONTS["caption"],
            fg="#F59E0B",
            bg=bg,
            wraplength=640,
            justify=tk.LEFT,
            anchor="w",
        )

        # Options Container
        self.options_frame = tk.Frame(self, bg=bg)
        self.options_frame.pack(fill=tk.X, padx=12, pady=(2, 8))

        self.option_buttons: List[FlatButton] = []
        for i in range(3):
            btn = FlatButton(
                self.options_frame,
                text=f"Option {i + 1}",
                font=FONTS["body_bold"],
                bg="#151D2E",
                fg="#F8FAFC",
                hover_bg="#1E293B",
                anchor="w",
                padx=16,
                pady=9,
                command=lambda idx=i: self._pick(idx),
            )
            btn.pack(fill=tk.X, pady=3)
            self.option_buttons.append(btn)

        # Explanation / Result Banner
        self.explanation_label = tk.Label(
            self,
            text="",
            font=FONTS["caption_bold"],
            fg=c.get("fg_secondary", "#8B9BB4"),
            bg=c.get("bg_card_inner", "#0D111A"),
            wraplength=640,
            justify=tk.LEFT,
            anchor="w",
            padx=10,
            pady=6,
        )

    def show(self, step, mascot=None) -> None:
        """Populate and display prediction question and options."""
        self._step = step
        self._mascot = mascot
        self._answered = False
        self._correct_index = getattr(step, "correct_index", -1)
        self._explanation = getattr(step, "explanation", "")
        self._hint_text = getattr(step, "hint", "")

        c = theme_manager.colors
        bg = c.get("bg_card", "#131926")
        btn_bg = c.get("bg_card_inner", "#0D111A")
        fg = c.get("fg_primary", "#F8FAFC")

        # Mascot themed colors
        if mascot and hasattr(mascot, "color"):
            self._accent_color = mascot.color
            badge_title = f"{mascot.emoji} {mascot.name.upper()} ASKS:"
        else:
            self._accent_color = c.get("accent", "#2563EB")
            badge_title = "🤔 PREDICTION CHALLENGE"

        self.mascot_badge.config(
            text=badge_title,
            fg=self._accent_color,
            bg=c.get("bg_card_inner", "#0D111A"),
        )
        self.config(highlightbackground=self._accent_color)

        # Reset Question
        q_text = getattr(step, "question", "") or "What happens next?"
        self.question_label.config(text=q_text, fg=fg)

        # Reset Hint
        self.hint_label.pack_forget()
        self.hint_label.config(text="")
        if self._hint_text:
            self.hint_btn.pack(side=tk.RIGHT)
            self.hint_btn.config(state=tk.NORMAL, text="💡 Hint (-5 XP)")
        else:
            self.hint_btn.pack_forget()

        # Reset Options
        opts = getattr(step, "options", [])
        for i, btn in enumerate(self.option_buttons):
            if i < len(opts):
                prefix = ["A)", "B)", "C)"][i]
                btn.config(
                    text=f"{prefix}  {opts[i]}",
                    bg="#151D2E",
                    fg="#F8FAFC",
                    state="normal",
                )
                btn.pack(fill=tk.X, pady=3)
            else:
                btn.pack_forget()

        # Reset Explanation
        self.explanation_label.pack_forget()
        self.explanation_label.config(text="")
        self.pack(fill=tk.X, padx=12, pady=(4, 8))

    def _on_hint_clicked(self) -> None:
        """Reveal hint and invoke penalty callback."""
        if not self._hint_text:
            return
        prefix = f"{self._mascot.hint_style} " if self._mascot else "💡 Hint: "
        self.hint_label.config(text=f"{prefix}{self._hint_text}")
        self.hint_label.pack(fill=tk.X, padx=14, pady=(0, 4), after=self.question_label)
        self.hint_btn.config(state="disabled", text="💡 Hint Revealed")
        if self.on_hint:
            self.on_hint()

    def _pick(self, idx: int) -> None:
        """Handle user choice, animate highlight, reveal explanation, notify parent."""
        if self._answered:
            return
        self._answered = True

        # Disable further clicks
        for btn in self.option_buttons:
            btn.config(state="disabled")

        is_correct = (idx == self._correct_index)

        # Color highlight choices
        for i, btn in enumerate(self.option_buttons):
            if i == self._correct_index:
                btn.config(bg="#059669", fg="#FFFFFF")  # Crisp Emerald green
            elif i == idx and not is_correct:
                btn.config(bg="#DC2626", fg="#FFFFFF")  # Crisp Crimson red
            else:
                btn.config(bg="#0B0F19", fg="#475569")

        # Show explanation
        self.show_explanation(self._explanation, is_correct)

        # Notify callback
        if self.on_answer:
            self.on_answer(is_correct)

    def show_explanation(self, text: str, is_correct: Optional[bool] = None) -> None:
        """Display conceptual rationale beneath options."""
        if not text:
            return
        c = theme_manager.colors
        if is_correct is True:
            prefix = "✨ CORRECT: "
            fg_color = "#34D399"
        elif is_correct is False:
            prefix = "💡 NOT QUITE: "
            fg_color = "#F87171"
        else:
            prefix = "ℹ️ "
            fg_color = c.get("fg_secondary", "#8B9BB4")

        self.explanation_label.config(
            text=f"{prefix}{text}",
            fg=fg_color,
            bg=c.get("bg_card_inner", "#0D111A"),
        )
        self.explanation_label.pack(fill=tk.X, padx=12, pady=(2, 6))

    def hide(self) -> None:
        """Hide panel from view."""
        self.pack_forget()

    def on_theme_changed(self, colors: dict) -> None:
        """React smoothly to runtime light/dark palette transitions."""
        bg = colors.get("bg_card", "#131926")
        inner_bg = colors.get("bg_card_inner", "#0D111A")
        border = self._accent_color if self._mascot else colors.get("border", "#1E2638")

        self.config(bg=bg, highlightbackground=border)
        self.header_frame.config(bg=bg)
        self.options_frame.config(bg=bg)
        self.question_label.config(bg=bg, fg=colors.get("fg_primary", "#F8FAFC"))
        self.hint_label.config(bg=bg)
        self.mascot_badge.config(bg=inner_bg)
        self.hint_btn.config(
            bg=colors.get("btn_secondary_bg", "#1B2234"),
            fg=colors.get("warning", "#F59E0B"),
        )
        if not self._answered:
            for btn in self.option_buttons:
                btn.config(
                    bg=colors.get("btn_secondary_bg", "#151D2E"),
                    fg=colors.get("fg_primary", "#F8FAFC"),
                )
