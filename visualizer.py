"""
visualizer.py - Canvas Rendering Engine for AlgoPlay.

Renders sorting bars and search boxes with canvas header, sorted-region
background, fatter glow arches, pass/comparison watermarks, cleaner
top-right legend, pivot dashed line, and richer search annotations.
"""

import random
import tkinter as tk
from typing import Dict, List, Optional, Tuple
from algorithm_base import AlgorithmStep
from theme import FONTS, theme_manager

_PTR: Dict[str, Tuple[str, str]] = {
    "i":("#2563EB","i"), "j":("#F59E0B","j"), "min":("#0284C7","min"),
    "pivot":("#0EA5E9","P"), "mid":("#10B981","mid"),
    "low":("#06B6D4","lo"), "high":("#EF4444","hi"), "pos":("#EAB308","pos"),
}
_ICONS: Dict[str, str] = {
    "Bubble Sort":"🫧","Insertion Sort":"🃏","Selection Sort":"🎯",
    "Merge Sort":"🔀","Quick Sort":"⚡","Linear Search":"🔍","Binary Search":"⚡🔍",
}


class VisualizerCanvas(tk.Canvas):
    """Canvas: data bars with header, partition tints, glow arches, and legend."""

    def __init__(self, parent: tk.Widget, mode: str = "bars", **kwargs) -> None:
        kwargs.setdefault("bg", theme_manager.get("bg_canvas"))
        kwargs.setdefault("highlightthickness", 0)
        super().__init__(parent, **kwargs)
        self.mode = mode; self._last_step: Optional[AlgorithmStep] = None
        self._pulse_state = self._step_counter = self._cmp_counter = 0
        self._algo_name: str = ""
        self.bind("<Configure>", self._on_resize)
        theme_manager.register_listener(self.on_theme_changed)
        self.after(50, self._on_resize); self.after(200, self._on_resize)

    def set_algo_name(self, name: str) -> None: self._algo_name = name
    def reset_counters(self) -> None: self._step_counter = 0; self._cmp_counter = 0

    def _on_resize(self, event=None) -> None:
        if self._last_step:
            (self.render_sorting if self.mode == "bars" else self.render_searching)(self._last_step)

    def on_theme_changed(self, colors: Dict[str, str]) -> None:
        self.configure(bg=colors.get("bg_canvas", "#0D111A")); self._on_resize()

    def _wh(self) -> Tuple[int, int]:
        w = self.winfo_width()  if self.winfo_width()  > 50 else (self.winfo_reqwidth()  or 750)
        h = self.winfo_height() if self.winfo_height() > 50 else (self.winfo_reqheight() or 380)
        return w, h

    def _draw_header(self, w: int, label: str, sub: str = "") -> int:
        """Draws header strip, returns y-offset where content starts."""
        c = theme_manager.colors
        self.create_rectangle(0, 0, w, 34, fill=c["bg_card"], outline="", tags="hdr")
        self.create_line(0, 34, w, 34, fill=c["border"], width=1, tags="hdr")
        self.create_text(14, 17, text=f"{_ICONS.get(label,'📊')}  {label}",
                         font=FONTS["subtitle"], fill=c["fg_primary"], anchor="w", tags="hdr")
        if sub:
            self.create_text(w - 10, 17, text=sub, font=FONTS["caption"],
                             fill=c["fg_secondary"], anchor="e", tags="hdr")
        return 38

    def _legend_row(self, w: int, y: int) -> None:
        """Compact horizontal legend at bottom of canvas."""
        c = theme_manager.colors
        items = [("Default",c["bar_default"]),("Comparing",c["bar_comparing"]),
                 ("Swapping",c["bar_swapping"]),("Sorted",c["bar_sorted"])]
        iw = 92; sx = (w - len(items) * iw) / 2
        for i, (lbl, col) in enumerate(items):
            x = sx + i * iw
            self.create_oval(x, y-4, x+8, y+4, fill=col, outline="", tags="leg")
            self.create_text(x+12, y, text=lbl, font=FONTS["small"],
                             fill=c["fg_secondary"], anchor="w", tags="leg")

    def _pointer_badge(self, cx: float, tip_y: float, name: str) -> None:
        if name not in _PTR: return
        col, lbl = _PTR[name]; pw = max(9, len(lbl)*4+4)
        self.create_rectangle(cx-pw, tip_y-18, cx+pw, tip_y-4, fill=col, outline="", tags="ptr")
        self.create_polygon(cx-3, tip_y-4, cx+3, tip_y-4, cx, tip_y, fill=col, outline="", tags="ptr")
        self.create_text(cx, tip_y-11, text=lbl, font=FONTS["caption_bold"], fill="#FFFFFF", tags="ptr")

    # ---------------------------------------------------------------- sorting
    def render_sorting(self, step: AlgorithmStep, show_labels: bool = True) -> None:
        self._last_step = step
        if step.comparing: self._cmp_counter += 1
        if step.swapping or step.comparing: self._step_counter += 1
        self.delete("all")
        arr = step.array
        if not arr: return
        w, h = self._wh(); c = theme_manager.colors
        sub = f"Cmps: {self._cmp_counter}  Steps: {self._step_counter}"
        pad_top = self._draw_header(w, self._algo_name or "Sorting", sub)
        pad_x, pad_bot = 42, 52; n = len(arr)
        max_val = max(arr) if max(arr) > 0 else 1
        avail_w = w - pad_x - 24; avail_h = h - pad_top - pad_bot
        bw = avail_w / n; y1 = h - pad_bot

        # Y-axis gridlines
        for pct, lbl in ((1.0,"100"),(0.75,"75"),(0.5,"50"),(0.25,"25"),(0.0,"0")):
            gy = y1 - avail_h * pct
            if pct > 0: self.create_line(pad_x, gy, w-20, gy, fill=c["border"], dash=(2,5), tags="grid")
            self.create_text(pad_x-8, gy, text=lbl, font=FONTS["caption"], fill=c["fg_dim"], anchor="e", tags="axis")
        self.create_line(pad_x-4, y1, w-20, y1, fill=c["border"], width=1, tags="grid")

        gap = max(2, int(bw*0.12)) if bw >= 12 else 1

        # Sorted partition tint (right-end contiguous run)
        if step.sorted_indices:
            sset = set(step.sorted_indices)
            right = [i for i in range(n-1,-1,-1) if i in sset]
            # extend while consecutive
            run = []
            for v in right:
                if not run or run[-1] - v == 1: run.append(v)
                else: break
            if len(run) >= 2:
                rx0 = pad_x + min(run)*bw; rx1 = pad_x + (max(run)+1)*bw
                self.create_rectangle(rx0, pad_top, rx1, y1, fill="#061A10", outline="", tags="partition")

        # Pivot dashed horizontal line
        if step.pivot_index is not None and 0 <= step.pivot_index < n:
            pv_y = y1 - (arr[step.pivot_index]/max_val)*avail_h
            self.create_line(pad_x, pv_y, w-20, pv_y, fill=c["bar_pivot"], dash=(4,4), width=1, tags="pvt_line")
            self.create_text(w-22, pv_y-7, text="pivot", font=FONTS["small"], fill=c["bar_pivot"], anchor="e", tags="pvt_line")

        bar_tops: Dict[int,Tuple[float,float]] = {}
        for idx, val in enumerate(arr):
            is_swp = idx in step.swapping; is_pvt = step.pivot_index == idx
            is_cmp = idx in step.comparing; is_srt = idx in step.sorted_indices
            fill = (c["bar_swapping"] if is_swp else c["bar_comparing"] if is_cmp else
                    c["bar_sorted"] if is_srt else c["bar_pivot"] if is_pvt else c["bar_default"])
            bar_h = (val/max_val)*avail_h
            x0 = pad_x + idx*bw + gap//2; x1 = pad_x + (idx+1)*bw - gap//2; y0 = y1 - bar_h
            bar_tops[idx] = ((x0+x1)/2, y0)
            self.create_rectangle(x0, y0, x1, y1, fill=fill, outline="", tags="bar")
            # Cap highlight
            if bar_h >= 6:
                cap = next((c[k] for k in c if k.startswith("bar_cap_") and c.get(k.replace("bar_cap_","bar_"))==fill), fill)
                self.create_rectangle(x0, y0, x1, min(y0+3, y1), fill=cap, outline="", tags="bar")
            # Double-ring glow
            if is_swp:
                self.create_rectangle(x0-2,y0-2,x1+2,y1,outline="#FCA5A5",width=1,tags="glow")
                self.create_rectangle(x0-1,y0-1,x1+1,y1,outline="#EF4444",width=2,tags="glow")
            elif is_cmp:
                self.create_rectangle(x0-2,y0-2,x1+2,y1,outline="#FDE68A",width=1,tags="glow")
                self.create_rectangle(x0-1,y0-1,x1+1,y1,outline="#F59E0B",width=2,tags="glow")
            elif is_pvt:
                self.create_rectangle(x0-1,y0-1,x1+1,y1,outline=c["bar_pivot"],width=2,tags="glow")
            # In-bar badge
            if bar_h >= 24 and bw >= 18:
                badge = "⇄" if is_swp else ("CMP" if is_cmp else ("P" if is_pvt else None))
                if badge: self.create_text((x0+x1)/2, y0+min(16,bar_h/2), text=badge,
                                           font=FONTS["body_bold" if is_swp else "caption_bold"],
                                           fill="#FFFFFF" if is_swp or is_pvt else "#0F172A", tags="badge")
            # Value label
            if show_labels and bw >= 14:
                lbl_y = max(pad_top+28, y0-12); cx = (x0+x1)/2
                if is_swp or is_cmp:
                    self.create_rectangle(cx-14,lbl_y-9,cx+14,lbl_y+9, fill=fill, outline="", tags="vpill")
                    self.create_text(cx, lbl_y, text=str(val), fill="#FFFFFF" if is_swp else "#0F172A",
                                     font=FONTS["caption_bold"], tags="vpill")
                else:
                    self.create_text(cx, lbl_y, text=str(val), fill=c["fg_primary"], font=FONTS["caption_bold"])
                self.create_text(cx, y1+12, text=str(idx), fill=c["fg_secondary"], font=FONTS["caption"])

        # Arch (swap or compare)
        def _arch(i1, i2, col, label, dashed=True):
            cx1,cy1 = bar_tops[i1]; cx2,cy2 = bar_tops[i2]
            at = min(cy1,cy2)-22; mx = (cx1+cx2)/2
            dk = (3,2) if dashed else None
            kw = dict(smooth=True, fill=col, width=2.5 if "SWAP" in label else 2, tags="arch")
            if dk: kw["dash"] = dk
            self.create_line(cx1,cy1-4,mx,at,cx2,cy2-4,**kw)
            self.create_rectangle(mx-36,at-9,mx+36,at+9,fill=col if "SWAP" in label else c["bg_card"],
                                  outline="" if "SWAP" in label else col, width=1 if "SWAP" not in label else 0, tags="arch")
            self.create_text(mx, at, text=label, font=FONTS["caption_bold"],
                             fill="#FFFFFF" if "SWAP" in label else c["fg_primary"], tags="arch")

        if len(step.swapping)>=2 and step.swapping[0] in bar_tops and step.swapping[1] in bar_tops:
            _arch(step.swapping[0], step.swapping[1], c["bar_swapping"], "⟷  SWAP")
        elif len(step.comparing)>=2 and step.comparing[0] in bar_tops and step.comparing[1] in bar_tops:
            v1,v2 = arr[step.comparing[0]], arr[step.comparing[1]]
            op = ">" if v1>v2 else ("<" if v1<v2 else "=")
            _arch(step.comparing[0], step.comparing[1], c["bar_comparing"], f"{v1} {op} {v2}")

        # Pointers
        for name, idx in (step.pointers or {}).items():
            if 0 <= idx < n: self._pointer_badge(pad_x+idx*bw+bw/2, pad_top+22, name)

        # Bottom legend + status
        self._legend_row(w, h-14)
        if step.status:
            self.create_text(w/2, h-pad_bot+30, text=step.status,
                             font=FONTS["caption_bold"], fill=c["fg_secondary"], tags="status")

    # --------------------------------------------------------------- searching
    def render_searching(self, step: AlgorithmStep) -> None:
        self._last_step = step
        if step.comparing: self._cmp_counter += 1
        self._step_counter += 1
        self.delete("all")
        arr = step.array
        if not arr: return
        w, h = self._wh(); c = theme_manager.colors; n = len(arr)
        tgt = getattr(step, "target", None)
        sub = (f"Target: {tgt}  |  " if tgt is not None else "") + f"Probe #{self._cmp_counter}"
        pad_top = self._draw_header(w, self._algo_name or "Searching", sub)

        box_w = min(54.0, max(28.0, (w-60)/n)); box_h = box_w*1.15
        total_w = n*box_w; start_x = max(20.0, (w-total_w)/2)
        cy = (h-pad_top)/2 + pad_top - 10
        r_lo = getattr(step,"range_low",-1); r_hi = getattr(step,"range_high",-1)

        # Active range shading
        if r_lo>=0 and r_hi>=0 and r_lo<=r_hi:
            rx0=start_x+r_lo*box_w; rx1=start_x+(r_hi+1)*box_w
            self.create_rectangle(rx0-2,cy-box_h/2-4,rx1+2,cy+box_h/2+4,
                                  fill="#0A1520", outline=c["accent"], width=1, dash=(3,3), tags="rbg")

        for i, val in enumerate(arr):
            x0=start_x+i*box_w+3; x1=start_x+(i+1)*box_w-3
            y0=cy-box_h/2; y1=cy+box_h/2
            is_found=(step.found_index==i); is_cmp=(i in step.comparing)
            is_elim=(i in step.eliminated_indices)
            if r_lo>=0 and r_hi>=0 and not (r_lo<=i<=r_hi) and not is_found: is_elim=True
            if   is_found: fill,bdr,bw2 = c["bar_sorted"],   c["fg_primary"],  2
            elif is_cmp:   fill,bdr,bw2 = c["bar_comparing"], c["accent"],      2
            elif is_elim:  fill,bdr,bw2 = c["bar_eliminated"],c["border"],      1
            else:          fill,bdr,bw2 = c["bg_card"],       c["border"],      1
            self.create_rectangle(x0,y0,x1,y1,fill=fill,outline=bdr,width=bw2,tags="box")
            if not is_elim:
                cap=c.get("bar_cap_sorted" if is_found else ("bar_cap_comparing" if is_cmp else "bar_cap_default"),fill)
                self.create_rectangle(x0,y0,x1,y0+3,fill=cap,outline="",tags="box")
            # Strikethrough on eliminated
            if is_elim:
                self.create_line(x0+2,y0+2,x1-2,y1-2,fill=c["border"],width=1,tags="elim")
                self.create_line(x1-2,y0+2,x0+2,y1-2,fill=c["border"],width=1,tags="elim")
            # Found pulse + label
            if is_found:
                off = 3+(self._pulse_state%3)*2
                self.create_rectangle(x0-off,y0-off,x1+off,y1+off,outline=c["bar_sorted"],width=1.5,tags="pulse")
                self.create_text((x0+x1)/2,y0-16,text="✓ FOUND",font=FONTS["caption_bold"],fill=c["bar_sorted"],tags="pulse")
                self._pulse_state += 1
            elif is_cmp:
                self.create_text((x0+x1)/2,y0-16,text="PROBE",font=FONTS["caption_bold"],fill=c["bar_comparing"],tags="probe")
            txt_c = "#000000" if (is_cmp and theme_manager.current_theme=="dark") else (c["fg_dim"] if is_elim else c["fg_primary"])
            self.create_text((x0+x1)/2, cy+2, text=str(val), fill=txt_c, font=FONTS["body_bold"])
            self.create_text((x0+x1)/2, y1+14, text=f"[{i}]", fill=c["fg_secondary"], font=FONTS["caption"])

        # Range bracket
        if r_lo>=0 and r_hi>=0 and r_lo<=r_hi:
            bx0=start_x+r_lo*box_w+3; bx1=start_x+(r_hi+1)*box_w-3; by=cy+box_h/2+32
            self.create_line(bx0,by-10,bx0,by,bx1,by,bx1,by-10,fill=c["accent"],width=2,tags="brk")
            self.create_text((bx0+bx1)/2, by+12, text=f"Active Range  [{r_lo} … {r_hi}]",
                             font=FONTS["caption_bold"], fill=c["accent"], tags="brk")

        # Pointers
        ptr_y = cy - box_h/2 - 8
        for name, idx in (step.pointers or {}).items():
            if 0<=idx<n: self._pointer_badge(start_x+idx*box_w+box_w/2, ptr_y, name)

        if step.status:
            self.create_text(w/2, h-10, text=step.status,
                             font=FONTS["caption_bold"], fill=c["fg_secondary"], tags="status")

    # --------------------------------------------------------------- extras
    def render_confetti(self, count: int = 50) -> None:
        w, h = max(400, self.winfo_width()), max(300, self.winfo_height())
        pal = ["#2563EB","#10B981","#F59E0B","#EF4444","#0284C7","#06B6D4"]
        for _ in range(count):
            cx,cy = random.randint(20,w-20), random.randint(20,h-40); r = random.randint(3,6)
            self.create_oval(cx-r,cy-r,cx+r,cy+r,fill=random.choice(pal),outline="",tags="confetti")

    def render_comparison_chart(self, results: Dict[str, int]) -> None:
        self.delete("all"); w,h = self.winfo_width(), self.winfo_height(); c = theme_manager.colors
        self.create_text(w/2, 24, text="📊  Algorithm Comparison Benchmark",
                         fill=c["fg_primary"], font=FONTS["subtitle"])
        if not results: return
        names,vals = list(results.keys()), list(results.values()); mx = max(vals) if max(vals)>0 else 1
        cx0,cy0 = 140,55; cw = w-cx0-70; rh = min(38,(h-cy0-20)/len(names))
        for idx,(name,ops) in enumerate(zip(names,vals)):
            y = cy0+idx*rh+rh/2; bl = (ops/mx)*cw
            col = c["bar_sorted"] if ops==min(vals) else (c["bar_swapping"] if ops==max(vals) else c["bar_default"])
            self.create_text(cx0-10,y,text=name,anchor="e",fill=c["fg_secondary"],font=FONTS["caption_bold"])
            self.create_rectangle(cx0,y-10,cx0+bl,y+10,fill=col,outline="")
            self.create_rectangle(cx0,y-10,cx0+3,y+10,fill=c["fg_primary"],outline="")
            self.create_text(cx0+bl+10,y,text=f"{ops} ops",anchor="w",fill=c["fg_primary"],font=FONTS["caption"])
