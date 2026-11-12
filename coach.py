"""
coach.py - Interactive Step Explainer & Concept Guide for AlgoPlay.

Translates algorithm execution into clear, step-by-step visual explanations,
'What to Watch' color guides, expandable 'Why?' deep-dives, and hints.
"""

import tkinter as tk
from typing import Dict, Optional, Tuple
from algorithm_base import AlgorithmStep
from theme import FONTS, theme_manager
from widgets import FlatButton

_WHY: Dict[str, Dict[str, Tuple[str, str]]] = {
    "Bubble": {
        "swap": ("Why swap?", "Adjacent items were out of order. Swapping pushes larger elements toward the end."),
        "compare": ("Why compare adjacent?", "Comparing adjacent items propagates the maximum value rightward on each pass."),
    },
    "Insertion": {
        "shift": ("Why shift right?", "Shifting creates a slot for the active key while maintaining sorted order of the prefix."),
        "compare": ("Why compare backwards?", "We scan left through the sorted prefix until finding where the key fits."),
    },
    "Selection": {
        "swap": ("Why swap minimum?", "Places the smallest remaining item directly into its final position at the prefix boundary."),
        "scan": ("Why scan everything?", "The array is unsorted, so every remaining element must be checked to confirm the minimum."),
    },
    "Merge": {
        "divide": ("Why divide in half?", "Splitting recursively into halves reduces overall work to O(n log n)."),
        "merge": ("Why compare heads?", "Both halves are already sorted, so comparing front items yields the next global minimum."),
    },
    "Quick": {
        "pivot": ("Why choose a pivot?", "The pivot partitions elements: smaller go left, larger go right in O(n) time."),
    },
    "Binary": {
        "probe": ("Why check midpoint?", "Sorted data allows discarding half the search space with each midpoint probe."),
    },
    "Linear": {
        "check": ("Why sequential scan?", "Unsorted data requires checking elements one by one in the worst case."),
    },
    "Jump": {
        "jump": ("Why jump by √n?", "Jumping by strides of √n balances jumping steps with linear scans, minimizing work."),
    },
    "Interpolation": {
        "probe": ("Why interpolate?", "Uniformly distributed values allow estimating position mathematically in O(log log n)."),
    },
    "Exponential": {
        "leap": ("Why double stride?", "Powers of two (1, 2, 4, 8...) bracket the search range in O(log i) steps."),
    },
    "Ternary": {
        "probe": ("Why two midpoints?", "Trisection discards two-thirds or one-third of the search interval per probe."),
    },
}


def _why_text(algo: str, step: AlgorithmStep) -> Tuple[str, str]:
    db = next((_WHY[k] for k in _WHY if k in algo), None)
    if not db: return "Why?", "Keep stepping through to see algorithm decisions in action!"
    entry = None
    if step.swapping: entry = db.get("swap") or db.get("shift") or db.get("merge")
    elif step.comparing: entry = db.get("compare") or db.get("probe") or db.get("check") or db.get("scan") or db.get("leap")
    elif step.pivot_index is not None: entry = db.get("divide") or db.get("pivot") or db.get("jump")
    if not entry: entry = next(iter(db.values()), ("Why?", "Maintaining algorithm invariants."))
    return entry[0], entry[1]


