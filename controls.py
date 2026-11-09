"""
controls.py - UI Panels for Controls, Stats, Pseudo-Code, and Complexity.

Provides interactive widgets (steppers, action buttons, custom input),
real-time metrics, synchronized pseudo-code display, and Big-O complexity pills.
"""

import tkinter as tk
from tkinter import messagebox
from typing import Any, Callable, Dict, List, Optional
from theme import FONTS, theme_manager
from widgets import FlatButton


def _get_btn_palette(is_dark: bool) -> Dict[str, tuple]:
    bg_neu = "#182030" if is_dark else "#F1F5F9"
    fg_neu = "#F8FAFC" if is_dark else "#0F172A"
    bg_rst = "#182030" if is_dark else "#FEF2F2"
    fg_rst = "#F87171" if is_dark else "#DC2626"
    return {
        "btn_random": (bg_neu, fg_neu), "btn_start": ("#2563EB", "#FFFFFF"),
        "btn_pause":  ("#D97706", "#FFFFFF"), "btn_step":  (bg_neu, fg_neu),
        "btn_reset":  (bg_rst, fg_rst),
    }


class ControlPanel(tk.Frame):
    """Control toolbar: size stepper, speed pills, custom input, and action buttons."""

    def __init__(
        self, parent: tk.Widget,
        on_randomize: Callable[[], None], on_start: Callable[[], None],
        on_pause: Callable[[], None], on_step: Callable[[], None], on_reset: Callable[[], None],
        on_custom_load: Callable[[List[int]], None],
        on_size_change: Optional[Callable[[int], None]] = None,
        on_info: Optional[Callable[[], None]] = None,
        is_searching: bool = False, **kwargs,
    ) -> None:
        kwargs.setdefault("bg", theme_manager.get("bg_card"))
        super().__init__(parent, **kwargs)
        self.on_randomize, self.on_start = on_randomize, on_start
        self.on_pause, self.on_step, self.on_reset = on_pause, on_step, on_reset
        self.on_custom_load, self.on_size_change = on_custom_load, on_size_change
        self.on_info = on_info; self.is_searching = is_searching
        self.cur_size = 20; self.cur_speed = "Normal"
        self._build_ui(); theme_manager.register_listener(self.apply_theme)

    def _build_ui(self) -> None:
        c = theme_manager.colors; is_d = theme_manager.current_theme == "dark"

        # ── Row 1: Array Size, Speed, Custom Input ─────────────────────────
        self.r1 = tk.Frame(self, bg=c["bg_card"], padx=10, pady=5); self.r1.pack(fill="x")

        # Array Size Stepper (Segmented Pill)
        tk.Label(self.r1, text="Array Size:", font=FONTS["body_bold"], bg=c["bg_card"], fg=c["fg_primary"]).pack(side="left", padx=(0, 6))
        self.step_box = tk.Frame(self.r1, bg=c["bg_card_inner"], highlightthickness=1, highlightbackground=c["border"])
        self.step_box.pack(side="left", padx=(0, 12))
        self.btn_dec = FlatButton(self.step_box, text=" − ", font=FONTS["body_bold"], bg=c["bg_card_inner"], fg=c["fg_primary"], padx=7, pady=2, command=lambda: self._adj_size(-5))
        self.btn_dec.pack(side="left")
        self.lbl_size = tk.Label(self.step_box, text=str(self.cur_size), font=FONTS["body_bold"], bg=c["bg_card_inner"], fg=c["accent"], width=3, pady=2)
        self.lbl_size.pack(side="left")
        self.btn_inc = FlatButton(self.step_box, text=" + ", font=FONTS["body_bold"], bg=c["bg_card_inner"], fg=c["fg_primary"], padx=7, pady=2, command=lambda: self._adj_size(5))
        self.btn_inc.pack(side="left")

        # Speed Pills (Segmented Capsule)
        tk.Label(self.r1, text="Speed:", font=FONTS["body_bold"], bg=c["bg_card"], fg=c["fg_primary"]).pack(side="left", padx=(4, 6))
        self.spd_box = tk.Frame(self.r1, bg=c["bg_card_inner"], highlightthickness=1, highlightbackground=c["border"])
        self.spd_box.pack(side="left", padx=(0, 12))
        self.speed_btns = {}
        for sp in ("Slow", "Normal", "Fast"):
            b = FlatButton(self.spd_box, text=sp, font=FONTS["caption_bold"],
                           bg=c["accent"] if sp == self.cur_speed else c["bg_card_inner"],
                           fg="#FFFFFF" if sp == self.cur_speed else c["fg_secondary"],
                           padx=10, pady=2, command=lambda s=sp: self._set_speed(s))
            b.pack(side="left"); self.speed_btns[sp] = b

        # Custom Input (Searchbar Capsule)
        tk.Label(self.r1, text="Custom Input:", font=FONTS["body_bold"], bg=c["bg_card"], fg=c["fg_primary"]).pack(side="left", padx=(4, 6))
        self.inp_box = tk.Frame(self.r1, bg=c["entry_bg"], highlightthickness=1, highlightbackground=c["border"])
        self.inp_box.pack(side="left", padx=(0, 6))
        self.custom_entry = tk.Entry(self.inp_box, width=24, font=FONTS["caption"], bg=c["entry_bg"], fg=c["entry_fg"],
                                     insertbackground=c["fg_primary"], relief="flat", bd=0)
        self.custom_entry.insert(0, "15,8,32,4,19,45,70,11,63,28")
        self.custom_entry.pack(side="left", padx=8, ipady=3)
        self.btn_load = FlatButton(self.inp_box, text="Load", font=FONTS["caption_bold"], bg=c["accent"], fg=c["accent_fg"],
                                   padx=10, pady=2, command=self._parse_custom)
        self.btn_load.pack(side="right", padx=1, pady=1)

        # ── Row 2: Action Buttons & Status ──────────────────────────────────
        self.r2 = tk.Frame(self, bg=c["bg_card"], padx=10, pady=4); self.r2.pack(fill="x")
        btn_pal = _get_btn_palette(is_d)
        specs = [
            ("🎲  Shuffle", self.on_randomize, "btn_random"),
            ("▶  Start",   self.on_start,     "btn_start"),
            ("⏸  Pause",   self.on_pause,     "btn_pause"),
            ("⏭  Step",    self.on_step,      "btn_step"),
            ("↺  Reset",   self.on_reset,     "btn_reset"),
        ]
        self.buttons: Dict[str, FlatButton] = {}
        for text, cmd, key in specs:
            bg, fg = btn_pal[key]
            btn = FlatButton(self.r2, text=text, font=FONTS["body_bold"], bg=bg, fg=fg, padx=12, pady=4, command=cmd)
            btn.pack(side="left", padx=3); self.buttons[key] = btn

        # Info button on far right
        if self.on_info:
            self.btn_info = FlatButton(self.r2, text="ⓘ Guide", font=FONTS["caption_bold"], bg=c["btn_secondary_bg"],
                                       fg=c["btn_secondary_fg"], padx=8, pady=3, command=self.on_info)
            self.btn_info.pack(side="right", padx=(6, 0))

        # Status text
        self.lbl_status = tk.Label(self.r2, text="Ready to visualize • Choose an algorithm and press Start",
                                   font=FONTS["caption"], bg=c["bg_card"], fg=c["fg_secondary"])
        self.lbl_status.pack(side="right", padx=6)

    def _adj_size(self, delta: int) -> None:
        self.cur_size = max(5, min(50, self.cur_size + delta))
        self.lbl_size.config(text=str(self.cur_size))
        if self.on_size_change: self.on_size_change(self.cur_size)

    def _set_speed(self, sp: str) -> None:
        self.cur_speed = sp; c = theme_manager.colors
        for k, b in self.speed_btns.items():
            b.configure(bg=c["accent"] if k == sp else c["btn_secondary_bg"],
                        fg=c["accent_fg"] if k == sp else c["btn_secondary_fg"])

    def get_delay_ms(self) -> int:
        delays = {"Slow": 600, "Normal": 220, "Fast": 30}
        return delays.get(self.cur_speed, 220)

    def _parse_custom(self) -> None:
        raw = self.custom_entry.get().strip()
        try:
            items = [int(x.strip()) for x in raw.split(",") if x.strip()]
            if not items: raise ValueError()
            self.on_custom_load(items[:50])
        except Exception:
            messagebox.showerror("Invalid Input", "Enter comma-separated integers, e.g. 15,8,32,4,19,45")

    def set_running_state(self, running: bool) -> None:
        self.buttons["btn_start"].config(state="disabled" if running else "normal")
        self.buttons["btn_pause"].config(state="normal"   if running else "disabled")
        self.buttons["btn_step"].config( state="disabled" if running else "normal")
        self.lbl_status.config(text="Visualizing algorithm step-by-step..." if running else "Paused • Ready for next step")

    def apply_theme(self, colors: Dict[str, str]) -> None:
        c = colors
        self.configure(bg=c["bg_card"]); self.r1.configure(bg=c["bg_card"]); self.r2.configure(bg=c["bg_card"])
        if hasattr(self, "step_box"): self.step_box.configure(bg=c["bg_card_inner"], highlightbackground=c["border"])
        if hasattr(self, "spd_box"):  self.spd_box.configure(bg=c["bg_card_inner"], highlightbackground=c["border"])
        if hasattr(self, "inp_box"):  self.inp_box.configure(bg=c["entry_bg"], highlightbackground=c["border"])
        self.lbl_size.configure(bg=c["bg_card_inner"], fg=c["accent"])
        self.btn_dec.configure(bg=c["bg_card_inner"], fg=c["fg_primary"])
        self.btn_inc.configure(bg=c["bg_card_inner"], fg=c["fg_primary"])
        self.btn_load.configure(bg=c["accent"], fg=c["accent_fg"])
        self.custom_entry.configure(bg=c["entry_bg"], fg=c["entry_fg"], insertbackground=c["fg_primary"])
        self.lbl_status.configure(bg=c["bg_card"], fg=c["fg_secondary"])
        if hasattr(self, "btn_info"): self.btn_info.configure(bg=c["btn_secondary_bg"], fg=c["btn_secondary_fg"])
        for k, b in self.speed_btns.items():
            b.configure(bg=c["accent"] if k == self.cur_speed else c["bg_card_inner"],
                        fg="#FFFFFF" if k == self.cur_speed else c["fg_secondary"])
        btn_pal = _get_btn_palette(theme_manager.current_theme == "dark")
        for key, btn in self.buttons.items():
            if key in btn_pal:
                bg, fg = btn_pal[key]; btn.configure(bg=bg, fg=fg)


