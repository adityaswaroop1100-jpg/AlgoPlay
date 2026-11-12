"""
concept_briefing.py - Pre-Flight Concept & Complexity Briefing Modal for AlgoPlay.

Displays an educational briefing card/modal detailing the algorithm's core
concept, step-by-step strategy, real-world analogy, and comprehensive Time &
Space Complexity breakdown before the user begins the visual representation.
Zero external dependencies — pure Python 3 standard library and Tkinter.
"""

import tkinter as tk
from typing import Callable, Dict, Optional
from theme import FONTS, theme_manager
from widgets import FlatButton
from concept_data import ALGO_CONCEPTS


class ConceptBriefingModal(tk.Toplevel):
    """Pre-flight modal detailing concept, working strategy, and Big-O breakdown."""

    def __init__(self, parent: tk.Widget, algo_name: str, on_start: Optional[Callable[[], None]] = None,
                 on_step: Optional[Callable[[], None]] = None, auto_pref_var: Optional[tk.BooleanVar] = None) -> None:
        super().__init__(parent)
        self.algo_name = algo_name
        self.on_start = on_start
        self.on_step = on_step
        self.auto_pref_var = auto_pref_var
        self.info = ALGO_CONCEPTS.get(algo_name, ALGO_CONCEPTS["Bubble Sort"])

        c = theme_manager.colors
        self.title(f"AlgoPlay — 💡 Concept Briefing: {algo_name}")
        self.geometry("640x560")
        self.minsize(580, 500)
        self.configure(bg=c["bg_root"])
        self.transient(parent.winfo_toplevel())
        self.grab_set()

        self._center_window(parent)
        self._build_ui(c)

    def _center_window(self, parent: tk.Widget) -> None:
        self.update_idletasks()
        try:
            pw, ph = parent.winfo_width(), parent.winfo_height()
            px, py = parent.winfo_rootx(), parent.winfo_rooty()
            w, h = 640, 560
            x = max(20, px + (pw - w) // 2)
            y = max(20, py + (ph - h) // 2)
            self.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            pass

    def _build_ui(self, c: Dict[str, str]) -> None:
        # Header banner
        hdr = tk.Frame(self, bg=c["bg_card"], padx=18, pady=12, highlightthickness=1, highlightbackground=c["border"])
        hdr.pack(fill="x")
        top_row = tk.Frame(hdr, bg=c["bg_card"]); top_row.pack(fill="x")
        tk.Label(top_row, text=f"{self.info['icon']}  {self.algo_name}", font=FONTS["title"],
                 bg=c["bg_card"], fg=c["fg_primary"]).pack(side="left")
        tk.Label(top_row, text=f" {self.info['tag']} ", font=FONTS["caption_bold"],
                 bg=c["bg_card_inner"], fg=c["accent"], highlightthickness=1,
                 highlightbackground=c["border"]).pack(side="right")
        tk.Label(hdr, text="Pre-flight algorithm briefing • Understand the concept and complexity before running",
                 font=FONTS["caption"], bg=c["bg_card"], fg=c["fg_secondary"]).pack(anchor="w", pady=(4, 0))

        # Main body
        body = tk.Frame(self, bg=c["bg_root"], padx=16, pady=10); body.pack(fill="both", expand=True)

        # 1. Concept & Analogy Card
        c_card = tk.Frame(body, bg=c["bg_card"], padx=14, pady=10, highlightthickness=1, highlightbackground=c["border"])
        c_card.pack(fill="x", pady=(0, 8))
        tk.Label(c_card, text="💡  Core Concept", font=FONTS["subtitle"], bg=c["bg_card"], fg=c["fg_primary"]).pack(anchor="w")
        tk.Label(c_card, text=self.info["concept"], font=FONTS["body"], bg=c["bg_card"],
                 fg=c["fg_primary"], wraplength=580, justify="left").pack(anchor="w", pady=(3, 6))

        ana_box = tk.Frame(c_card, bg=c["bg_card_inner"], padx=10, pady=6, highlightthickness=1, highlightbackground=c["border"])
        ana_box.pack(fill="x")
        tk.Label(ana_box, text=f"💭 Real-World Analogy:  {self.info['analogy']}", font=FONTS["caption"],
                 bg=c["bg_card_inner"], fg=c["fg_secondary"], wraplength=560, justify="left").pack(anchor="w")

        # 2. Time & Space Complexity Pills
        comp_card = tk.Frame(body, bg=c["bg_card"], padx=14, pady=10, highlightthickness=1, highlightbackground=c["border"])
        comp_card.pack(fill="x", pady=(0, 8))
        tk.Label(comp_card, text="⏱  Time & Space Complexity Breakdown", font=FONTS["subtitle"],
                 bg=c["bg_card"], fg=c["fg_primary"]).pack(anchor="w", pady=(0, 6))

        grid = tk.Frame(comp_card, bg=c["bg_card"]); grid.pack(fill="x")
        c_data = self.info["complexity"]
        items = [
            ("Best Time", c_data["best"][0], c_data["best"][1], c.get("badge_best_bg", "#062A1F"), c.get("badge_best_fg", "#34D399"), c.get("badge_best_border", "#065F46")),
            ("Average", c_data["avg"][0], c_data["avg"][1], c.get("badge_avg_bg", "#08273F"), c.get("badge_avg_fg", "#38BDF8"), c.get("badge_avg_border", "#0369A1")),
            ("Worst Time", c_data["worst"][0], c_data["worst"][1], c.get("badge_worst_bg", "#2E0E14"), c.get("badge_worst_fg", "#F87171"), c.get("badge_worst_border", "#991B1B")),
            ("Space", c_data["space"][0], c_data["space"][1], c.get("badge_space_bg", "#281A05"), c.get("badge_space_fg", "#FBBF24"), c.get("badge_space_border", "#92400E")),
        ]
        for col_idx, (title, val, desc, bg_b, fg_b, bdr_b) in enumerate(items):
            box = tk.Frame(grid, bg=c["bg_card_inner"], padx=8, pady=6, highlightthickness=1, highlightbackground=c["border"])
            box.pack(side="left", fill="both", expand=True, padx=2)
            tk.Label(box, text=title, font=FONTS["small_bold"], bg=c["bg_card_inner"], fg=c["fg_secondary"]).pack(anchor="w")
            tk.Label(box, text=f" {val} ", font=FONTS["body_bold"], bg=bg_b, fg=fg_b,
                     highlightthickness=1, highlightbackground=bdr_b).pack(anchor="w", pady=3)
            tk.Label(box, text=desc, font=FONTS["small"], bg=c["bg_card_inner"], fg=c["fg_dim"],
                     wraplength=125, justify="left").pack(anchor="w")

        # 3. Strategy & Key Invariant
        strat_card = tk.Frame(body, bg=c["bg_card"], padx=14, pady=10, highlightthickness=1, highlightbackground=c["border"])
        strat_card.pack(fill="x")
        tk.Label(strat_card, text="🎯  Algorithm Strategy & Key Invariant", font=FONTS["subtitle"],
                 bg=c["bg_card"], fg=c["fg_primary"]).pack(anchor="w")
        for st_text in self.info["steps"]:
            tk.Label(strat_card, text=st_text, font=FONTS["caption"], bg=c["bg_card"],
                     fg=c["fg_primary"], wraplength=570, justify="left").pack(anchor="w", pady=1)
        tk.Label(strat_card, text=f"🔍 Invariant to watch:  {self.info['invariant']}",
                 font=FONTS["caption_bold"], bg=c["bg_card"], fg=c["accent"], wraplength=570, justify="left").pack(anchor="w", pady=(4, 0))

        # Bottom Bar: preference checkbox + action buttons
        btm = tk.Frame(self, bg=c["bg_card"], padx=18, pady=10, highlightthickness=1, highlightbackground=c["border"])
        btm.pack(fill="x", side="bottom")

        if self.auto_pref_var is not None:
            chk = tk.Checkbutton(btm, text="Always show briefing before start", variable=self.auto_pref_var,
                                 font=FONTS["caption"], bg=c["bg_card"], fg=c["fg_secondary"],
                                 activebackground=c["bg_card"], selectcolor=c["bg_card_inner"])
            chk.pack(side="left")

        FlatButton(btm, text="✕ Close", font=FONTS["body"], bg=c["btn_secondary_bg"],
                   fg=c["btn_secondary_fg"], padx=10, pady=4, command=self.destroy).pack(side="right", padx=(4, 0))

        if self.on_step:
            FlatButton(btm, text="⏭ Step Once", font=FONTS["body_bold"], bg=c["btn_secondary_bg"],
                       fg=c["btn_secondary_fg"], padx=12, pady=4, command=self._do_step).pack(side="right", padx=(4, 0))

        if self.on_start:
            FlatButton(btm, text="🚀 Start Visualization ▶", font=FONTS["body_bold"], bg=c["accent"],
                       fg=c["accent_fg"], padx=14, pady=4, command=self._do_start).pack(side="right", padx=(4, 0))

    def _do_start(self) -> None:
        self.destroy()
        if self.on_start: self.on_start()

    def _do_step(self) -> None:
        self.destroy()
        if self.on_step: self.on_step()


def show_concept_briefing(parent: tk.Widget, algo_name: str, on_start: Optional[Callable[[], None]] = None,
                          on_step: Optional[Callable[[], None]] = None, auto_pref_var: Optional[tk.BooleanVar] = None) -> ConceptBriefingModal:
    """Convenience helper to launch the Concept Briefing Modal."""
    return ConceptBriefingModal(parent, algo_name, on_start=on_start, on_step=on_step, auto_pref_var=auto_pref_var)
