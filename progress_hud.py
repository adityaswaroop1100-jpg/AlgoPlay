"""
progress_hud.py - Algorithm Progress HUD + Operation Heatmap for AlgoPlay.

Provides:
  • ProgressHUD  — compact bar showing % of algorithm completion + live ETA
  • HeatmapOverlay — per-index operation counter that the visualizer can stamp
  • LearningTicker — rotating fact/tip strip at the bottom of the main window

Zero external dependencies — pure Python 3 standard library and Tkinter.
"""

import time
import tkinter as tk
from typing import Dict, List, Optional
from theme import FONTS, theme_manager


# ── Learning tips shown in the ticker ────────────────────────────────────────

LEARNING_TIPS: List[str] = [
    "💡 Bubble Sort gets its name because large values 'bubble up' to the top.",
    "💡 Binary Search only works on sorted arrays — always sort first!",
    "💡 Quick Sort's performance depends heavily on the pivot choice.",
    "💡 Insertion Sort is very fast on nearly-sorted data (O(n) best case).",
    "💡 Merge Sort is a stable sort — equal elements keep their original order.",
    "💡 Selection Sort always makes exactly n-1 swaps, no matter the input.",
    "💡 Linear Search is O(n) even in the best case — no shortcuts!",
    "💡 Binary Search achieves O(log n) by halving the search space each step.",
    "💡 O(n log n) is the theoretical fastest any comparison sort can achieve.",
    "💡 Space complexity matters! Merge Sort needs O(n) extra memory.",
    "💡 In-place algorithms (like Bubble/Insertion) use O(1) extra space.",
    "💡 Stability means equal elements appear in the same order as input.",
    "💡 Quick Sort is usually faster in practice despite O(n²) worst case.",
    "💡 The 'sorted' invariant: after pass k, the last k elements are in place.",
    "💡 Try the Race mode to compare two algorithms head-to-head!",
    "💡 Press Space or → to step through the algorithm one action at a time.",
]


# ── Progress HUD ──────────────────────────────────────────────────────────────

class ProgressHUD(tk.Frame):
    """
    Compact progress bar + live stats strip.
    Shows algorithm completion %, total ops so far, and estimated steps left.
    """

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        kwargs.setdefault("bg", theme_manager.get("bg_card"))
        super().__init__(parent, **kwargs)
        self._total_steps = 0
        self._done_steps = 0
        self._start_ts: Optional[float] = None
        self._build_ui()
        theme_manager.register_listener(self.apply_theme)

    def _build_ui(self) -> None:
        c = theme_manager.colors

        # Row: label + step counter + ETA
        hdr = tk.Frame(self, bg=c["bg_card"], padx=10, pady=3)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📈 Progress", font=FONTS["caption_bold"],
                 bg=c["bg_card"], fg=c["fg_primary"]).pack(side="left")
        self.lbl_steps = tk.Label(hdr, text="Step 0 / ?", font=FONTS["caption"],
                                   bg=c["bg_card"], fg=c["fg_secondary"])
        self.lbl_steps.pack(side="right")

        # Progress track
        self.track = tk.Frame(self, bg=c["bg_card_inner"], height=6,
                              highlightthickness=1, highlightbackground=c["border"])
        self.track.pack(fill="x", padx=10, pady=(0, 4))
        self.track.pack_propagate(False)
        self.bar = tk.Frame(self.track, bg=c["accent"], height=6)
        self.bar.place(x=0, y=0, relheight=1.0, relwidth=0.0)

    def set_total(self, total: int) -> None:
        self._total_steps = total
        self._done_steps = 0
        self._start_ts = time.time()
        self._refresh()

    def advance(self) -> None:
        if self._start_ts is None:
            self._start_ts = time.time()
        self._done_steps += 1
        self._refresh()

    def reset(self) -> None:
        self._done_steps = 0; self._total_steps = 0; self._start_ts = None
        self._refresh()

    def _refresh(self) -> None:
        total = max(1, self._total_steps)
        done = min(self._done_steps, total)
        pct = done / total
        self.bar.place(relwidth=pct)
        eta = ""
        if self._start_ts and done > 0 and done < total:
            elapsed = time.time() - self._start_ts
            rate = done / elapsed if elapsed > 0 else 0
            remaining = (total - done) / rate if rate > 0 else 0
            eta = f" • ~{remaining:.1f}s left"
        self.lbl_steps.configure(text=f"Step {done} / {self._total_steps or '?'}{eta}")

    def apply_theme(self, colors: Dict[str, str]) -> None:
        c = colors
        self.configure(bg=c["bg_card"])
        for child in self.winfo_children():
            if isinstance(child, tk.Frame): child.configure(bg=c["bg_card"])
        self.track.configure(bg=c["bg_card_inner"], highlightbackground=c["border"])
        self.bar.configure(bg=c["accent"])
        self.lbl_steps.configure(bg=c["bg_card"], fg=c["fg_secondary"])


# ── Heatmap overlay (operation count per array index) ────────────────────────