# ─────────────────────────────────────────────────────────────────────────────

class StatsPanel(tk.Frame):
    """Statistics section: Comparisons, Swaps, Time in 3 distinct cards."""

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        kwargs.setdefault("bg", theme_manager.get("bg_card"))
        super().__init__(parent, **kwargs)
        self._build_ui(); theme_manager.register_listener(self.apply_theme)

    def _build_ui(self) -> None:
        c = theme_manager.colors
        tk.Label(self, text="📊 Statistics", font=FONTS["subtitle"], bg=c["bg_card"], fg=c["fg_primary"]).pack(anchor="w", padx=10, pady=(6, 4))
        self.row = tk.Frame(self, bg=c["bg_card"]); self.row.pack(fill="x", padx=10, pady=(2, 6))
        self.boxes = []
        for name, col, attr in (("Comparisons", c["warning"], "lbl_comps"),
                                ("Swaps",       c["danger"],  "lbl_swaps"),
                                ("Time",        c["success"], "lbl_time")):
            bx = tk.Frame(self.row, bg=c["bg_card_inner"], padx=12, pady=4, highlightthickness=1, highlightbackground=c["border"])
            bx.pack(side="left", fill="both", expand=True, padx=3); self.boxes.append(bx)
            tk.Label(bx, text=name, font=FONTS["caption"], bg=c["bg_card_inner"], fg=c["fg_secondary"]).pack()
            lbl = tk.Label(bx, text="0" if name != "Time" else "0.00 s", font=FONTS["title"], bg=c["bg_card_inner"], fg=col)
            lbl.pack(); setattr(self, attr, lbl)

    def update_metrics(self, comps: int, swaps: int, time_str: str, status: str = "", vars_dict=None) -> None:
        self.lbl_comps.config(text=str(comps)); self.lbl_swaps.config(text=str(swaps)); self.lbl_time.config(text=time_str)

    def apply_theme(self, colors: Dict[str, str]) -> None:
        c = colors; self.configure(bg=c["bg_card"]); self.row.configure(bg=c["bg_card"])
        for b in getattr(self, "boxes", []): b.configure(bg=c["bg_card_inner"], highlightbackground=c["border"])
        self.lbl_comps.configure(bg=c["bg_card_inner"], fg=c["warning"])
        self.lbl_swaps.configure(bg=c["bg_card_inner"], fg=c["danger"])
        self.lbl_time.configure(bg=c["bg_card_inner"], fg=c["success"])


