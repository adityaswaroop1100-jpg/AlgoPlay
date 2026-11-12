"""
searching.py - Linear, Binary, Jump, Interpolation, Exponential, and Ternary Search.

Implements standard and advanced search algorithms as subclasses of AlgorithmBase,
yielding state steps for range elimination, multi-pointer probes, and target matching.
"""

import math
from typing import Any, Dict, Generator, List
from algorithm_base import AlgorithmBase, AlgorithmStep


def _ensure_sorted(arr: List[int], target: int) -> Generator[AlgorithmStep, None, None]:
    """Ensures array is sorted before running ordered search algorithms."""
    n = len(arr)
    if all(arr[i] <= arr[i + 1] for i in range(n - 1)):
        return
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield AlgorithmStep(array=list(arr), swapping=[j, j + 1], pointers={"j": j},
                                    status=f"Pre-sorting array: {arr[j]} ⇄ {arr[j+1]}", target_value=target)
    yield AlgorithmStep(array=list(arr), sorted_indices=list(range(n)), status=f"Array sorted! Ready to search for {target}.")


class LinearSearch(AlgorithmBase):
    def __init__(self) -> None:
        super().__init__(name="Linear Search", category="searching", time_best="O(1)", time_avg="O(n)",
                         time_worst="O(n)", space_complexity="O(1)",
                         description="Sequentially scans every element from start to finish until target is found.",
                         analogy="Checking each book on a shelf one by one from left to right.",
                         pseudo_code=["for i = 0 to n - 1:", "  if arr[i] == target: return i", "return -1"])

    def run(self, data: List[int], **kwargs: Any) -> Generator[AlgorithmStep, None, None]:
        arr = list(data); n = len(arr); target: int = kwargs.get("target", arr[0] if arr else 0)
        eliminated: List[int] = []
        yield AlgorithmStep(array=list(arr), pointers={"i": 0}, status=f"Searching for {target} left to right.", target_value=target)
        for i in range(n):
            val = arr[i]
            yield AlgorithmStep(array=list(arr), comparing=[i], pointers={"i": i}, eliminated_indices=list(eliminated),
                                pseudo_line=1, status=f"arr[{i}]={val} vs target {target}", target_value=target)
            if val == target:
                yield AlgorithmStep(array=list(arr), sorted_indices=[i], found_index=i, pointers={"i": i},
                                    pseudo_line=1, status=f"🎉 Found {target} at index {i}!", target_value=target)
                return
            eliminated.append(i)
        yield AlgorithmStep(array=list(arr), eliminated_indices=list(range(n)), pseudo_line=2,
                            status=f"❌ {target} not found in array.", target_value=target)


class BinarySearch(AlgorithmBase):
    def __init__(self) -> None:
        super().__init__(name="Binary Search", category="searching", time_best="O(1)", time_avg="O(log n)",
                         time_worst="O(log n)", space_complexity="O(1)",
                         description="Searches a sorted array by repeatedly dividing the search interval in half.",
                         analogy="Opening a dictionary in the middle to see which half contains the word.",
                         pseudo_code=["low = 0, high = n - 1", "while low <= high:", "  mid = (low + high) // 2",
                                      "  if arr[mid] == target: return mid", "  elif arr[mid] < target: low = mid + 1",
                                      "  else: high = mid - 1", "return -1"])

    def run(self, data: List[int], **kwargs: Any) -> Generator[AlgorithmStep, None, None]:
        arr = list(data); n = len(arr); target: int = kwargs.get("target", arr[0] if arr else 0)
        yield from _ensure_sorted(arr, target)
        low, high = 0, n - 1
        while low <= high:
            mid = (low + high) // 2; mid_val = arr[mid]
            elim = [k for k in range(n) if k < low or k > high]
            yield AlgorithmStep(array=list(arr), comparing=[mid], pivot_index=mid, pointers={"low": low, "mid": mid, "high": high},
                                eliminated_indices=elim, pseudo_line=2, range_low=low, range_high=high,
                                status=f"mid={mid} (arr[{mid}]={mid_val}) vs target {target}", target_value=target)
            if mid_val == target:
                yield AlgorithmStep(array=list(arr), sorted_indices=[mid], found_index=mid, pointers={"mid": mid},
                                    pseudo_line=3, status=f"🎉 Found {target} at index {mid}!", target_value=target); return
            elif mid_val < target:
                low = mid + 1
            else:
                high = mid - 1
        yield AlgorithmStep(array=list(arr), eliminated_indices=list(range(n)), pseudo_line=6,
                            status=f"❌ {target} not found in array.", target_value=target)


