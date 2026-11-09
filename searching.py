"""
searching.py - Linear and Binary Search Algorithms with Step Generators for AlgoPlay.

Implements Linear Search and Binary Search as subclasses of AlgorithmBase,
yielding state steps for target comparison, range elimination, and result pulsing.
"""

from typing import Any, Dict, Generator, List
from algorithm_base import AlgorithmBase, AlgorithmStep


class LinearSearch(AlgorithmBase):
    """Linear Search: Sequentially scans every element until target is found or list ends."""

    def __init__(self) -> None:
        super().__init__(
            name="Linear Search",
            category="searching",
            time_best="O(1)",
            time_avg="O(n)",
            time_worst="O(n)",
            space_complexity="O(1)",
            description="Examines each element from start to finish until target is found.",
            analogy="Checking each book on a shelf one by one from left to right.",
            pseudo_code=[
                "for i = 0 to n - 1:",
                "  if arr[i] == target:",
                "    return i  # Element found!",
                "return -1    # Element not found",
            ],
        )

    def run(self, data: List[int], **kwargs: Any) -> Generator[AlgorithmStep, None, None]:
        arr = list(data)
        n = len(arr)
        target: int = kwargs.get("target", arr[0] if arr else 0)
        eliminated: List[int] = []

        yield AlgorithmStep(
            array=list(arr), pointers={"i": 0},
            pseudo_line=0,
            status=f"🔍 Searching for {target}. Checking each element left to right.",
            variables={"target": target, "i": 0},
            target_value=target,
        )

        for i in range(n):
            val = arr[i]
            # Yield step comparing current item
            yield AlgorithmStep(
                array=list(arr),
                comparing=[i], pointers={"i": i},
                eliminated_indices=list(eliminated),
                pseudo_line=1,
                status=f"arr[{i}]={val} → {'MATCH!' if val==target else 'not a match, continue'}",
                variables={"i": i, "arr[i]": val, "target": target},
                target_value=target,
            )

            if val == target:
                # Found target!
                yield AlgorithmStep(
                    array=list(arr),
                    sorted_indices=[i],
                    eliminated_indices=list(eliminated),
                    found_index=i, pointers={"i": i},
                    pseudo_line=2,
                    status=f"🎉 Found {target} at index {i}! Took {i+1} comparisons.",
                    variables={"i": i, "found_at": i, "target": target},
                    target_value=target,
                )
                return

            eliminated.append(i)

        # Reached end without match
        yield AlgorithmStep(
            array=list(arr),
            eliminated_indices=list(range(n)),
            pseudo_line=3,
            status=f"❌ {target} not found. Checked all {n} elements.",
            variables={"target": target, "result": "Not found (-1)"},
            target_value=target,
        )