# ─────────────────────────────────────────────────────────────────────────────

class ComplexityPanel(tk.Frame):
    """Big-O complexity card with Best, Average, Worst, and Space pills."""

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        kwargs.setdefault("bg", theme_manager.get("bg_card"))
        super().__init__(parent, **kwargs)
        self._build_ui(); theme_manager.register_listener(self.apply_theme)

    def _build_ui(self) -> None:
        c = theme_manager.colors
        tk.Label(self, text="⏱ Time Complexity", font=FONTS["subtitle"], bg=c["bg_card"], fg=c["fg_primary"]).pack(anchor="w", padx=10, pady=(6, 4))
        self.row = tk.Frame(self, bg=c["bg_card"]); self.row.pack(fill="x", padx=10, pady=(2, 6))

        self.lbl_best = tk.Label(self.row, text="Best: O(n)", font=FONTS["caption_bold"],
                                 bg=c.get("badge_best_bg", "#062A1F"), fg=c.get("badge_best_fg", "#34D399"),
                                 highlightthickness=1, highlightbackground=c.get("badge_best_border", "#065F46"), padx=10, pady=4)
        self.lbl_best.pack(side="left", padx=(0, 6))
        self.lbl_avg = tk.Label(self.row, text="Average: O(n²)", font=FONTS["caption_bold"],
                                bg=c.get("badge_avg_bg", "#08273F"), fg=c.get("badge_avg_fg", "#38BDF8"),
                                highlightthickness=1, highlightbackground=c.get("badge_avg_border", "#0369A1"), padx=10, pady=4)
        self.lbl_avg.pack(side="left", padx=(0, 6))
        self.lbl_worst = tk.Label(self.row, text="Worst: O(n²)", font=FONTS["caption_bold"],
                                  bg=c.get("badge_worst_bg", "#2E0E14"), fg=c.get("badge_worst_fg", "#F87171"),
                                  highlightthickness=1, highlightbackground=c.get("badge_worst_border", "#991B1B"), padx=10, pady=4)
        self.lbl_worst.pack(side="left", padx=(0, 6))
        self.lbl_space = tk.Label(self.row, text="Space: O(1)", font=FONTS["caption_bold"],
                                  bg=c.get("badge_space_bg", "#281A05"), fg=c.get("badge_space_fg", "#FBBF24"),
                                  highlightthickness=1, highlightbackground=c.get("badge_space_border", "#92400E"), padx=10, pady=4)
        self.lbl_space.pack(side="left")

    def update_info(self, info: Dict[str, str]) -> None:
        self.lbl_best.config(text=f"Best: {info.get('best', '-')}")
        self.lbl_avg.config(text=f"Average: {info.get('average', '-')}")
        self.lbl_worst.config(text=f"Worst: {info.get('worst', '-')}")
        self.lbl_space.config(text=f"Space: {info.get('space', '-')}")

    def apply_theme(self, colors: Dict[str, str]) -> None:
        c = colors; self.configure(bg=c["bg_card"]); self.row.configure(bg=c["bg_card"])
        self.lbl_best.configure(bg=c.get("badge_best_bg", "#062A1F"), fg=c.get("badge_best_fg", "#34D399"), highlightbackground=c.get("badge_best_border", "#065F46"))
        self.lbl_avg.configure(bg=c.get("badge_avg_bg", "#08273F"), fg=c.get("badge_avg_fg", "#38BDF8"), highlightbackground=c.get("badge_avg_border", "#0369A1"))
        self.lbl_worst.configure(bg=c.get("badge_worst_bg", "#2E0E14"), fg=c.get("badge_worst_fg", "#F87171"), highlightbackground=c.get("badge_worst_border", "#991B1B"))
        self.lbl_space.configure(bg=c.get("badge_space_bg", "#281A05"), fg=c.get("badge_space_fg", "#FBBF24"), highlightbackground=c.get("badge_space_border", "#92400E"))