class JumpSearch(AlgorithmBase):
    def __init__(self) -> None:
        super().__init__(name="Jump Search", category="searching", time_best="O(1)", time_avg="O(√n)",
                         time_worst="O(√n)", space_complexity="O(1)",
                         description="Jumps ahead by fixed blocks of size √n, then performs linear search within block.",
                         analogy="Flipping through a photo album 5 pages at a time, then checking individual photos.",
                         pseudo_code=["m = floor(sqrt(n)), prev = 0", "while arr[min(m, n)-1] < target:",
                                      "  prev = m; m += floor(sqrt(n))", "while arr[prev] < target:",
                                      "  prev += 1", "if arr[prev] == target: return prev", "return -1"])

    def run(self, data: List[int], **kwargs: Any) -> Generator[AlgorithmStep, None, None]:
        arr = list(data); n = len(arr); target: int = kwargs.get("target", arr[0] if arr else 0)
        yield from _ensure_sorted(arr, target)
        step_sz = max(1, int(math.isqrt(n))); prev, step = 0, step_sz
        # Jumping phase
        while step < n and arr[min(step, n) - 1] < target:
            elim = list(range(prev))
            yield AlgorithmStep(array=list(arr), comparing=[min(step, n) - 1], pointers={"low": prev, "high": min(step, n) - 1},
                                eliminated_indices=elim, pseudo_line=1, range_low=prev, range_high=min(step, n) - 1,
                                status=f"🦘 Jumped block to index {min(step,n)-1} (val {arr[min(step,n)-1]} < {target})", target_value=target)
            prev = step; step += step_sz
        # Linear phase within identified block
        block_end = min(step, n)
        elim = [k for k in range(n) if k < prev or k >= block_end]
        yield AlgorithmStep(array=list(arr), pointers={"low": prev, "high": block_end - 1}, eliminated_indices=elim,
                            pseudo_line=3, range_low=prev, range_high=block_end - 1,
                            status=f"Target bounded in block [{prev}..{block_end-1}]. Linear scanning...", target_value=target)
        for idx in range(prev, block_end):
            yield AlgorithmStep(array=list(arr), comparing=[idx], pointers={"i": idx, "low": prev, "high": block_end - 1},
                                eliminated_indices=[k for k in range(n) if k < idx or k >= block_end],
                                pseudo_line=4, status=f"Scanning block: arr[{idx}]={arr[idx]} vs {target}", target_value=target)
            if arr[idx] == target:
                yield AlgorithmStep(array=list(arr), sorted_indices=[idx], found_index=idx, pointers={"i": idx},
                                    pseudo_line=5, status=f"🎉 Found {target} at index {idx} via Jump Search!", target_value=target); return
        yield AlgorithmStep(array=list(arr), eliminated_indices=list(range(n)), pseudo_line=6,
                            status=f"❌ {target} not found.", target_value=target)


