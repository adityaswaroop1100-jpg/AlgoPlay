"""
race_window.py - Race Mode Window for AlgoPlay.

Side-by-side comparison of two sorting algorithms on identical data,
with live op counters and confetti celebration on winner.
"""

import tkinter as tk
from typing import List
from theme import FONTS, theme_manager
from sorting import SORTING_ALGORITHMS
from visualizer import VisualizerCanvas
from widgets import FlatButton
from algorithm_base import AlgorithmStep
from quiz import play_sound


class RaceWindow(tk.Toplevel):
    """Race Mode: Two algorithms head-to-head on identical arrays + confetti."""

    def __init__(self, parent: tk.Widget, initial_data: List[int]) -> None:
        super().__init__(parent); self.title("AlgoPlay — 🏁 Algorithm Race Mode")
        self.geometry("1050x600"); self.configure(bg=theme_manager.get("bg_root"))
        self.data, self._running, self.c1_ops, self.c2_ops = list(initial_data), False, 0, 0
        self._gen1 = self._gen2 = None; self.done1 = self.done2 = False; self._build_ui()

    def _build_ui(self) -> None:
        c = theme_manager.colors
        bar = tk.Frame(self, bg=c["bg_card"], padx=10, pady=6); bar.pack(fill="x")
        tk.Label(bar, text="Competitor 1:", font=FONTS["body_bold"], bg=c["bg_card"], fg=c["fg_primary"]).pack(side="left")
        self.sel1 = tk.StringVar(value="Merge Sort"); tk.OptionMenu(bar, self.sel1, *SORTING_ALGORITHMS.keys()).pack(side="left", padx=4)
        tk.Label(bar, text="vs. 2:", font=FONTS["body_bold"], bg=c["bg_card"], fg=c["fg_primary"]).pack(side="left", padx=(10, 2))
        self.sel2 = tk.StringVar(value="Bubble Sort"); tk.OptionMenu(bar, self.sel2, *SORTING_ALGORITHMS.keys()).pack(side="left", padx=4)
        self.btn_run = FlatButton(bar, text="▶ Start Race", font=FONTS["body_bold"], bg=c["accent"], fg=c["accent_fg"], padx=10, command=self.start_race)
        self.btn_run.pack(side="left", padx=10)
        FlatButton(bar, text="Rematch", font=FONTS["body_bold"], bg=c["btn_secondary_bg"], fg=c["btn_secondary_fg"], padx=8, command=self.reset_race).pack(side="left")
        self.lbl_win = tk.Label(bar, text="Ready!", font=FONTS["subtitle"], bg=c["bg_card"], fg=c["warning"])
        self.lbl_win.pack(side="right", padx=10)

        body = tk.Frame(self, bg=c["bg_root"]); body.pack(fill="both", expand=True, padx=8, pady=8)
        col1 = tk.Frame(body, bg=c["bg_card"]); col1.pack(side="left", fill="both", expand=True, padx=(0, 4))
        self.lbl1 = tk.Label(col1, text="Algo 1: 0 ops", font=FONTS["body_bold"], bg=c["bg_card"], fg=c["info"])
        self.lbl1.pack(pady=2)
        self.canvas1 = VisualizerCanvas(col1, mode="bars", bg=c["bg_canvas"])
        self.canvas1.pack(fill="both", expand=True, padx=4, pady=4)

        col2 = tk.Frame(body, bg=c["bg_card"]); col2.pack(side="right", fill="both", expand=True, padx=(4, 0))
        self.lbl2 = tk.Label(col2, text="Algo 2: 0 ops", font=FONTS["body_bold"], bg=c["bg_card"], fg=c["warning"])
        self.lbl2.pack(pady=2)
        self.canvas2 = VisualizerCanvas(col2, mode="bars", bg=c["bg_canvas"])
        self.canvas2.pack(fill="both", expand=True, padx=4, pady=4)

    def start_race(self) -> None:
        if self._running: return
        self.reset_race(); self._running = True; self.btn_run.config(state="disabled")
        self._gen1 = SORTING_ALGORITHMS[self.sel1.get()].run(list(self.data))
        self._gen2 = SORTING_ALGORITHMS[self.sel2.get()].run(list(self.data))
        self.lbl_win.config(text="Racing...", fg=theme_manager.get("info")); self._step()

    def _step(self) -> None:
        if not self._running: return
        for s, gen, cv, lbl, da, oa in [(self.sel1.get(), self._gen1, self.canvas1, self.lbl1, "done1", "c1_ops"),
                                         (self.sel2.get(), self._gen2, self.canvas2, self.lbl2, "done2", "c2_ops")]:
            if not getattr(self, da) and gen:
                try:
                    st = next(gen); cv.render_sorting(st, show_labels=False)
                    if st.comparing or st.swapping: setattr(self, oa, getattr(self, oa) + 1)
                    lbl.config(text=f"{s}: {getattr(self, oa)} ops")
                except StopIteration: setattr(self, da, True)
        if self.done1 or self.done2:
            self._running = False; self.btn_run.config(state="normal")
            if not (self.done1 and self.done2):
                wn = self.sel1.get() if self.done1 else self.sel2.get()
                (self.canvas1 if self.done1 else self.canvas2).render_confetti(50); play_sound("Glass")
                self.lbl_win.config(text=f"🏆 Winner: {wn}!", fg=theme_manager.get("success"))
            return
        self.after(25, self._step)

    def reset_race(self) -> None:
        self._running = self.done1 = self.done2 = False; self.c1_ops = self.c2_ops = 0
        self.btn_run.config(state="normal"); self.lbl_win.config(text="Ready!", fg=theme_manager.get("warning"))
        s = AlgorithmStep(array=list(self.data))
        self.canvas1.render_sorting(s, show_labels=False); self.canvas2.render_sorting(s, show_labels=False)
