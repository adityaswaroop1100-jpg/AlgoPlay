"""
concept_briefing.py - Pre-Flight Concept & Complexity Briefing for AlgoPlay.

Displays an educational briefing card/modal detailing the algorithm's core
concept, step-by-step strategy, real-world analogy, and comprehensive Time &
Space Complexity breakdown before the user begins the visual representation.
Zero external dependencies — pure Python 3 standard library and Tkinter.
"""

import tkinter as tk
from typing import Callable, Dict, Optional
from theme import FONTS, theme_manager
from widgets import FlatButton

ALGO_CONCEPTS: Dict[str, Dict] = {
    "Bubble Sort": {
        "icon": "🫧",
        "tag": "Comparison Sort • In-Place • Stable",
        "concept": "Repeatedly steps through the array, compares adjacent elements, and swaps them if they are in the wrong order. Larger values 'bubble up' to the right.",
        "analogy": "Lining up students by height by repeatedly comparing pairs of neighbours and swapping them until everyone is in order.",
        "steps": [
            "1. Scan left to right, comparing adjacent pairs (arr[j] vs arr[j+1]).",
            "2. If left > right, swap them so the larger value moves rightward.",
            "3. After each full pass, the largest remaining unsorted element is locked into place.",
            "4. Stop early if a full pass completes with zero swaps (array is sorted).",
        ],
        "complexity": {
            "best": ("O(n)", "Already sorted array — early-exit pass detects 0 swaps."),
            "avg": ("O(n²)", "Random order requires ~n²/2 comparisons and ~n²/4 swaps."),
            "worst": ("O(n²)", "Reversed array causes maximum possible comparisons and swaps."),
            "space": ("O(1)", "In-place sort — auxiliary memory is strictly constant."),
        },
        "invariant": "After pass k, the last k elements are in their permanent, sorted positions.",
        "when": "Great for learning and small or nearly-sorted datasets; avoid for large arrays.",
    },
    "Insertion Sort": {
        "icon": "🃏",
        "tag": "Incremental Sort • In-Place • Stable",
        "concept": "Builds the sorted array one item at a time. Takes the next unsorted element and shifts larger sorted elements rightward to insert it into place.",
        "analogy": "Sorting playing cards in your hand: take cards one by one from the deck and slide each into its proper sorted slot.",
        "steps": [
            "1. Assume the first element (index 0) is already a sorted sub-array of length 1.",
            "2. Pick the next element ('key') from the unsorted portion.",
            "3. Compare the key leftward, shifting larger sorted elements 1 position right.",
            "4. Drop the key into the resulting gap and advance to the next element.",
        ],
        "complexity": {
            "best": ("O(n)", "Nearly-sorted data — each key needs only 1 comparison and 0 shifts."),
            "avg": ("O(n²)", "Random data shifts half the sorted prefix on average."),
            "worst": ("O(n²)", "Reversed data requires shifting the full sorted prefix every step."),
            "space": ("O(1)", "Requires only a single temporary variable to hold the active key."),
        },
        "invariant": "At step i, the prefix arr[0..i-1] is guaranteed to be in sorted order.",
        "when": "Ideal for small arrays (n < 30) or continuously streaming real-time data.",
    },
    "Selection Sort": {
        "icon": "🎯",
        "tag": "Selection Sort • In-Place • Unstable",
        "concept": "Divides the array into sorted and unsorted regions. Repeatedly scans the unsorted partition to find the minimum value and swaps it to the front.",
        "analogy": "Scanning a messy bookshelf for the shortest book, placing it first, then repeating for the remaining unsorted books.",
        "steps": [
            "1. Maintain boundary i between sorted (left) and unsorted (right) portions.",
            "2. Scan the unsorted portion to find the index of the absolute minimum element.",
            "3. Swap this minimum element with the item at boundary index i.",
            "4. Increment boundary i by 1 and repeat until the entire array is sorted.",
        ],
        "complexity": {
            "best": ("O(n²)", "Must always scan the full remaining array to verify the minimum."),
            "avg": ("O(n²)", "Always performs n(n-1)/2 comparisons regardless of initial order."),
            "worst": ("O(n²)", "Comparison count is identical even on reverse-sorted input."),
            "space": ("O(1)", "Performs at most n-1 swaps total — minimizes memory writes."),
        },
        "invariant": "Prefix arr[0..i] contains the i smallest elements in the array in sorted order.",
        "when": "Useful when memory writes (swaps) are significantly more expensive than reads.",
    },
    "Merge Sort": {
        "icon": "⚡",
        "tag": "Divide & Conquer • Out-of-Place • Stable",
        "concept": "Recursively divides the array into halves until single-element arrays are reached, then merges sorted sub-arrays back together in order.",
        "analogy": "Dividing a stack of papers among team members to sort individually, then systematically merging their sorted piles.",
        "steps": [
            "1. Divide: calculate midpoint and split array recursively into left and right halves.",
            "2. Base case: a sub-array of length 1 or 0 is trivially sorted.",
            "3. Conquer: compare the heads of both sorted halves and pick the smaller value.",
            "4. Copy the merged ordered elements back into the target array slice.",
        ],
        "complexity": {
            "best": ("O(n log n)", "Always splits in half (log n levels) with linear merge work (n)."),
            "avg": ("O(n log n)", "Predictable, rock-solid performance across all input distributions."),
            "worst": ("O(n log n)", "Guaranteed upper bound even on malicious worst-case data."),
            "space": ("O(n)", "Requires temporary auxiliary array memory to perform the merge step."),
        },
        "invariant": "Each merged sub-array is strictly sorted before being merged into larger arrays.",
        "when": "Essential when stable sorting and guaranteed O(n log n) runtime are required.",
    },
    "Quick Sort": {
        "icon": "⚖️",
        "tag": "Partition Sort • Divide & Conquer • In-Place",
        "concept": "Selects a 'pivot' element, partitions the array so smaller elements move left and larger move right, then recursively sorts each partition.",
        "analogy": "Appointing a referee in gym class: everyone shorter than the referee steps left, everyone taller steps right.",
        "steps": [
            "1. Choose a pivot element (e.g. the last element or median).",
            "2. Partition: scan from both ends, swapping elements to place < pivot left and > pivot right.",
            "3. Place the pivot into its final, permanent resting spot between both halves.",
            "4. Recursively sort the sub-arrays to the left and right of the pivot.",
        ],
        "complexity": {
            "best": ("O(n log n)", "Balanced partitioning splits array into roughly equal halves."),
            "avg": ("O(n log n)", "Very fast in practice due to high cache locality and low constants."),
            "worst": ("O(n²)", "Highly unbalanced partitions (e.g. already sorted without random pivot)."),
            "space": ("O(log n)", "Call stack memory for recursive partition frames."),
        },
        "invariant": "Once placed, the pivot element is in its permanent, final sorted index forever.",
        "when": "The standard general-purpose sorting algorithm for high-performance applications.",
    },
    "Linear Search": {
        "icon": "🔍",
        "tag": "Sequential Search • Unordered • In-Place",
        "concept": "Examines each element one by one from beginning to end until the target value is found or the end of the array is reached.",
        "analogy": "Searching for a specific receipt in an unsorted stack of papers by checking each receipt one by one.",
        "steps": [
            "1. Initialize pointer i at index 0.",
            "2. Compare arr[i] with the target value.",
            "3. If equal, target is found at index i (Success!).",
            "4. If not equal, advance i by 1; return -1 if the end of the array is reached.",
        ],
        "complexity": {
            "best": ("O(1)", "Target value happens to be located at index 0 (first checked)."),
            "avg": ("O(n)", "On average, scans roughly n/2 elements before finding target."),
            "worst": ("O(n)", "Target is at the very end or absent; all n elements must be scanned."),
            "space": ("O(1)", "Uses zero extra memory beyond a single index pointer."),
        },
        "invariant": "Target is guaranteed not to exist in indices [0..i-1] after i failed probes.",
        "when": "Use on unsorted or small datasets where sorting beforehand is not cost-effective.",
    },
    "Binary Search": {
        "icon": "🎯",
        "tag": "Divide & Conquer • Logarithmic • Requires Sorted",
        "concept": "Repeatedly halves the search space of a sorted array by probing the middle element and discarding the impossible half.",
        "analogy": "Looking up a word in a dictionary: open to the middle, decide if word is before or after, and discard the other half.",
        "steps": [
            "1. Maintain search range pointers: low = 0, high = n - 1.",
            "2. Compute midpoint index: mid = (low + high) // 2.",
            "3. If arr[mid] == target, match found immediately! Return mid.",
            "4. If arr[mid] < target: discard left half (low = mid + 1); else discard right (high = mid - 1).",
        ],
        "complexity": {
            "best": ("O(1)", "Target is located at the exact middle index on the very first probe."),
            "avg": ("O(log n)", "Cuts the remaining search candidates in half with every probe."),
            "worst": ("O(log n)", "For 1,000,000 items, takes at most 20 comparisons to find or confirm absent."),
            "space": ("O(1)", "Iterative search requires only low, mid, and high pointer variables."),
        },
        "invariant": "The target, if present, is strictly contained within the active slice arr[low..high].",
        "when": "Standard for fast lookups in sorted tables, database indexes, and lookup dictionaries.",
    },
}


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

        # Main scrollable/padded body
        body = tk.Frame(self, bg=c["bg_root"], padx=16, pady=10); body.pack(fill="both", expand=True)

        # 1. Concept & Analogy Card
        c_card = tk.Frame(body, bg=c["bg_card"], padx=14, pady=10, highlightthickness=1, highlightbackground=c["border"])
        c_card.pack(fill="x", pady=(0, 8))
        tk.Label(c_card, text="💡  Core Concept", font=FONTS["subtitle"], bg=c["bg_card"], fg=c["fg_primary"]).pack(anchor="w")
        tk.Label(c_card, text=self.info["concept"], font=FONTS["body"], bg=c["bg_card"],
                 fg=c["fg_primary"], wraplength=580, justify="left").pack(anchor="w", pady=(3, 6))

        # Analogy strip
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