def get_step_info(algo: str, step: AlgorithmStep) -> Tuple[str, str, str]:
    cmp, swp = step.comparing, step.swapping
    arr = step.array or []; n = len(arr)
    if not cmp and not swp and len(step.sorted_indices) == 0:
        return "Step 1", "Initialize", "Pointers initialized. Click 'Start' or 'Step' to begin."
    if len(step.sorted_indices) == n and n > 0:
        return "Complete", "Array Processed", "All elements have been processed into final state."

    if "Bubble" in algo:
        if cmp and len(cmp) >= 2:
            v1, v2 = arr[cmp[0]], arr[cmp[1]]
            return "Step 2 of 4", "Compare", f"Comparing arr[{cmp[0]}] ({v1}) and arr[{cmp[1]}] ({v2})."
        if swp: return "Step 3 of 4", "Swap", "Swapping out-of-order pair. Larger element bubbles rightward."
        return "Step 4 of 4", "Pass Complete", "Pass finished; largest element locked into place."
    if "Insertion" in algo:
        if cmp: return "Step 2 of 4", "Scan Insertion Spot", "Comparing key against sorted prefix elements."
        if swp: return "Step 3 of 4", "Shift Right", "Shifted element rightward to make room for key."
        return "Step 4 of 4", "Insert Key", "Inserted key into its correct sorted slot."
    if "Selection" in algo:
        if cmp: return "Step 2 of 3", "Scan for Minimum", "Comparing candidate against running minimum."
        if swp: return "Step 3 of 3", "Swap Minimum", "Swapping minimum element into sorted prefix."
        return "Step 1 of 3", "Initialize Min", "Scanning remaining elements to find minimum."
    if "Merge" in algo:
        if cmp: return "Step 2 of 3", "Compare Heads", "Comparing front items from both sorted halves."
        return "Step 3 of 3", "Merge", "Writing smallest element back to main array in order."
    if "Quick" in algo:
        if cmp: return "Step 2 of 3", "Partition", "Comparing element against pivot value."
        return "Step 3 of 3", "Pivot Placed", "Pivot locked in position separating partitions."
    if "Binary" in algo:
        if step.found_index is not None: return "Found", "Target Matched!", f"Target located at index {step.found_index}!"
        if cmp: return "Step 2 of 3", "Probe Midpoint", f"Probing midpoint index {step.comparing[0]}."
        return "Step 3 of 3", "Halve Range", "Eliminated half of the search space."
    if "Jump" in algo:
        if step.found_index is not None: return "Found", "Target Located!", f"Target found at index {step.found_index}!"
        if "Jumped" in (step.status or ""): return "Step 1 of 3", "Jump Block", "Jumping ahead by strides of √n."
        return "Step 2 of 3", "Block Linear Scan", "Scanning within bounded candidate block."
    if "Interpolation" in algo:
        if step.found_index is not None: return "Found", "Interpolation Match!", f"Target found at index {step.found_index}!"
        return "Step 2 of 3", "Interpolated Probe", "Probing calculated index based on value magnitude."
    if "Exponential" in algo:
        if step.found_index is not None: return "Found", "Target Found!", f"Target located at index {step.found_index}!"
        if "Exponential leap" in (step.status or ""): return "Step 1 of 3", "Power-of-Two Leap", "Doubling stride to bracket target."
        return "Step 2 of 3", "Binary Search Range", "Binary searching within bracketed bounds."
    if "Ternary" in algo:
        if step.found_index is not None: return "Found", "Target Found!", f"Target matched at index {step.found_index}!"
        return "Step 2 of 3", "Tri-Partition Probe", "Probing dual midpoints mid1 and mid2."
    if "Linear" in algo:
        if step.found_index is not None: return "Found", "Target Located!", f"Found target at index {step.found_index}!"
        return "Step 2 of 3", "Sequential Probe", "Inspecting element sequentially from left to right."

    return "Executing", algo, step.status or "Algorithm executing step..."


