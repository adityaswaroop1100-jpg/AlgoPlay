"""
hint_engine.py - Predict-Next-Step Interactive Quiz Engine for AlgoPlay.

Pops up a lightweight inline challenge after every N steps asking the learner
to predict what the algorithm will do next. Correct answers earn XP and
trigger a celebration; wrong answers show a friendly explanation.
Zero external dependencies — pure Python 3 standard library and Tkinter.
"""

import tkinter as tk
from typing import Callable, Dict, List, Optional, Tuple
from algorithm_base import AlgorithmStep
from theme import FONTS, theme_manager


# ── Prediction generators per algorithm ──────────────────────────────────────

def _predict_sort(algo: str, step: AlgorithmStep, nxt: Optional[AlgorithmStep]) -> Optional[Dict]:
    """Return a quiz dict {question, options, correct, explanation} or None."""
    if nxt is None:
        return None
    arr = step.array
    if not arr or not step.comparing or len(step.comparing) < 2:
        return None
    i1, i2 = step.comparing[0], step.comparing[1]
    if i1 >= len(arr) or i2 >= len(arr):
        return None
    v1, v2 = arr[i1], arr[i2]
    will_swap = bool(nxt.swapping)
    opts = ["🔄 Swap them", "✅ Leave as-is", "⏭ Move to next pair", "✔ Mark as sorted"]
    if will_swap:
        correct = 0
        explanation = (f"Because arr[{i1}]={v1} > arr[{i2}]={v2}, "
                       "the larger value needs to bubble right — a swap is performed!")
    else:
        correct = 1
        explanation = (f"Because arr[{i1}]={v1} ≤ arr[{i2}]={v2}, "
                       "they are already in order — no swap needed.")
    return {
        "question": f"arr[{i1}]={v1}  vs  arr[{i2}]={v2}  — What happens next?",
        "options": opts, "correct": correct, "explanation": explanation,
    }


def _predict_search(algo: str, step: AlgorithmStep, nxt: Optional[AlgorithmStep]) -> Optional[Dict]:
    """Return a quiz dict for a searching step or None."""
    if nxt is None or not step.comparing:
        return None
    arr = step.array
    if not arr:
        return None
    idx = step.comparing[0]
    if idx >= len(arr):
        return None
    val = arr[idx]
    tgt = step.target_value
    if tgt is None:
        return None
    if "Binary" in algo:
        if val == tgt:
            correct = 0
            opts = ["🎯 Target found!", "⬅ Search left half", "➡ Search right half", "❌ Not present"]
            explanation = f"arr[mid]={val} matches target={tgt} → target is found!"
        elif val < tgt:
            correct = 2
            opts = ["🎯 Target found!", "⬅ Search left half", "➡ Search right half", "❌ Not present"]
            explanation = f"arr[mid]={val} < target={tgt} → discard left, search right half."
        else:
            correct = 1
            opts = ["🎯 Target found!", "⬅ Search left half", "➡ Search right half", "❌ Not present"]
            explanation = f"arr[mid]={val} > target={tgt} → discard right, search left half."
        return {"question": f"mid value = {val},  target = {tgt}  — What happens?",
                "options": opts, "correct": correct, "explanation": explanation}
    return None


def build_quiz(algo: str, step: AlgorithmStep, nxt: Optional[AlgorithmStep]) -> Optional[Dict]:
    """Return a prediction quiz dict or None if no suitable quiz for this step."""
    if any(k in algo for k in ("Bubble", "Insertion", "Selection", "Merge", "Quick")):
        return _predict_sort(algo, step, nxt)
    if any(k in algo for k in ("Linear", "Binary")):
        return _predict_search(algo, step, nxt)
    return None


# ── XP & Streak tracker ───────────────────────────────────────────────────────

class QuizScore:
    """Lightweight session XP tracker."""
    def __init__(self) -> None:
        self.xp = 0; self.streak = 0; self.total = 0; self.correct = 0

    def record(self, right: bool) -> int:
        """Record answer, return XP gained."""
        self.total += 1
        if right:
            self.correct += 1; self.streak += 1
            gain = 10 + (5 * min(self.streak, 5))   # streak bonus up to +25
            self.xp += gain; return gain
        else:
            self.streak = 0; return 0

    @property
    def accuracy(self) -> str:
        if not self.total: return "—"
        return f"{round(100 * self.correct / self.total)}%"


# ── Inline quiz popup widget ──────────────────────────────────────────────────