class InterpolationSearch(AlgorithmBase):
    def __init__(self) -> None:
        super().__init__(name="Interpolation Search", category="searching", time_best="O(1)", time_avg="O(log log n)",
                         time_worst="O(n)", space_complexity="O(1)",
                         description="Estimates target position using value distribution formula for uniformly distributed data.",
                         analogy="Opening a dictionary near 'Z' when searching for 'Zebra', rather than opening the middle.",
                         pseudo_code=["low = 0, high = n - 1", "while low <= high and arr[low] <= target <= arr[high]:",
                                      "  pos = low + ((target-arr[low])*(high-low))//(arr[high]-arr[low])",
                                      "  if arr[pos] == target: return pos", "  elif arr[pos] < target: low = pos + 1",
                                      "  else: high = pos - 1", "return -1"])

    def run(self, data: List[int], **kwargs: Any) -> Generator[AlgorithmStep, None, None]:
        arr = list(data); n = len(arr); target: int = kwargs.get("target", arr[0] if arr else 0)
        yield from _ensure_sorted(arr, target)
        low, high = 0, n - 1
        while low <= high and arr[low] <= target <= arr[high]:
            if arr[high] == arr[low]:
                pos = low
            else:
                pos = low + int(((target - arr[low]) * (high - low)) / (arr[high] - arr[low]))
            pos = max(low, min(high, pos))
            elim = [k for k in range(n) if k < low or k > high]
            yield AlgorithmStep(array=list(arr), comparing=[pos], pivot_index=pos, pointers={"low": low, "pos": pos, "high": high},
                                eliminated_indices=elim, pseudo_line=2, range_low=low, range_high=high,
                                status=f"📍 Interpolated probe at index {pos} (val {arr[pos]}) for target {target}", target_value=target)
            if arr[pos] == target:
                yield AlgorithmStep(array=list(arr), sorted_indices=[pos], found_index=pos, pointers={"pos": pos},
                                    pseudo_line=3, status=f"🎉 Interpolation hit! Found {target} at index {pos}!", target_value=target); return
            elif arr[pos] < target:
                low = pos + 1
            else:
                high = pos - 1
        yield AlgorithmStep(array=list(arr), eliminated_indices=list(range(n)), pseudo_line=6,
                            status=f"❌ {target} not found within range.", target_value=target)


class ExponentialSearch(AlgorithmBase):
    def __init__(self) -> None:
        super().__init__(name="Exponential Search", category="searching", time_best="O(1)", time_avg="O(log n)",
                         time_worst="O(log n)", space_complexity="O(1)",
                         description="Finds range by repeated power-of-two doubling (1, 2, 4, 8...), then binary searches that range.",
                         analogy="Testing signal range at 1m, 2m, 4m, 8m... then narrowing down once signal is bracketed.",
                         pseudo_code=["if arr[0] == target: return 0", "i = 1", "while i < n and arr[i] <= target: i *= 2",
                                      "return binarySearch(arr, i // 2, min(i, n - 1), target)"])

    def run(self, data: List[int], **kwargs: Any) -> Generator[AlgorithmStep, None, None]:
        arr = list(data); n = len(arr); target: int = kwargs.get("target", arr[0] if arr else 0)
        yield from _ensure_sorted(arr, target)
        if arr[0] == target:
            yield AlgorithmStep(array=list(arr), sorted_indices=[0], found_index=0, pointers={"i": 0},
                                pseudo_line=0, status=f"🎉 Found {target} immediately at index 0!", target_value=target); return
        i = 1
        while i < n and arr[i] <= target:
            yield AlgorithmStep(array=list(arr), comparing=[i], pointers={"pos": i}, pseudo_line=2,
                                status=f"⚡ Exponential leap to index {i} (val {arr[i]} <= {target})", target_value=target)
            if arr[i] == target:
                yield AlgorithmStep(array=list(arr), sorted_indices=[i], found_index=i, pointers={"pos": i},
                                    pseudo_line=2, status=f"🎉 Found {target} at leap index {i}!", target_value=target); return
            i *= 2
        low = i // 2; high = min(i, n - 1)
        elim = [k for k in range(n) if k < low or k > high]
        yield AlgorithmStep(array=list(arr), pointers={"low": low, "high": high}, eliminated_indices=elim,
                            pseudo_line=3, range_low=low, range_high=high,
                            status=f"Target bounded in range [{low}..{high}]. Running Binary Search...", target_value=target)
        while low <= high:
            mid = (low + high) // 2; elim = [k for k in range(n) if k < low or k > high]
            yield AlgorithmStep(array=list(arr), comparing=[mid], pivot_index=mid, pointers={"low": low, "mid": mid, "high": high},
                                eliminated_indices=elim, pseudo_line=3, range_low=low, range_high=high,
                                status=f"Binary search probe mid={mid} (val {arr[mid]}) vs {target}", target_value=target)
            if arr[mid] == target:
                yield AlgorithmStep(array=list(arr), sorted_indices=[mid], found_index=mid, pointers={"mid": mid},
                                    pseudo_line=3, status=f"🎉 Found {target} at index {mid}!", target_value=target); return
            elif arr[mid] < target: low = mid + 1
            else: high = mid - 1
        yield AlgorithmStep(array=list(arr), eliminated_indices=list(range(n)), pseudo_line=3,
                            status=f"❌ {target} not found.", target_value=target)


