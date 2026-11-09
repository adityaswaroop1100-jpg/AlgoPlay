"""
quiz.py - Interactive "AlgoChallenge" Gamified Quiz for AlgoPlay.

Transforms algorithm learning into an active game with prediction challenges,
streak counters, visual confetti, and instant educational feedback.
"""

import os
import random
import subprocess
import tkinter as tk
from typing import Dict, List, Optional
from theme import FONTS, theme_manager
from widgets import FlatButton

_SOUND_ENABLED = True


def play_sound(sound_name: str) -> None:
    """Play macOS system audio in background if enabled."""
    global _SOUND_ENABLED
    if not _SOUND_ENABLED: return
    p = f"/System/Library/Sounds/{sound_name}.aiff"
    if os.path.exists(p):
        try: subprocess.Popen(["afplay", p], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception: pass


def toggle_sound() -> bool:
    global _SOUND_ENABLED
    _SOUND_ENABLED = not _SOUND_ENABLED
    return _SOUND_ENABLED


def is_sound_on() -> bool:
    return _SOUND_ENABLED


_QUESTIONS = [
    {
        "q": "Bubble Sort compares [78] and [23] (ascending). What happens?",
        "options": ["↕ Swap them (78 moves right)", "➡ Keep them (already in order)", "✂ Delete the smaller one"],
        "correct": 0,
        "why": "In Bubble Sort, if the left number is bigger than the right (78 > 23), they must swap seats so the larger number floats right!"
    },
    {
        "q": "Bubble Sort compares [14] and [45] (ascending). What happens?",
        "options": ["↕ Swap them", "➡ No swap (14 ≤ 45 is in order)", "↺ Restart from beginning"],
        "correct": 1,
        "why": "14 is already less than 45, so they are in perfect order. No swap needed, saving computer work!"
    },
    {
        "q": "Binary Search: Target is 32. Midpoint value is 65. Where do you look?",
        "options": ["⬅ Search left half (discard right)", "➡ Search right half (discard left)", "🎯 It is at the midpoint"],
        "correct": 0,
        "why": "Since the list is sorted and 32 < 65, the target MUST be in the left half! We can safely discard the entire right half!"
    },
    {
        "q": "Binary Search: Target is 89. Midpoint value is 50. Where do you look?",
        "options": ["⬅ Search left half", "➡ Search right half (discard left)", "🗑 Discard both halves"],
        "correct": 1,
        "why": "Because 89 > 50, the target can only exist in the right half. The left half is eliminated in a single step!"
    },
    {
        "q": "Which algorithm is FASTEST when an array is ALREADY sorted?",
        "options": ["Insertion Sort (O(n) time)", "Selection Sort (O(n²) time)", "Bubble Sort without checks"],
        "correct": 0,
        "why": "Insertion Sort only makes 1 comparison per element on pre-sorted data, finishing in blazing linear O(n) time!"
    },
    {
        "q": "Selection Sort finds a new minimum value [12]. What does it do?",
        "options": ["Immediately swaps with neighbor", "Remembers index 12, continues scanning", "Stops the entire sort"],
        "correct": 1,
        "why": "Selection Sort patiently scans the ENTIRE unsorted section to find the true minimum before doing a single swap!"
    },
    {
        "q": "Merge Sort receives an array of 8 numbers. What is its first step?",
        "options": ["Swap first and last number", "Split into two halves of 4 numbers", "Find the largest number"],
        "correct": 1,
        "why": "Merge Sort is Divide & Conquer! It chops the list in half recursively until pieces are size 1, then merges them in order."
    },
    {
        "q": "Quick Sort chooses a Pivot [50]. Where do numbers smaller than 50 go?",
        "options": ["Packed into the left partition", "Packed into the right partition", "Left in random positions"],
        "correct": 0,
        "why": "The pivot acts like a referee: all numbers smaller than 50 pack to the left, while larger numbers pack to the right!"
    },
    {
        "q": "Can Binary Search work on an unsorted, scrambled array?",
        "options": ["No, Binary Search REQUIRES sorted data", "Yes, it works on any random data", "Only if array size is even"],
        "correct": 0,
        "why": "Binary Search relies on sorted order to decide which half to discard. On unsorted data, only Linear Search works!"
    },
]


class QuizWindow(tk.Toplevel):
    """Gamified interactive challenge window with score, streaks, and feedback."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self.title("AlgoPlay — 🎮 Interactive Quiz Challenge")
        self.geometry("640x480"); self.minsize(580, 420)
        self.configure(bg=theme_manager.get("bg_root"))
        self.score, self.streak = 0, 0
        self.q_idx = 0; random.shuffle(_QUESTIONS)
        self._build_ui(); self._load_question()
        theme_manager.register_listener(self.apply_theme)

    def _build_ui(self) -> None:
        c = theme_manager.colors
        # Top score banner
        self.top_f = tk.Frame(self, bg=c["bg_card"], padx=14, pady=8); self.top_f.pack(fill="x")
        self.lbl_title = tk.Label(self.top_f, text="🎮 AlgoChallenge", font=FONTS["title"],
                                  bg=c["bg_card"], fg=c["accent"]); self.lbl_title.pack(side="left")
        self.lbl_streak = tk.Label(self.top_f, text="🔥 Streak: 0", font=FONTS["caption_bold"],
                                   bg=c["btn_secondary_bg"], fg=c["warning"], padx=8, pady=2)
        self.lbl_streak.pack(side="right", padx=4)
        self.lbl_score = tk.Label(self.top_f, text="Score: 0 pts", font=FONTS["caption_bold"],
                                  bg=c["btn_secondary_bg"], fg=c["success"], padx=8, pady=2)
        self.lbl_score.pack(side="right", padx=4)

        # Question card
        self.card = tk.Frame(self, bg=c["bg_card"], padx=16, pady=12, highlightthickness=1, highlightbackground=c["border"])
        self.card.pack(fill="both", expand=True, padx=14, pady=10)

        self.lbl_q_num = tk.Label(self.card, text="Question 1 of 9", font=FONTS["caption_bold"],
                                  bg=c["bg_card"], fg=c["fg_secondary"])
        self.lbl_q_num.pack(anchor="w", pady=(0, 4))
        self.lbl_question = tk.Label(self.card, text="", font=FONTS["body_bold"], bg=c["bg_card"],
                                     fg=c["fg_primary"], wraplength=560, justify="left", anchor="w")
        self.lbl_question.pack(fill="x", pady=(2, 10))

        # Options container
        self.opt_f = tk.Frame(self.card, bg=c["bg_card"]); self.opt_f.pack(fill="x", pady=4)
        self.opt_btns: List[FlatButton] = []

        # Feedback box
        self.fb_f = tk.Frame(self.card, bg=c["bg_card_inner"], padx=10, pady=8)
        self.fb_f.pack(fill="x", pady=(10, 4))
        self.lbl_fb_title = tk.Label(self.fb_f, text="", font=FONTS["body_bold"], bg=c["bg_card_inner"], fg=c["fg_primary"])
        self.lbl_fb_title.pack(anchor="w")
        self.lbl_fb_why = tk.Label(self.fb_f, text="", font=FONTS["caption"], bg=c["bg_card_inner"],
                                   fg=c["fg_secondary"], wraplength=540, justify="left", anchor="w")
        self.lbl_fb_why.pack(fill="x", pady=(2, 0))

        # Next button
        self.btn_next = FlatButton(self.card, text="Next Question ➔", font=FONTS["body_bold"],
                                   bg=c["accent"], fg=c["accent_fg"], padx=12, pady=4, command=self._next_q)
        self.btn_next.pack(side="right", pady=6)

    def _load_question(self) -> None:
        q_data = _QUESTIONS[self.q_idx % len(_QUESTIONS)]
        c = theme_manager.colors
        self.lbl_q_num.config(text=f"Challenge {self.q_idx + 1} of {len(_QUESTIONS)}")
        self.lbl_question.config(text=q_data["q"])
        self.lbl_fb_title.config(text="🤔 What do you think?", fg=c["info"])
        self.lbl_fb_why.config(text="Pick the best option above to test your algorithm intuition!")
        self.btn_next.config(state="disabled")

        for b in self.opt_btns: b.destroy()
        self.opt_btns.clear()

        for idx, opt_text in enumerate(q_data["options"]):
            btn = FlatButton(self.opt_f, text=f"  {chr(65+idx)}.  {opt_text}  ", font=FONTS["body"],
                             bg=c["btn_secondary_bg"], fg=c["btn_secondary_fg"], anchor="w",
                             padx=10, pady=6, command=lambda i=idx: self._answer(i))
            btn.pack(fill="x", pady=3); self.opt_btns.append(btn)

    def _answer(self, chosen: int) -> None:
        q_data = _QUESTIONS[self.q_idx % len(_QUESTIONS)]
        correct = q_data["correct"]
        c = theme_manager.colors

        for b in self.opt_btns: b.config(state="disabled")
        self.btn_next.config(state="normal")

        if chosen == correct:
            self.score += 10 + self.streak * 2; self.streak += 1
            play_sound("Ping")
            self.lbl_fb_title.config(text="🎉 Spot on! Correct!", fg=c["success"])
            self.opt_btns[chosen].configure(bg=c["badge_best_bg"], fg=c["badge_best_fg"])
        else:
            self.streak = 0
            play_sound("Basso")
            self.lbl_fb_title.config(text="💡 Not quite, but here is the trick:", fg=c["warning"])
            self.opt_btns[chosen].configure(bg=c["badge_worst_bg"], fg=c["badge_worst_fg"])
            self.opt_btns[correct].configure(bg=c["badge_best_bg"], fg=c["badge_best_fg"])

        self.lbl_fb_why.config(text=q_data["why"])
        self.lbl_score.config(text=f"Score: {self.score} pts")
        self.lbl_streak.config(text=f"🔥 Streak: {self.streak}" if self.streak > 0 else "Streak: 0")

    def _next_q(self) -> None:
        self.q_idx += 1
        self._load_question()

    def apply_theme(self, colors: Dict[str, str]) -> None:
        c = colors; self.configure(bg=c["bg_root"])
        self.top_f.configure(bg=c["bg_card"]); self.lbl_title.configure(bg=c["bg_card"], fg=c["accent"])
        self.lbl_score.configure(bg=c["btn_secondary_bg"], fg=c["success"])
        self.lbl_streak.configure(bg=c["btn_secondary_bg"], fg=c["warning"])
        self.card.configure(bg=c["bg_card"], highlightbackground=c["border"])
        self.lbl_q_num.configure(bg=c["bg_card"], fg=c["fg_secondary"])
        self.lbl_question.configure(bg=c["bg_card"], fg=c["fg_primary"])
        self.opt_f.configure(bg=c["bg_card"])
        self.fb_f.configure(bg=c["bg_card_inner"])
        self.lbl_fb_title.configure(bg=c["bg_card_inner"])
        self.lbl_fb_why.configure(bg=c["bg_card_inner"], fg=c["fg_secondary"])
        self.btn_next.configure(bg=c["accent"], fg=c["accent_fg"])