class BinarySearch(AlgorithmBase):
    """Binary Search: Efficiently searches sorted array by repeatedly halving search interval."""

    def __init__(self) -> None:
        super().__init__(
            name="Binary Search",
            category="searching",
            time_best="O(1)",
            time_avg="O(log n)",
            time_worst="O(log n)",
            space_complexity="O(1)",
            description="Searches a sorted array by dividing search interval in half repeatedly.",
            analogy="Opening a phone book directly to the middle to see which half has the name.",
            pseudo_code=[
                "Ensure array is sorted",
                "low = 0, high = n - 1",
                "while low <= high:",
                "  mid = (low + high) // 2",
                "  if arr[mid] == target: return mid",
                "  else if arr[mid] < target: low = mid + 1",
                "  else: high = mid - 1",
                "return -1",
            ],
        )

    def run(self, data: List[int], **kwargs: Any) -> Generator[AlgorithmStep, None, None]:
        arr = list(data)
        n = len(arr)
        target: int = kwargs.get("target", arr[0] if arr else 0)

        # Check if sorting animation is required first
        is_sorted = all(arr[i] <= arr[i + 1] for i in range(n - 1))
        if not is_sorted:
            yield AlgorithmStep(
                array=list(arr),
                pseudo_line=0,
                status="Array must be sorted before Binary Search! Sorting now...",
                variables={"target": target, "state": "Auto-Sorting"},
                target_value=target,
            )
            # Gentle animated bubble pass to show sorting phase
            for i in range(n):
                for j in range(0, n - i - 1):
                    if arr[j] > arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                        yield AlgorithmStep(
                            array=list(arr),
                            swapping=[j, j + 1], pointers={"j": j},
                            pseudo_line=0,
                            status=f"Pre-sorting array: swapped arr[{j}] and arr[{j+1}]",
                            variables={"target": target, "state": "Sorting array"},
                            target_value=target,
                        )

            yield AlgorithmStep(
                array=list(arr),
                sorted_indices=list(range(n)),
                pseudo_line=0,
                status=f"Array sorted! Ready to binary search for {target}.",
                variables={"target": target, "state": "Sorted"},
                target_value=target,
            )

        low = 0
        high = n - 1

        yield AlgorithmStep(
            array=list(arr),
            pseudo_line=1, pointers={"low": low, "high": high},
            status=f"📐 Search range set: [{low}..{high}], target={target}",
            variables={"low": low, "high": high, "target": target},
            target_value=target,
        )

        while low <= high:
            mid = (low + high) // 2
            mid_val = arr[mid]

            # Compute eliminated indices outside active range [low, high]
            eliminated = [idx for idx in range(n) if idx < low or idx > high]

            yield AlgorithmStep(
                array=list(arr),
                comparing=[mid],
                pivot_index=mid, pointers={"low": low, "mid": mid, "high": high},
                eliminated_indices=list(eliminated),
                pseudo_line=3, range_low=low, range_high=high,
                status=f"mid={mid} (arr[{mid}]={mid_val}) vs target={target}",
                variables={"low": low, "mid": mid, "high": high, "arr[mid]": mid_val, "target": target},
                target_value=target,
            )

            if mid_val == target:
                yield AlgorithmStep(
                    array=list(arr),
                    sorted_indices=[mid],
                    eliminated_indices=list(eliminated),
                    found_index=mid, pointers={"mid": mid},
                    pseudo_line=4,
                    status=f"🎉 Found {target} at index {mid}!",
                    variables={"found_at": mid, "target": target, "steps": "Completed"},
                    target_value=target,
                )
                return
            elif mid_val < target:
                yield AlgorithmStep(
                    array=list(arr),
                    comparing=[mid], pointers={"low": mid+1, "mid": mid, "high": high},
                    eliminated_indices=list(eliminated),
                    pseudo_line=5, range_low=mid+1, range_high=high,
                    status=f"arr[{mid}]={mid_val} < {target} → Discard left half! Range now [{mid+1}..{high}]",
                    variables={"low": mid + 1, "mid": mid, "high": high, "target": target},
                    target_value=target,
                )
                low = mid + 1
            else:
                yield AlgorithmStep(
                    array=list(arr),
                    comparing=[mid], pointers={"low": low, "mid": mid, "high": mid-1},
                    eliminated_indices=list(eliminated),
                    pseudo_line=6, range_low=low, range_high=mid-1,
                    status=f"arr[{mid}]={mid_val} > {target} → Discard right half! Range now [{low}..{mid-1}]",
                    variables={"low": low, "mid": mid, "high": high - 1, "target": target},
                    target_value=target,
                )
                high = mid - 1

        all_eliminated = list(range(n))
        yield AlgorithmStep(
            array=list(arr),
            eliminated_indices=all_eliminated,
            pseudo_line=7,
            status=f"❌ {target} not found — search space exhausted ({low} > {high}).",
            variables={"low": low, "high": high, "target": target, "result": "Not found (-1)"},
            target_value=target,
        )


SEARCHING_ALGORITHMS: Dict[str, AlgorithmBase] = {
    "Linear Search": LinearSearch(),
    "Binary Search": BinarySearch(),
}