# ─────────────────────────────────────────────────────────────────────────────

class PseudoCodePanel(tk.Frame):
    """Pseudo-code viewer with per-line highlight synchronised to animation."""

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        kwargs.setdefault("bg", theme_manager.get("bg_code"))
        super().__init__(parent, **kwargs)
        self.lines: List[str] = []; self.active_line = -1
        self.hf = tk.Frame(self, bg=theme_manager.get("bg_code"), padx=10, pady=6); self.hf.pack(fill="x")
        self.hdr_lbl = tk.Label(self.hf, text="</> Pseudo-Code", font=FONTS["subtitle"],
                                bg=theme_manager.get("bg_code"), fg=theme_manager.get("fg_primary"))
        self.hdr_lbl.pack(side="left")
        self.chev = tk.Label(self.hf, text="⌄", font=FONTS["subtitle"], bg=theme_manager.get("bg_code"), fg=theme_manager.get("fg_secondary"))
        self.chev.pack(side="right")
        self.text_widget = tk.Text(
            self, font=FONTS["code"], bg=theme_manager.get("bg_code"),
            fg=theme_manager.get("fg_primary"), relief="flat",
            width=28, height=8, highlightthickness=0, wrap="none",
        ); self.text_widget.pack(fill="both", expand=True, padx=8, pady=(0, 6))
        self.text_widget.tag_configure("highlight",
            background=theme_manager.get("code_highlight_bg"),
            foreground=theme_manager.get("code_highlight_fg"))
        theme_manager.register_listener(self.apply_theme)

    def set_code(self, lines: List[str]) -> None:
        self.lines = list(lines)
        self.text_widget.config(state="normal"); self.text_widget.delete("1.0", "end")
        for i, line in enumerate(self.lines, start=1):
            self.text_widget.insert("end", f" {i}  {line}\n")
        self.text_widget.config(state="disabled")

    def highlight_line(self, line_idx: int) -> None:
        self.active_line = line_idx
        self.text_widget.config(state="normal"); self.text_widget.tag_remove("highlight", "1.0", "end")
        if 0 <= line_idx < len(self.lines):
            self.text_widget.tag_add("highlight", f"{line_idx+1}.0", f"{line_idx+1}.end")
            self.text_widget.see(f"{line_idx+1}.0")
        self.text_widget.config(state="disabled")

    def apply_theme(self, colors: Dict[str, str]) -> None:
        self.configure(bg=colors["bg_code"]); self.hf.configure(bg=colors["bg_code"])
        self.hdr_lbl.configure(bg=colors["bg_code"], fg=colors["fg_primary"])
        self.chev.configure(bg=colors["bg_code"], fg=colors["fg_secondary"])
        self.text_widget.configure(bg=colors["bg_code"], fg=colors["fg_primary"])
        self.text_widget.tag_configure("highlight",
            background=colors["code_highlight_bg"], foreground=colors["code_highlight_fg"])