class FunCoachPanel(tk.Frame):
    """Step Explainer + 'Why?' expandable deep-dive + 'What to Watch' guide."""

    def __init__(self, parent: tk.Widget, is_searching: bool = False, **kwargs) -> None:
        c = theme_manager.colors
        kwargs.setdefault("bg", c["bg_card"])
        kwargs.setdefault("highlightthickness", 1)
        kwargs.setdefault("highlightbackground", c["border"])
        super().__init__(parent, **kwargs)
        self.is_searching = is_searching
        self._why_expanded = False
        self._current_algo = ""
        self._current_step: Optional[AlgorithmStep] = None
        self._build_ui(c)
        theme_manager.register_listener(self.apply_theme)

    def _build_ui(self, c: Dict[str, str]) -> None:
        self.hdr_f = tk.Frame(self, bg=c["bg_card"], padx=12, pady=6)
        self.hdr_f.pack(fill="x")
        tk.Label(self.hdr_f, text="💡 Step Explainer", font=FONTS["subtitle"],
                 bg=c["bg_card"], fg=c["fg_primary"]).pack(side="left")

        self.body_f = tk.Frame(self, bg=c["bg_card"], padx=12, pady=4)
        self.body_f.pack(fill="x")

        self.lbl_phase = tk.Label(self.body_f, text="Step 1 of 4: Initialize",
                                  font=FONTS["caption_bold"], bg=c["bg_card"], fg=c["accent"])
        self.lbl_phase.pack(anchor="w")

        self.lbl_title = tk.Label(self.body_f, text="Ready to start",
                                  font=FONTS["body_bold"], bg=c["bg_card"], fg=c["fg_primary"])
        self.lbl_title.pack(anchor="w", pady=(2, 0))

        self.lbl_desc = tk.Label(self.body_f, text="Click '▶ Start' or 'Step ⏭' to visualize.",
                                 font=FONTS["caption"], bg=c["bg_card"], fg=c["fg_secondary"],
                                 wraplength=270, justify="left")
        self.lbl_desc.pack(anchor="w", pady=(2, 6))

        self.btn_why = FlatButton(self.body_f, text="🤔 Why? (Expand)", font=FONTS["caption_bold"],
                                  bg=c["btn_secondary_bg"], fg=c["accent"], padx=8, pady=2,
                                  command=self._toggle_why)
        self.btn_why.pack(anchor="w", pady=(0, 4))

        self.why_box = tk.Frame(self.body_f, bg=c["bg_card_inner"], padx=8, pady=6,
                                highlightthickness=1, highlightbackground=c["border"])
        self.lbl_why_title = tk.Label(self.why_box, text="", font=FONTS["caption_bold"],
                                      bg=c["bg_card_inner"], fg=c["fg_primary"], wraplength=260, justify="left")
        self.lbl_why_title.pack(anchor="w")
        self.lbl_why_body = tk.Label(self.why_box, text="", font=FONTS["small"],
                                     bg=c["bg_card_inner"], fg=c["fg_secondary"], wraplength=260, justify="left")
        self.lbl_why_body.pack(anchor="w", pady=(2, 0))

    def _toggle_why(self) -> None:
        self._why_expanded = not self._why_expanded
        c = theme_manager.colors
        if self._why_expanded:
            self.why_box.pack(fill="x", pady=(2, 6))
            self.btn_why.configure(text="🤔 Why? (Collapse)", bg=c["btn_secondary_bg"])
            self._refresh_why()
        else:
            self.why_box.pack_forget()
            self.btn_why.configure(text="🤔 Why? (Expand)", bg=c["btn_secondary_bg"])

    def _refresh_why(self) -> None:
        if not self._why_expanded or not self._current_step: return
        title, body = _why_text(self._current_algo, self._current_step)
        self.lbl_why_title.configure(text=title)
        self.lbl_why_body.configure(text=body)

    def update_step(self, algo_name: str, step: AlgorithmStep) -> None:
        self._current_algo = algo_name
        self._current_step = step
        phase, title, desc = get_step_info(algo_name, step)
        self.lbl_phase.configure(text=phase)
        self.lbl_title.configure(text=title)
        self.lbl_desc.configure(text=desc)
        if self._why_expanded: self._refresh_why()

    def apply_theme(self, colors: Dict[str, str]) -> None:
        c = colors
        self.configure(bg=c["bg_card"], highlightbackground=c["border"])
        self.hdr_f.configure(bg=c["bg_card"])
        self.body_f.configure(bg=c["bg_card"])
        self.lbl_phase.configure(bg=c["bg_card"], fg=c["accent"])
        self.lbl_title.configure(bg=c["bg_card"], fg=c["fg_primary"])
        self.lbl_desc.configure(bg=c["bg_card"], fg=c["fg_secondary"])
        self.why_box.configure(bg=c["bg_card_inner"], highlightbackground=c["border"])
        self.lbl_why_title.configure(bg=c["bg_card_inner"], fg=c["fg_primary"])
        self.lbl_why_body.configure(bg=c["bg_card_inner"], fg=c["fg_secondary"])
        self.btn_why.configure(bg=c["btn_secondary_bg"], fg=c["accent"])