class PredictPopup(tk.Toplevel):
    """Slide-in Predict-Next-Step challenge overlay."""

    def __init__(self, parent: tk.Widget, quiz: Dict, score: QuizScore,
                 on_done: Callable[[bool], None]) -> None:
        super().__init__(parent)
        self.quiz = quiz; self.score = score; self.on_done = on_done
        self._answered = False
        c = theme_manager.colors
        self.overrideredirect(True)
        self.configure(bg=c["bg_card"])
        self.attributes("-topmost", True)
        self._place_near(parent)
        self._build(c)

    def _place_near(self, parent: tk.Widget) -> None:
        parent.update_idletasks()
        px = parent.winfo_rootx(); py = parent.winfo_rooty()
        pw = parent.winfo_width()
        self.geometry(f"420x280+{px + pw//2 - 210}+{py + 60}")

    def _build(self, c: Dict[str, str]) -> None:
        # Border frame
        bdr = tk.Frame(self, bg=c["accent"], padx=2, pady=2); bdr.pack(fill="both", expand=True)
        inner = tk.Frame(bdr, bg=c["bg_card"], padx=16, pady=12); inner.pack(fill="both", expand=True)

        tk.Label(inner, text="🤔  Predict Next Step", font=FONTS["subtitle"],
                 bg=c["bg_card"], fg=c["accent"]).pack(anchor="w")
        self.lbl_q = tk.Label(inner, text=self.quiz["question"], font=FONTS["body_bold"],
                               bg=c["bg_card"], fg=c["fg_primary"], wraplength=380, justify="left")
        self.lbl_q.pack(anchor="w", pady=(6, 10))

        self.opt_btns: List[tk.Button] = []
        for i, opt in enumerate(self.quiz["options"]):
            btn = tk.Label(inner, text=f"  {opt}", font=FONTS["body"], bg=c["bg_card_inner"],
                           fg=c["fg_primary"], anchor="w", padx=8, pady=4,
                           highlightthickness=1, highlightbackground=c["border"], cursor="hand2")
            btn.pack(fill="x", pady=2)
            btn.bind("<Button-1>", lambda e, idx=i: self._answer(idx))
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=c["accent"], fg="#FFFFFF"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=c["bg_card_inner"], fg=c["fg_primary"])
                     if not self._answered else None)
            self.opt_btns.append(btn)

        self.lbl_feedback = tk.Label(inner, text="", font=FONTS["caption"],
                                      bg=c["bg_card"], fg=c["fg_secondary"], wraplength=380, justify="left")
        self.lbl_feedback.pack(anchor="w", pady=(6, 0))

        # XP / streak strip
        self.lbl_xp = tk.Label(inner, text=f"⚡ {self.score.xp} XP  •  🔥 {self.score.streak}× streak",
                                font=FONTS["caption_bold"], bg=c["bg_card"], fg=c["warning"])
        self.lbl_xp.pack(side="bottom", anchor="w")

    def _answer(self, chosen: int) -> None:
        if self._answered: return
        self._answered = True
        c = theme_manager.colors
        correct = self.quiz["correct"]
        right = (chosen == correct)
        gained = self.score.record(right)
        for i, btn in enumerate(self.opt_btns):
            if i == correct:
                btn.configure(bg="#059669", fg="#FFFFFF", highlightbackground="#059669")
            elif i == chosen and not right:
                btn.configure(bg="#DC2626", fg="#FFFFFF", highlightbackground="#DC2626")
            else:
                btn.configure(fg=c["fg_dim"])
        msg = (f"✅ Correct! +{gained} XP  —  {self.quiz['explanation']}" if right
               else f"❌ Not quite.  —  {self.quiz['explanation']}")
        self.lbl_feedback.configure(text=msg, fg="#059669" if right else "#DC2626")
        self.lbl_xp.configure(text=f"⚡ {self.score.xp} XP  •  🔥 {self.score.streak}× streak")
        self.after(2800, self._close)

    def _close(self) -> None:
        self.on_done(self._answered)
        self.destroy()


# ── Trigger manager ───────────────────────────────────────────────────────────

class HintEngine:
    """
    Sits between the main animation loop and the popup.
    Call maybe_quiz() after each step; it fires PredictPopup every N steps.
    """
    INTERVAL = 8   # show quiz every 8 steps

    def __init__(self, parent: tk.Widget) -> None:
        self.parent = parent
        self.score = QuizScore()
        self._counter = 0
        self._active_popup: Optional[PredictPopup] = None
        self._paused = False   # True while popup is open (caller must respect)
        self.on_pause_change: Optional[Callable[[bool], None]] = None

    def maybe_quiz(self, algo: str, step: AlgorithmStep, nxt: Optional[AlgorithmStep]) -> None:
        """Call after rendering each step. Opens a popup every INTERVAL steps."""
        if self._active_popup or self._paused:
            return
        self._counter += 1
        if self._counter % self.INTERVAL != 0:
            return
        quiz = build_quiz(algo, step, nxt)
        if quiz is None:
            return
        self._paused = True
        if self.on_pause_change:
            self.on_pause_change(True)
        self._active_popup = PredictPopup(self.parent, quiz, self.score, self._on_popup_done)

    def _on_popup_done(self, answered: bool) -> None:
        self._active_popup = None
        self._paused = False
        if self.on_pause_change:
            self.on_pause_change(False)

    def reset(self) -> None:
        self._counter = 0
        if self._active_popup:
            try: self._active_popup.destroy()
            except Exception: pass
        self._active_popup = None
        self._paused = False

    @property
    def xp_label(self) -> str:
        return f"⚡ {self.score.xp} XP  •  🔥 {self.score.streak}×  •  {self.score.accuracy} acc"
