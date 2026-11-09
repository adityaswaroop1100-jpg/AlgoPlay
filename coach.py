"""
coach.py - Interactive Step Explainer & Concept Guide for AlgoPlay.

Translates algorithm execution into clear, step-by-step visual explanations,
'What to Watch' color guides, expandable 'Why?' deep-dives, and a Hint button.
"""

import tkinter as tk
from typing import Dict, Optional, Tuple
from algorithm_base import AlgorithmStep
from theme import FONTS, theme_manager


# ── Deep "Why?" explanations per algorithm ─────────────────────────────────

_WHY: Dict[str, Dict[str, str]] = {
    "Bubble Sort": {
        "compare": ("Why compare adjacent elements?",
                    "Bubble Sort's invariant: after each full pass, the largest unsorted "
                    "element reaches its final position. By comparing each adjacent pair we "
                    "guarantee that every pass 'bubbles' the maximum to the right end."),
        "swap":    ("Why swap here?",
                    "arr[j] > arr[j+1] violates ascending order. Swapping restores "
                    "local order and moves the larger value one step closer to its final place."),
        "done":    ("Why is it sorted now?",
                    "After n passes each element has been compared against all larger neighbours "
                    "and has 'bubbled' to the correct slot. The array is now fully in order."),
    },
    "Insertion Sort": {
        "pick":    ("Why pick this element?",
                    "Insertion Sort maintains a sorted prefix [0..i-1]. We now extend it by "
                    "picking arr[i] and finding where it belongs inside that prefix."),
        "shift":   ("Why shift right?",
                    "To insert the key into the correct slot, we first create a gap by sliding "
                    "each element that is larger than the key one position to the right."),
        "insert":  ("Why place it here?",
                    "We found the insertion point: everything to the left is ≤ key. "
                    "Placing the key here preserves the sorted-prefix invariant."),
    },
    "Selection Sort": {
        "scan":    ("Why scan for a minimum?",
                    "Selection Sort divides the array into sorted (left) and unsorted (right). "
                    "To extend the sorted section by one, we must find the absolute minimum "
                    "of the unsorted part and move it to the boundary."),
        "swap":    ("Why swap to front?",
                    "Once the minimum is located, swapping it with the first unsorted element "
                    "extends the sorted prefix by exactly one element in a single swap."),
    },
    "Merge Sort": {
        "divide":  ("Why divide into halves?",
                    "Merge Sort uses Divide & Conquer. By recursively splitting into halves "
                    "until trivial (n=1), then merging, the total work is O(n log n) instead "
                    "of the O(n²) of simpler sorts."),
        "merge":   ("Why compare heads of halves?",
                    "Both sub-arrays are already sorted. The global minimum must be one of "
                    "the two front elements, so a single comparison picks the next element "
                    "for the merged output."),
    },
    "Quick Sort": {
        "pivot":   ("Why choose a pivot?",
                    "The pivot acts as a referee: everything < pivot goes left, "
                    "everything > pivot goes right. After partitioning, pivot is in its "
                    "exact final position — no further moves needed for it."),
        "partition": ("Why compare to pivot?",
                      "By scanning from both ends and swapping out-of-place elements "
                      "around the pivot, we achieve in-place partitioning in O(n)."),
    },
    "Binary Search": {
        "probe":   ("Why check the midpoint?",
                    "The array is sorted, so if arr[mid] < target, the target must be in "
                    "the right half; if arr[mid] > target, in the left half. Each probe "
                    "eliminates exactly half the remaining candidates — giving O(log n)."),
        "discard": ("Why discard half?",
                    "Because the array is sorted, all values in the discarded half are "
                    "provably not equal to the target. We safely narrow the search window."),
    },
    "Linear Search": {
        "check":   ("Why check sequentially?",
                    "Linear Search makes no assumptions about order. The only guarantee "
                    "is exhaustive scanning — every element must be checked in the worst case."),
    },
}


