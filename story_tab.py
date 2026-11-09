"""
story_tab.py - The Story Mode Main Tab for AlgoPlay.

Turns the algorithm visualizer into a narrative learning adventure with
mascots, interactive branching predictions, XP progression, streaks,
badges, and canvas-rendered speech bubbles.
"""

import random
import tkinter as tk
from typing import Any, Dict, List, Optional
from algorithm_base import AlgorithmStep
from badges import check_and_unlock
from feedback import FeedbackPanel
from game_state import GameState
from mascots import Mascot, get_mascot, get_mascot_for_algorithm
from predict_panel import PredictPanel
from searching import SEARCHING_ALGORITHMS
from sorting import SORTING_ALGORITHMS
from story import CHAPTERS, Chapter, get_chapter, get_level, get_next_level
from theme import FONTS, theme_manager
from visualizer import VisualizerCanvas
from widgets import FlatButton

def get_algo_and_mode(name: str):
    clean = (name or "").lower().replace(" ", "_")
    for k, v in SORTING_ALGORITHMS.items():
        if k.lower().replace(" ", "_") == clean: return v, "bars"
    for k, v in SEARCHING_ALGORITHMS.items():
        if k.lower().replace(" ", "_") == clean: return v, "boxes"
    return None, "bars"


class StoryTab(tk.Frame):
    """The self-contained Story Mode interface page."""

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        c = theme_manager.colors
        kwargs.setdefault("bg", c.get("bg_root", "#0B0E17"))
        super().__init__(parent, **kwargs)

        self.game_state = GameState()
        self.game_state.load()
        self.current_chapter: Optional[Chapter] = None
        self.current_level: Optional[Dict[str, Any]] = None
        self.current_mascot: Optional[Mascot] = None
        self.generator = None
        self.is_running: bool = False
        self._paused_for_predict: bool = False
        self._pending_step: Optional[AlgorithmStep] = None
        self._mascot_state: str = "idle"
        self._speech_text: str = ""
        self._step_counter: int = 0
        self.predict_mode = tk.BooleanVar(value=True)

        self._build_ui()
        init_ch = get_chapter(self.game_state.current_chapter) or CHAPTERS[0]
        self._select_chapter(init_ch.id)
        theme_manager.register_listener(self._on_theme_change)

    def _build_ui(self) -> None:
        c = theme_manager.colors
        bg_card = c.get("bg_card", "#131926")

        # ── Top Bar: Story Header & Player Stats ───────────────────
        self.top_bar = tk.Frame(self, bg=bg_card, padx=12, pady=6, highlightthickness=1, highlightbackground=c.get("border", "#1E2638"))
        self.top_bar.pack(fill=tk.X, padx=10, pady=(6, 4))

        tk.Label(self.top_bar, text="📖 Story Mode", font=FONTS["title"], bg=bg_card, fg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 10))

        self.ch_var = tk.StringVar(value="")
        ch_titles = [f"{ch.id.upper()}: {ch.title}" for ch in CHAPTERS]
        self.ch_menu = tk.OptionMenu(self.top_bar, self.ch_var, *ch_titles, command=self._on_chapter_picked)
        self.ch_menu.config(font=FONTS["caption_bold"], bg=c.get("btn_secondary_bg", "#1B2234"), fg=c.get("fg_primary", "#F8FAFC"), relief=tk.FLAT)
        self.ch_menu.pack(side=tk.LEFT, padx=4)

        self.btn_next_lvl = FlatButton(self.top_bar, text="Next Level ⏭", font=FONTS["caption_bold"], bg=c["accent"], fg="#FFF", padx=8, pady=2, command=self._advance_level)
        self.btn_next_lvl.pack(side=tk.LEFT, padx=6)

        # Gamification Stats
        self.stats_label = tk.Label(self.top_bar, text="", font=FONTS["caption_bold"], bg=c.get("bg_card_inner", "#0D111A"), fg="#F8FAFC", padx=10, pady=3)
        self.stats_label.pack(side=tk.RIGHT, padx=6)

        self.chk_predict = tk.Checkbutton(self.top_bar, text="Prediction Mode", variable=self.predict_mode, font=FONTS["caption_bold"], bg=bg_card, fg=c.get("fg_secondary", "#8B9BB4"), selectcolor=c.get("bg_card_inner", "#0D111A"), activebackground=bg_card)
        self.chk_predict.pack(side=tk.RIGHT, padx=10)

        # ── Visualizer Canvas Area ─────────────────────────────────
        self.vis_card = tk.Frame(self, bg=bg_card, highlightthickness=1, highlightbackground=c.get("border", "#1E2638"))
        self.vis_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=2)

        self.canvas = VisualizerCanvas(self.vis_card, mode="bars", bg=c.get("bg_canvas", "#0D111A"))
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # ── Prediction & Feedback Widgets ──────────────────────────
        self.feedback_panel = FeedbackPanel(self)
        self.predict_panel = PredictPanel(self, on_answer=self._on_prediction, on_hint=self._on_hint)

        # ── Bottom Control Bar ─────────────────────────────────────
        self.ctrl_bar = tk.Frame(self, bg=bg_card, padx=10, pady=6, highlightthickness=1, highlightbackground=c.get("border", "#1E2638"))
        self.ctrl_bar.pack(fill=tk.X, padx=10, pady=(2, 6))

        self.btn_start = FlatButton(self.ctrl_bar, text="▶ Start Adventure", font=FONTS["body_bold"], bg=c["accent"], fg="#FFF", padx=12, pady=4, command=self.action_start)
        self.btn_start.pack(side=tk.LEFT, padx=3)
        self.btn_step = FlatButton(self.ctrl_bar, text="⏭ Step", font=FONTS["body_bold"], bg=c.get("btn_secondary_bg", "#1B2234"), fg="#FFF", padx=10, pady=4, command=self.action_step)
        self.btn_step.pack(side=tk.LEFT, padx=3)
        self.btn_reset = FlatButton(self.ctrl_bar, text="↺ Reset", font=FONTS["body_bold"], bg=c.get("btn_secondary_bg", "#1B2234"), fg="#FFF", padx=10, pady=4, command=self.action_reset)
        self.btn_reset.pack(side=tk.LEFT, padx=3)

        self.level_desc = tk.Label(self.ctrl_bar, text="", font=FONTS["caption"], bg=bg_card, fg=c.get("fg_secondary", "#8B9BB4"))
        self.level_desc.pack(side=tk.RIGHT, padx=6)
        self._update_stats_display()

    def _select_chapter(self, ch_id: str) -> None:
        self.current_chapter = get_chapter(ch_id) or CHAPTERS[0]
        self.ch_var.set(f"{self.current_chapter.id.upper()}: {self.current_chapter.title}")
        self.current_mascot = get_mascot(self.current_chapter.mascot_key) or get_mascot_for_algorithm(self.current_chapter.algorithm)
        self.current_level = self.current_chapter.levels[0]
        self.game_state.current_chapter = self.current_chapter.id
        self.game_state.current_level = self.current_level["id"]
        self.action_reset()

    def _on_chapter_picked(self, label: str) -> None:
        ch_id = label.split(":")[0].strip().lower()
        self._select_chapter(ch_id)

    def _start_level(self) -> None:
        if not self.current_chapter or not self.current_level: return
        algo_cls, mode = get_algo_and_mode(self.current_chapter.algorithm)
        if not algo_cls: return
        self.canvas.mode = mode
        arr = list(self.current_level["array"])
        tgt = self.current_level.get("target", arr[len(arr) // 2] if arr else 0)
        self.generator = algo_cls.run(arr, target=tgt) if mode == "boxes" else algo_cls.run(arr)
        self._mascot_state = "idle"
        self._speech_text = f"{self.current_mascot.intro_line} Goal: {self.current_level['goal']}"
        self.level_desc.config(text=f"Level: {self.current_level['id']} — {self.current_level['goal']}")
        step0 = AlgorithmStep(array=list(arr), target_value=tgt if mode == "boxes" else None)
        (self.canvas.render_sorting if mode == "bars" else self.canvas.render_searching)(step0)
        self._draw_mascot_bubble()

    def action_reset(self) -> None:
        self.is_running = self._paused_for_predict = False
        self._pending_step = None; self.btn_start.config(text="▶ Start Adventure")
        self.predict_panel.hide(); self.feedback_panel.clear()
        self._start_level()

    def action_start(self) -> None:
        if self._paused_for_predict: return
        if self.is_running:
            self.is_running = False; self.btn_start.config(text="▶ Resume")
        else:
            self.is_running = True; self.btn_start.config(text="⏸ Pause")
            self._tick()

    def action_step(self) -> None:
        if self._paused_for_predict: return
        self.is_running = False; self.btn_start.config(text="▶ Resume")
        self._advance_step()

    def _advance_step(self) -> bool:
        if not self.generator: return False
        try:
            step = next(self.generator)
            self._step_counter += 1
            if self.predict_mode.get() and (getattr(step, "question", "") or (step.comparing and self._step_counter % 3 == 0)):
                self._pause_for_prediction(step); return False
            self._render_step(step); return True
        except StopIteration:
            self._on_level_complete(); return False

    def _tick(self) -> None:
        if not self.is_running: return
        if self._advance_step():
            self.after(350, self._tick)

    def _pause_for_prediction(self, step: AlgorithmStep) -> None:
        self.is_running = False; self._paused_for_predict = True
        self._pending_step = step; self._mascot_state = "thinking"
        self.btn_start.config(text="🤔 Predict Next")
        if not getattr(step, "question", ""):
            self._synthesize_prediction(step)
        self._speech_text = step.question or "Quick question! What's next?"
        self._draw_mascot_bubble()
        self.predict_panel.show(step, self.current_mascot)

    def _synthesize_prediction(self, step: AlgorithmStep) -> None:
        arr = step.array
        if step.comparing and len(step.comparing) >= 2:
            i, j = step.comparing[0], step.comparing[1]
            vi, vj = arr[i], arr[j]
            should_swap = vi > vj
            step.question = f"We are comparing {vi} (at [{i}]) and {vj} (at [{j}]). What should happen?"
            step.options = [f"Swap {vi} and {vj} because {vi} > {vj}", f"Keep order because {vi} <= {vj}", "Skip both elements"]
            step.correct_index = 0 if should_swap else 1
            step.explanation = f"Since {vi} {'>' if should_swap else '<='} {vj}, the algorithm {'must swap them' if should_swap else 'leaves them in place'}."
            step.hint = f"Compare {vi} with {vj}. Which one is larger?"

    def _on_prediction(self, correct: bool) -> None:
        self._paused_for_predict = False
        step = self._pending_step; self._pending_step = None
        if correct:
            self.game_state.correct_answer()
            self._mascot_state = "happy"
            self.feedback_panel.show_correct(self.current_mascot, step.explanation if step else "", xp=10, streak=self.game_state.streak)
            if self.game_state.streak in (5, 10, 20):
                self.feedback_panel.show_streak_milestone(self.current_mascot, self.game_state.streak)
        else:
            self.game_state.wrong_answer()
            self._mascot_state = "sad"
            self.feedback_panel.show_wrong(self.current_mascot, step.explanation if step else "", xp=2)

        new_badges = check_and_unlock(self.game_state)
        self._update_stats_display()
        if step: self._render_step(step)
        self.btn_start.config(text="▶ Continue")
        self.after(600, lambda: self._draw_mascot_bubble())

    def _on_hint(self) -> None:
        self.game_state.use_hint()
        self._update_stats_display()
        self.feedback_panel.show_hint(self.current_mascot, getattr(self._pending_step, "hint", ""), cost=5)

    def _render_step(self, step: AlgorithmStep) -> None:
        _, mode = get_algo_and_mode(self.current_chapter.algorithm)
        (self.canvas.render_sorting if mode == "bars" else self.canvas.render_searching)(step)
        if step.status: self._speech_text = step.status
        self._draw_mascot_bubble()

    def _on_level_complete(self) -> None:
        self.is_running = self._paused_for_predict = False
        self.btn_start.config(text="Level Complete! 🏆")
        self._mascot_state = "excited"
        bonus = self.current_level.get("xp_reward", 50) if self.current_level else 50
        self.game_state.complete_level(self.current_level["id"] if self.current_level else "", bonus)
        check_and_unlock(self.game_state); self._update_stats_display()
        self._speech_text = f"🎉 {self.current_mascot.win_line} Level complete! (+{bonus} XP)"
        self.canvas.render_confetti(60); self._draw_mascot_bubble()

    def _advance_level(self) -> None:
        if not self.current_chapter or not self.current_level: return
        nxt = get_next_level(self.current_chapter.id, self.current_level["id"])
        if nxt:
            nxt_ch_id, nxt_lvl_id = nxt
            if nxt_ch_id != self.current_chapter.id:
                self._select_chapter(nxt_ch_id)
            else:
                lvl = get_level(nxt_ch_id, nxt_lvl_id)
                if lvl:
                    self.current_level = lvl
                    self.game_state.current_level = nxt_lvl_id
                    self.action_reset()

    def _draw_mascot_bubble(self) -> None:
        self.canvas.delete("bubble")
        if not self.current_mascot: return
        w = self.canvas.winfo_width() or 750
        bw, bh = min(320, max(230, w // 3)), 82
        bx, by = w - bw - 14, 12
        col = self.current_mascot.color
        self.canvas.create_rectangle(bx, by, bx + bw, by + bh, fill="#0F172A", outline="#1E293B", width=1, tags="bubble")
        self.canvas.create_rectangle(bx, by, bx + bw, by + 24, fill="#1E293B", outline="", tags="bubble")
        self.canvas.create_rectangle(bx, by, bx + 3, by + bh, fill=col, outline="", tags="bubble")
        expr = self.current_mascot.get_expression(self._mascot_state)
        self.canvas.create_text(bx + 10, by + 12, text=f"{expr}  {self.current_mascot.name.upper()}", font=FONTS["caption_bold"], fill="#F8FAFC", anchor="w", tags="bubble")
        txt = self._speech_text or self.current_mascot.intro_line
        self.canvas.create_text(bx + 10, by + 32, text=txt, font=FONTS["caption"], fill="#CBD5E1", anchor="nw", width=bw - 20, tags="bubble")

    def _on_canvas_configure(self, event=None) -> None:
        self.canvas._on_resize(event); self._draw_mascot_bubble()

    def on_tab_shown(self) -> None:
        self.update_idletasks()
        if self.canvas._last_step:
            (self.canvas.render_sorting if self.canvas.mode == "bars" else self.canvas.render_searching)(self.canvas._last_step)
        else: self._start_level()
        self._draw_mascot_bubble()

    def _update_stats_display(self) -> None:
        gs = self.game_state
        self.stats_label.config(text=f"⭐ Lv.{gs.level}  |  💎 {gs.xp} XP  |  🔥 {gs.streak}  |  🏅 {len(gs.badges)} Badges")

    def _on_theme_change(self, colors: dict) -> None:
        bg_card = colors.get("bg_card", "#131926")
        self.configure(bg=colors.get("bg_root", "#0B0E17"))
        self.top_bar.config(bg=bg_card); self.vis_card.config(bg=bg_card, highlightbackground=colors.get("border", "#1E2638"))
        self.ctrl_bar.config(bg=bg_card); self.stats_label.config(bg=colors.get("bg_card_inner", "#0D111A"), fg=colors.get("fg_primary", "#F8FAFC"))
        self.chk_predict.config(bg=bg_card, selectcolor=colors.get("bg_card_inner", "#0D111A"))
        self._update_stats_display(); self._draw_mascot_bubble()