class HeatmapOverlay:
    """
    Tracks how many times each array index has been touched (compared/swapped).
    Call stamp() on each step; get_colors() returns per-index hex strings for
    the visualizer to use as bar cap overlays.
    """

    PALETTE = [
        "#1E3A5F",  # 0 ops   – deep navy
        "#0369A1",  # 1-2     – blue
        "#0891B2",  # 3-5     – cyan
        "#10B981",  # 6-9     – green
        "#F59E0B",  # 10-14   – amber
        "#EF4444",  # 15+     – red-hot
    ]

    def __init__(self) -> None:
        self._counts: Dict[int, int] = {}
        self.enabled = False

    def reset(self, n: int) -> None:
        self._counts = {i: 0 for i in range(n)}

    def stamp(self, indices: List[int]) -> None:
        for i in indices:
            self._counts[i] = self._counts.get(i, 0) + 1

    def heat_color(self, idx: int) -> str:
        c = self._counts.get(idx, 0)
        if   c == 0:    return self.PALETTE[0]
        elif c <= 2:    return self.PALETTE[1]
        elif c <= 5:    return self.PALETTE[2]
        elif c <= 9:    return self.PALETTE[3]
        elif c <= 14:   return self.PALETTE[4]
        else:           return self.PALETTE[5]

    def get_all(self) -> Dict[int, str]:
        return {i: self.heat_color(i) for i in self._counts}


# ── Learning Tip Ticker ───────────────────────────────────────────────────────

class LearningTicker(tk.Frame):
    """
    Scrolling ticker strip that rotates through LEARNING_TIPS.
    Auto-advances every 7 seconds. Click ← → to navigate manually.
    """

    INTERVAL_MS = 7000

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        kwargs.setdefault("bg", theme_manager.get("bg_card"))
        super().__init__(parent, **kwargs)
        self._idx = 0
        self._after_id: Optional[str] = None
        self._build_ui()
        theme_manager.register_listener(self.apply_theme)
        self._schedule()

    def _build_ui(self) -> None:
        c = theme_manager.colors
        self.configure(highlightthickness=1, highlightbackground=c["border"])

        nav_l = tk.Label(self, text="‹", font=FONTS["body_bold"], bg=c["bg_card"],
                         fg=c["fg_secondary"], padx=6, cursor="hand2")
        nav_l.pack(side="left")
        nav_l.bind("<Button-1>", lambda e: self._prev())

        self.lbl = tk.Label(self, text=LEARNING_TIPS[0], font=FONTS["caption"],
                             bg=c["bg_card"], fg=c["fg_primary"], anchor="w",
                             wraplength=900, justify="left")
        self.lbl.pack(side="left", fill="x", expand=True, padx=4, pady=4)

        nav_r = tk.Label(self, text="›", font=FONTS["body_bold"], bg=c["bg_card"],
                         fg=c["fg_secondary"], padx=6, cursor="hand2")
        nav_r.pack(side="right")
        nav_r.bind("<Button-1>", lambda e: self._next())

        self.dot_f = tk.Frame(self, bg=c["bg_card"]); self.dot_f.pack(side="right", padx=4)
        self._dots: List[tk.Label] = []
        for i in range(min(5, len(LEARNING_TIPS))):
            d = tk.Label(self.dot_f, text="•", font=FONTS["caption"],
                         bg=c["bg_card"], fg=c["accent"] if i == 0 else c["fg_dim"])
            d.pack(side="left")
            self._dots.append(d)

        self.nav_l = nav_l; self.nav_r = nav_r

    def _refresh_text(self) -> None:
        tip = LEARNING_TIPS[self._idx % len(LEARNING_TIPS)]
        self.lbl.configure(text=tip)
        for i, d in enumerate(self._dots):
            d.configure(fg=theme_manager.get("accent") if i == self._idx % len(self._dots)
                        else theme_manager.get("fg_dim"))

    def _next(self) -> None:
        self._idx = (self._idx + 1) % len(LEARNING_TIPS)
        self._refresh_text(); self._reschedule()

    def _prev(self) -> None:
        self._idx = (self._idx - 1) % len(LEARNING_TIPS)
        self._refresh_text(); self._reschedule()

    def _schedule(self) -> None:
        self._after_id = self.after(self.INTERVAL_MS, self._auto_next)

    def _reschedule(self) -> None:
        if self._after_id:
            try: self.after_cancel(self._after_id)
            except Exception: pass
        self._schedule()

    def _auto_next(self) -> None:
        self._next()

    def apply_theme(self, colors: Dict[str, str]) -> None:
        c = colors
        self.configure(bg=c["bg_card"], highlightbackground=c["border"])
        self.lbl.configure(bg=c["bg_card"], fg=c["fg_primary"])
        self.nav_l.configure(bg=c["bg_card"], fg=c["fg_secondary"])
        self.nav_r.configure(bg=c["bg_card"], fg=c["fg_secondary"])
        self.dot_f.configure(bg=c["bg_card"])
        for i, d in enumerate(self._dots):
            d.configure(bg=c["bg_card"],
                        fg=c["accent"] if i == self._idx % max(1, len(self._dots)) else c["fg_dim"])