class TernarySearch(AlgorithmBase):
    def __init__(self) -> None:
        super().__init__(name="Ternary Search", category="searching", time_best="O(1)", time_avg="O(log₃ n)",
                         time_worst="O(log₃ n)", space_complexity="O(1)",
                         description="Divides the search space into three parts using two midpoints (mid1, mid2).",
                         analogy="Dividing a gold mine into three zones and eliminating the non-bearing sections.",
                         pseudo_code=["low = 0, high = n - 1", "while low <= high:", "  mid1 = low + (high - low) // 3",
                                      "  mid2 = high - (high - low) // 3", "  if arr[mid1] == target: return mid1",
                                      "  if arr[mid2] == target: return mid2", "  if target < arr[mid1]: high = mid1 - 1",
                                      "  elif target > arr[mid2]: low = mid2 + 1", "  else: low = mid1 + 1, high = mid2 - 1", "return -1"])

    def run(self, data: List[int], **kwargs: Any) -> Generator[AlgorithmStep, None, None]:
        arr = list(data); n = len(arr); target: int = kwargs.get("target", arr[0] if arr else 0)
        yield from _ensure_sorted(arr, target)
        low, high = 0, n - 1
        while low <= high:
            mid1 = low + (high - low) // 3
            mid2 = high - (high - low) // 3
            elim = [k for k in range(n) if k < low or k > high]
            yield AlgorithmStep(array=list(arr), comparing=[mid1, mid2], pointers={"low": low, "mid": mid1, "pos": mid2, "high": high},
                                eliminated_indices=elim, pseudo_line=2, range_low=low, range_high=high,
                                status=f"Tri-partitioning: mid1={mid1} ({arr[mid1]}), mid2={mid2} ({arr[mid2]}) vs {target}", target_value=target)
            if arr[mid1] == target:
                yield AlgorithmStep(array=list(arr), sorted_indices=[mid1], found_index=mid1, pointers={"mid": mid1},
                                    pseudo_line=4, status=f"🎉 Found {target} at mid1 (index {mid1})!", target_value=target); return
            if arr[mid2] == target:
                yield AlgorithmStep(array=list(arr), sorted_indices=[mid2], found_index=mid2, pointers={"mid": mid2},
                                    pseudo_line=5, status=f"🎉 Found {target} at mid2 (index {mid2})!", target_value=target); return
            if target < arr[mid1]:
                high = mid1 - 1
            elif target > arr[mid2]:
                low = mid2 + 1
            else:
                low = mid1 + 1; high = mid2 - 1
        yield AlgorithmStep(array=list(arr), eliminated_indices=list(range(n)), pseudo_line=9,
                            status=f"❌ {target} not found.", target_value=target)


SEARCHING_ALGORITHMS: Dict[str, AlgorithmBase] = {
    "Linear Search": LinearSearch(),
    "Binary Search": BinarySearch(),
    "Jump Search": JumpSearch(),
    "Interpolation Search": InterpolationSearch(),
    "Exponential Search": ExponentialSearch(),
    "Ternary Search": TernarySearch(),
}