def _why_text(algo: str, step: AlgorithmStep) -> Tuple[str, str]:
    """Return (title, body) for the Why? panel given current algo + step."""
    db = None
    for key in _WHY:
        if key in algo:
            db = _WHY[key]; break
    if not db:
        return "Why?", "Keep stepping through to see the algorithm in action!"
    if step.swapping:
        entry = db.get("swap") or db.get("shift") or db.get("merge")
    elif step.comparing:
        entry = db.get("compare") or db.get("probe") or db.get("check") or db.get("merge") or db.get("partition") or db.get("scan")
    elif step.pivot_index is not None:
        entry = db.get("divide") or db.get("pick") or db.get("pivot")
    elif step.sorted_indices and len(step.sorted_indices) == len(step.array):
        entry = db.get("done")
    else:
        entry = next(iter(db.values()), None)
    if entry:
        return entry[0], entry[1]
    return "Why?", "Continue stepping to see the next decision."


def get_step_info(algo: str, step: AlgorithmStep) -> Tuple[str, str, str]:
    """Returns (step_num_str, action_title, action_description)."""
    cmp, swp = step.comparing, step.swapping
    arr = step.array or []
    n = len(arr)
    if not cmp and not swp and len(step.sorted_indices) == 0:
        return "Step 1 of 5", "Initialize pointers", "Starting algorithm pass. Pointers are initialized at the beginning of the array."
    if len(step.sorted_indices) == n and n > 0:
        return "Step 5 of 5", "Array completely sorted", "All elements have been placed into their verified, final ascending positions."
    if "Bubble" in algo:
        if cmp and len(cmp) >= 2:
            i1, i2 = cmp[0], cmp[1]
            if i1 < n and i2 < n:
                v1, v2 = arr[i1], arr[i2]
                res = "swap required" if v1 > v2 else "already in order"
                return "Step 2 of 5", "Compare adjacent elements", f"Compare arr[{i1}] ({v1}) and arr[{i2}] ({v2}). Left is {'>' if v1>v2 else '≤'} right → {res}."
        if swp:
            return "Step 3 of 5", "Swap adjacent elements", "Swapping out-of-order pair. Larger element bubbles rightward toward sorted partition."
        return "Step 4 of 5", "End of pass", "Pass complete! The largest unsorted element has been locked into its final place."
    if "Insertion" in algo:
        if step.pivot_index is not None and not cmp and not swp:
            return "Step 1 of 4", "Pick next unsorted key", f"Selected arr[{step.pivot_index}] as key to insert into sorted prefix on the left."
        if cmp: return "Step 2 of 4", "Scan left for insertion spot", "Comparing current key against sorted prefix elements to find where it fits."
        if swp: return "Step 3 of 4", "Shift elements right", "Shifted larger element rightward by one position to make room for insertion."
        return "Step 4 of 4", "Insert key in place", "Inserted key into its correct sorted location."
    if "Selection" in algo:
        if cmp: return "Step 2 of 4", "Scan for minimum element", "Comparing current candidate against running minimum of the unsorted section."
        if swp: return "Step 3 of 4", "Swap minimum to front", "Found absolute minimum of remaining unsorted items; swapping it to its final place."
        return "Step 1 of 4", "Assume start as minimum", "Scanning remaining elements to find the true minimum value."
    if "Merge" in algo:
        if step.pivot_index is not None and not cmp and not swp:
            return "Step 1 of 3", "Divide into sub-arrays", "Recursively dividing array into left and right halves around midpoint."
        if cmp: return "Step 2 of 3", "Compare sub-array heads", "Comparing front values of both halves to pick the smaller element."
        return "Step 3 of 3", "Merge back in order", "Writing smallest element back to main array in sorted order."
    if "Quick" in algo:
        if step.pivot_index is not None and not cmp and not swp:
            return "Step 1 of 3", "Select pivot element", "Selected pivot referee: elements smaller go left, larger go right."
        if cmp: return "Step 2 of 3", "Partition around pivot", "Comparing element against pivot to determine which partition it belongs to."
        return "Step 3 of 3", "Place pivot into spot", "Placed pivot into its final resting position separating both partitions."
    if "Binary" in algo:
        if step.found_index is not None:
            return "Step 4 of 4", "Target located!", "Midpoint value matches target! Search finished in logarithmic time."
        if cmp: return "Step 2 of 4", "Probe midpoint value", "Comparing target value with midpoint of active search range."
        return "Step 3 of 4", "Discard half of space", "Eliminated half of the remaining array; updated low/high range boundaries."
    if "Linear" in algo:
        if step.found_index is not None:
            return "Step 3 of 3", "Target found!", "Target element identified! Search successfully concluded."
        return "Step 2 of 3", "Check sequential element", "Comparing target against element sequentially from left to right."
    return "Step 1 of 5", "Ready", step.status or "Click '▶ Start' or 'Step ⏭' to visualize."


