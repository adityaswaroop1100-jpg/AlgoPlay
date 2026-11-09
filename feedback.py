"""
feedback.py - Visual feedback banner and reaction widget for AlgoPlay.

Displays mascot-voiced praise, encouragement, XP awards, streak milestones,
and hints with automatic fade-out timers and crisp theme-aligned visual indicators.
"""

import tkinter as tk
from typing import Optional
from theme import FONTS, theme_manager


class FeedbackPanel(tk.Frame):
    """Animated status banner rendering mascot feedback, XP gains, and streaks."""

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        c = theme_manager.colors
        kwargs.setdefault("bg", c.get("bg_card", "#131926"))
        kwargs.setdefault("highlightthickness", 1)
        kwargs.setdefault("highlightbackground", c.get("border", "#1E2638"))
        super().__init__(parent, **kwargs)

        self._hide_job: Optional[str] = None
        self._accent_color: str = c.get("accent", "#2563EB")
        self._build_ui()
        theme_manager.register_listener(self.on_theme_changed)

    def _build_ui(self) -> None:
        c = theme_manager.colors
        bg = c.get("bg_card", "#131926")

        # Top line: Badge + XP Delta + Streak
        self.top_row = tk.Frame(self, bg=bg)
        self.top_row.pack(fill=tk.X, padx=12, pady=(6, 2))

        self.title_label = tk.Label(
            self.top_row,
            text="",
            font=FONTS["body_bold"],
            fg="#10B981",
            bg=bg,
        )
        self.title_label.pack(side=tk.LEFT)

        self.xp_badge = tk.Label(
            self.top_row,
            text="",
            font=FONTS["caption_bold"],
            fg="#FACC15",
            bg=c.get("bg_card_inner", "#0D111A"),
            padx=8,
            pady=2,
        )
        self.xp_badge.pack(side=tk.RIGHT, padx=(4, 0))

        self.streak_badge = tk.Label(
            self.top_row,
            text="",
            font=FONTS["caption_bold"],
            fg="#F97316",
            bg=c.get("bg_card_inner", "#0D111A"),
            padx=8,
            pady=2,
        )
        self.streak_badge.pack(side=tk.RIGHT)

        # Mascot Voice Reaction Quote
        self.reaction_label = tk.Label(
            self,
            text="",
            font=FONTS["body"],
            fg=c.get("fg_primary", "#F8FAFC"),
            bg=bg,
            wraplength=640,
            justify=tk.LEFT,
            anchor="w",
        )
        self.reaction_label.pack(fill=tk.X, padx=14, pady=(2, 6))

    def _cancel_timer(self) -> None:
        if self._hide_job is not None:
            try:
                self.after_cancel(self._hide_job)
            except Exception:
                pass
            self._hide_job = None

    def _schedule_auto_hide(self, ms: int = 2500) -> None:
        self._cancel_timer()
        self._hide_job = self.after(ms, self.clear)

    def show_correct(
        self,
        mascot=None,
        explanation: str = "",
        xp: int = 10,
        streak: int = 0,
        streak_text: str = "",
    ) -> None:
        """Display cheer on correct prediction."""
        self._cancel_timer()
        c = theme_manager.colors
        border_col = mascot.color if mascot else "#10B981"
        self.config(highlightbackground=border_col)

        m_name = mascot.name if mascot else "Mascot"
        m_emoji = mascot.get_expression("happy") if mascot else "✨"
        quote = mascot.get_reaction("correct") if mascot else "Spot on! That's correct!"

        self.title_label.config(
            text=f"{m_emoji} {m_name}: Excellent!",
            fg="#10B981",
        )
        self.xp_badge.config(
            text=f"+{xp} XP",
            fg="#10B981",
            bg=c.get("bg_card_inner", "#0D111A"),
        )
        self.xp_badge.pack(side=tk.RIGHT, padx=(4, 0))

        if streak >= 2:
            s_text = streak_text or f"🔥 {streak} Streak"
            self.streak_badge.config(
                text=s_text,
                fg="#F97316",
                bg=c.get("bg_card_inner", "#0D111A"),
            )
            self.streak_badge.pack(side=tk.RIGHT)
        else:
            self.streak_badge.pack_forget()

        full_quote = f'"{quote}"'
        if explanation:
            full_quote += f" — {explanation}"
        self.reaction_label.config(text=full_quote)

        self.pack(fill=tk.X, padx=12, pady=(4, 6))
        self._schedule_auto_hide(3000)

    def show_wrong(
        self,
        mascot=None,
        explanation: str = "",
        xp: int = 2,
    ) -> None:
        """Display encouraging reaction on wrong prediction."""
        self._cancel_timer()
        c = theme_manager.colors
        self.config(highlightbackground="#EF4444")

        m_name = mascot.name if mascot else "Mascot"
        m_emoji = mascot.get_expression("sad") if mascot else "💭"
        quote = mascot.get_reaction("wrong") if mascot else "Not quite, but good effort!"

        self.title_label.config(
            text=f"{m_emoji} {m_name}: Keep Going!",
            fg="#EF4444",
        )
        self.xp_badge.config(
            text=f"+{xp} XP (try)",
            fg=c.get("fg_secondary", "#8B9BB4"),
            bg=c.get("bg_card_inner", "#0D111A"),
        )
        self.xp_badge.pack(side=tk.RIGHT, padx=(4, 0))
        self.streak_badge.pack_forget()

        full_quote = f'"{quote}"'
        if explanation:
            full_quote += f" — {explanation}"
        self.reaction_label.config(text=full_quote)

        self.pack(fill=tk.X, padx=12, pady=(4, 6))
        self._schedule_auto_hide(3200)

    def show_hint(self, mascot=None, text: str = "", cost: int = 5) -> None:
        """Display hint announcement and XP deduction."""
        self._cancel_timer()
        c = theme_manager.colors
        self.config(highlightbackground="#F59E0B")

        m_name = mascot.name if mascot else "Advisor"
        m_emoji = mascot.get_expression("thinking") if mascot else "💡"

        self.title_label.config(
            text=f"{m_emoji} {m_name}: Clue Revealed",
            fg="#F59E0B",
        )
        self.xp_badge.config(
            text=f"-{cost} XP",
            fg="#F59E0B",
            bg=c.get("bg_card_inner", "#0D111A"),
        )
        self.xp_badge.pack(side=tk.RIGHT, padx=(4, 0))
        self.streak_badge.pack_forget()

        prefix = f"{mascot.hint_style} " if mascot else "💡 "
        self.reaction_label.config(text=f'{prefix}"{text}"')

        self.pack(fill=tk.X, padx=12, pady=(4, 6))
        self._schedule_auto_hide(3000)

    def show_streak_milestone(self, mascot=None, streak: int = 5, bonus_xp: int = 25) -> None:
        """Celebrate streak milestone (5, 10, 20)."""
        self._cancel_timer()
        c = theme_manager.colors
        self.config(highlightbackground="#F59E0B")

        m_name = mascot.name if mascot else "Mascot"
        m_emoji = mascot.get_expression("excited") if mascot else "🔥"
        streak_line = (
            mascot.reaction_streak.get(streak, f"{streak} in a row! Unstoppable!")
            if mascot
            else f"{streak} streak!"
        )

        self.title_label.config(
            text=f"{m_emoji} {m_name}: 🔥 STREAK x{streak}!",
            fg="#F59E0B",
        )
        self.xp_badge.config(
            text=f"+{bonus_xp} BONUS XP",
            fg="#F59E0B",
            bg=c.get("bg_card_inner", "#0D111A"),
        )
        self.xp_badge.pack(side=tk.RIGHT, padx=(4, 0))
        self.streak_badge.pack_forget()

        self.reaction_label.config(text=f'"{streak_line}"')
        self.pack(fill=tk.X, padx=12, pady=(4, 6))
        self._schedule_auto_hide(3500)

    def clear(self) -> None:
        """Fade out and pack_forget feedback panel."""
        self._cancel_timer()
        self.pack_forget()

    def on_theme_changed(self, colors: dict) -> None:
        """Update colors on theme switch."""
        bg = colors.get("bg_card", "#131926")
        inner_bg = colors.get("bg_card_inner", "#0D111A")
        self.config(bg=bg, highlightbackground=colors.get("border", "#1E2638"))
        self.top_row.config(bg=bg)
        self.reaction_label.config(bg=bg, fg=colors.get("fg_primary", "#F8FAFC"))
        self.title_label.config(bg=bg)
        self.xp_badge.config(bg=inner_bg)
        self.streak_badge.config(bg=inner_bg)