class FunCoachPanel(tk.Frame):
    """Step Explainer + 'Why?' expandable deep-dive + 'What to Watch' guide."""

    def __init__(self, parent: tk.Widget, is_searching: bool = False, **kwargs) -> None:
        kwargs.setdefault("bg", theme_manager.get("bg_card"))
        super().__init__(parent, **kwargs)
        self.is_searching = is_searching
        self._why_open = False
        self._cur_algo = ""
        self._cur_step: Optional[AlgorithmStep] = None
        self._build_ui()
        theme_manager.register_listener(self.apply_theme)

    def _build_ui(self) -> None:
        c = theme_manager.colors
        self.hdr_f = tk.Frame(self, bg=c["bg_card"], padx=12, pady=6); self.hdr_f.pack(fill="x")
        self.lbl_title = tk.Label(self.hdr_f, text="💡 Step Explainer", font=FONTS["subtitle"],
                                   bg=c["bg_card"], fg=c["fg_primary"]); self.lbl_title.pack(side="left")
        self.lbl_step_num = tk.Label(self.hdr_f, text="Step 1 of 5", font=FONTS["caption"],
                                      bg=c["bg_card"], fg=c["fg_secondary"]); self.lbl_step_num.pack(side="right")

        self.card_box = tk.Frame(self, bg=c["bg_card_inner"], padx=12, pady=8,
                                  highlightthickness=1, highlightbackground=c["border"])
        self.card_box.pack(fill="x", padx=10, pady=(2, 4))
        self.lbl_action_title = tk.Label(self.card_box, text="Compare adjacent elements",
                                          font=FONTS["body_bold"], bg=c["bg_card_inner"],
                                          fg=c.get("bar_default", "#38BDF8"), anchor="w")
        self.lbl_action_title.pack(fill="x")
        self.lbl_action_desc = tk.Label(self.card_box,
                                         text="Click ▶ Start or Step ⏭ to begin.",
                                         font=FONTS["caption"], bg=c["bg_card_inner"],
                                         fg=c["fg_primary"], wraplength=265, justify="left", anchor="w")
        self.lbl_action_desc.pack(fill="x", pady=(4, 0))

        # Why? toggle button
        btn_row = tk.Frame(self, bg=c["bg_card"], padx=10, pady=2); btn_row.pack(fill="x")
        self.btn_why = tk.Label(btn_row, text="🤔 Why?", font=FONTS["caption_bold"],
                                 bg=c["bg_card_inner"], fg=c["accent"], padx=8, pady=3,
                                 highlightthickness=1, highlightbackground=c["border"], cursor="hand2")
        self.btn_why.pack(side="left", padx=(0, 4))
        self.btn_why.bind("<Button-1>", lambda e: self._toggle_why())

        # Collapsible Why? panel
        self.why_panel = tk.Frame(self, bg=c["bg_card_inner"], padx=12, pady=8,
                                   highlightthickness=1, highlightbackground=c["accent"])
        self.lbl_why_title = tk.Label(self.why_panel, text="Why?", font=FONTS["body_bold"],
                                       bg=c["bg_card_inner"], fg=c["accent"], anchor="w")
        self.lbl_why_title.pack(fill="x")
        self.lbl_why_body = tk.Label(self.why_panel, text="",
                                      font=FONTS["caption"], bg=c["bg_card_inner"],
                                      fg=c["fg_primary"], wraplength=265, justify="left", anchor="w")
        self.lbl_why_body.pack(fill="x", pady=(4, 0))

        # What to Watch
        self.wtw_f = tk.Frame(self, bg=c["bg_card"], padx=10, pady=4); self.wtw_f.pack(fill="both", expand=True)
        tk.Label(self.wtw_f, text="👁  What to Watch", font=FONTS["body_bold"],
                 bg=c["bg_card"], fg=c["fg_primary"]).pack(anchor="w", pady=(0, 4))
        self.lbl_wtw_hdr = self.wtw_f.winfo_children()[-1]
        self.bullets = []
        specs = [("🟠", "Orange bars are the elements being compared."),
                 ("🔴", "Red bars are being swapped."),
                 ("🟢", "Green bars are in their final sorted position."),
                 ("🔵", "The array is sorted when all bars turn green."),
                 ] if not self.is_searching else [
                 ("🎯", "Target value is highlighted in the title bar."),
                 ("🟠", "Orange boxes are actively being probed."),
                 ("🟢", "Green box indicates the matching target."),
                 ("⚫", "Dimmed boxes are eliminated from search space."),
                 ]
        for icon, txt in specs:
            row = tk.Frame(self.wtw_f, bg=c["bg_card"]); row.pack(fill="x", pady=2)
            tk.Label(row, text=icon, font=FONTS["caption"], bg=c["bg_card"], width=2).pack(side="left")
            lbl = tk.Label(row, text=txt, font=FONTS["caption"], bg=c["bg_card"],
                           fg=c["fg_secondary"], wraplength=250, justify="left", anchor="w")
            lbl.pack(side="left", fill="x"); self.bullets.append(lbl)

    def _toggle_why(self) -> None:
        self._why_open = not self._why_open
        if self._why_open:
            self.why_panel.pack(fill="x", padx=10, pady=(0, 4))
            self.btn_why.configure(text="🤔 Why? ▲")
            if self._cur_step and self._cur_algo:
                title, body = _why_text(self._cur_algo, self._cur_step)
                self.lbl_why_title.configure(text=title)
                self.lbl_why_body.configure(text=body)
        else:
            self.why_panel.pack_forget()
            self.btn_why.configure(text="🤔 Why?")

    def update_step(self, algo: str, step: AlgorithmStep) -> None:
        self._cur_algo = algo; self._cur_step = step
        step_num, title, desc = get_step_info(algo, step)
        self.lbl_step_num.config(text=step_num)
        self.lbl_action_title.config(text=title)
        self.lbl_action_desc.config(text=desc)
        if self._why_open:
            wt, wb = _why_text(algo, step)
            self.lbl_why_title.configure(text=wt)
            self.lbl_why_body.configure(text=wb)

    def apply_theme(self, colors: Dict[str, str]) -> None:
        c = colors
        self.configure(bg=c["bg_card"]); self.hdr_f.configure(bg=c["bg_card"])
        self.lbl_title.configure(bg=c["bg_card"], fg=c["fg_primary"])
        self.lbl_step_num.configure(bg=c["bg_card"], fg=c["fg_secondary"])
        self.card_box.configure(bg=c["bg_card_inner"], highlightbackground=c["border"])
        self.lbl_action_title.configure(bg=c["bg_card_inner"], fg=c.get("bar_default", "#38BDF8"))
        self.lbl_action_desc.configure(bg=c["bg_card_inner"], fg=c["fg_primary"])
        self.btn_why.configure(bg=c["bg_card_inner"], fg=c["accent"], highlightbackground=c["border"])
        self.why_panel.configure(bg=c["bg_card_inner"], highlightbackground=c["accent"])
        self.lbl_why_title.configure(bg=c["bg_card_inner"], fg=c["accent"])
        self.lbl_why_body.configure(bg=c["bg_card_inner"], fg=c["fg_primary"])
        self.wtw_f.configure(bg=c["bg_card"])
        self.lbl_wtw_hdr.configure(bg=c["bg_card"], fg=c["fg_primary"])
        for lbl in self.bullets:
            lbl.master.configure(bg=c["bg_card"])
            lbl.configure(bg=c["bg_card"], fg=c["fg_secondary"])
