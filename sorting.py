"""
sorting.py - Five Core Sorting Algorithms with Step Generators for AlgoPlay.

Implements Bubble, Insertion, Selection, Merge, and Quick Sort as subclasses
of AlgorithmBase, yielding granular visualization frames for animation sync.
"""

from typing import Any, Dict, Generator, List
from algorithm_base import AlgorithmBase, AlgorithmStep


class BubbleSort(AlgorithmBase):
    """Bubble Sort: Compares adjacent elements and swaps out-of-order pairs."""

    def __init__(self) -> None:
        super().__init__(
            name="Bubble Sort", category="sorting",
            time_best="O(n)", time_avg="O(n²)", time_worst="O(n²)", space_complexity="O(1)",
            description="Compares adjacent elements and swaps them if they are in the wrong order.",
            analogy="Lining up students by height by swapping adjacent pairs.",
            pseudo_code=[
                "for i = 0 to n - 1:",
                "  for j = 0 to n - i - 2:",
                "    if arr[j] > arr[j + 1]: swap(arr[j], arr[j + 1])",
                "  mark arr[n - 1 - i] as sorted",
            ],
        )

    def run(self, data: List[int], **kwargs: Any) -> Generator[AlgorithmStep, None, None]:
        arr, n, sorted_idx = list(data), len(data), []
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                yield AlgorithmStep(
                    array=list(arr), comparing=[j, j + 1], pointers={"i": i, "j": j}, sorted_indices=list(sorted_idx),
                    pseudo_line=2, status=f"Comparing arr[{j}]={arr[j]} with arr[{j+1}]={arr[j+1]} → {'swap!' if arr[j]>arr[j+1] else 'in order'}",
                    variables={"i": i, "j": j, "arr[j]": arr[j], "arr[j+1]": arr[j+1]},
                )
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    yield AlgorithmStep(
                        array=list(arr), swapping=[j, j + 1], pointers={"i": i, "j": j}, sorted_indices=list(sorted_idx),
                        pseudo_line=2, status=f"↕ Swapped! {arr[j]} ↔ {arr[j+1]} — larger value bubbled right",
                        variables={"i": i, "j": j, "swapped": True},
                    )
            sorted_idx.append(n - 1 - i)
            yield AlgorithmStep(
                array=list(arr), sorted_indices=list(sorted_idx), pseudo_line=3,
                status=f"Pass {i+1} done — {len(sorted_idx)} element(s) in final sorted position",
                variables={"i": i, "sorted_count": len(sorted_idx)},
            )
            if not swapped:
                sorted_idx = list(range(n))
                break
        yield AlgorithmStep(array=list(arr), sorted_indices=list(range(n)), pseudo_line=3,
                            status="Array is fully sorted!", variables={"status": "Complete"})


class InsertionSort(AlgorithmBase):
    """Insertion Sort: Builds sorted array one element at a time by shifting."""

    def __init__(self) -> None:
        super().__init__(
            name="Insertion Sort", category="sorting",
            time_best="O(n)", time_avg="O(n²)", time_worst="O(n²)", space_complexity="O(1)",
            description="Picks next element and shifts larger sorted elements right to insert it.",
            analogy="Sorting playing cards in your hand one by one.",
            pseudo_code=[
                "for i = 1 to n - 1:",
                "  key = arr[i], j = i - 1",
                "  while j >= 0 and arr[j] > key:",
                "    arr[j + 1] = arr[j]; j = j - 1",
                "  arr[j + 1] = key",
            ],
        )

    def run(self, data: List[int], **kwargs: Any) -> Generator[AlgorithmStep, None, None]:
        arr, n = list(data), len(data)
        sorted_idx = [0] if n > 0 else []
        for i in range(1, n):
            key, j = arr[i], i - 1
            yield AlgorithmStep(
                array=list(arr), pivot_index=i, pointers={"i": i}, sorted_indices=list(sorted_idx), pseudo_line=1,
                status=f"🃏 Picked up arr[{i}]={key} — inserting into sorted portion [{0}..{i-1}]", variables={"i": i, "key": key, "j": j},
            )
            while j >= 0:
                yield AlgorithmStep(
                    array=list(arr), comparing=[j, j + 1], pointers={"i": i, "j": j}, pivot_index=i, sorted_indices=list(sorted_idx),
                    pseudo_line=2, status=f"arr[{j}]={arr[j]} {'>' if arr[j]>key else '≤'} key={key} → {'shift right' if arr[j]>key else 'found spot'}",
                    variables={"i": i, "key": key, "j": j, "arr[j]": arr[j]},
                )
                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    yield AlgorithmStep(
                        array=list(arr), swapping=[j, j + 1], pointers={"i": i, "j": j}, sorted_indices=list(sorted_idx),
                        pseudo_line=3, status=f"Shifted {arr[j]} one step right to [{j+1}] to make room",
                        variables={"i": i, "key": key, "j": j},
                    )
                    j -= 1
                else:
                    break
            arr[j + 1] = key
            sorted_idx = list(range(i + 1))
            yield AlgorithmStep(
                array=list(arr), sorted_indices=list(sorted_idx), pseudo_line=4,
                status=f"✅ Placed key={key} at index {j+1} — left [{0}..{i}] fully sorted", variables={"i": i, "key": key, "pos": j + 1},
            )
        yield AlgorithmStep(array=list(arr), sorted_indices=list(range(n)), pseudo_line=4,
                            status="Array is fully sorted!", variables={"status": "Complete"})


class SelectionSort(AlgorithmBase):
    """Selection Sort: Finds the minimum element and places it at the beginning."""

    def __init__(self) -> None:
        super().__init__(
            name="Selection Sort", category="sorting",
            time_best="O(n²)", time_avg="O(n²)", time_worst="O(n²)", space_complexity="O(1)",
            description="Repeatedly finds the smallest remaining item and swaps it into place.",
            analogy="Picking the shortest person in a crowd, standing them first, repeat.",
            pseudo_code=[
                "for i = 0 to n - 1:",
                "  min_idx = i",
                "  for j = i + 1 to n - 1: if arr[j] < arr[min_idx]: min_idx = j",
                "  swap(arr[i], arr[min_idx])",
            ],
        )

    def run(self, data: List[int], **kwargs: Any) -> Generator[AlgorithmStep, None, None]:
        arr, n, sorted_idx = list(data), len(data), []
        for i in range(n):
            min_idx = i
            yield AlgorithmStep(
                array=list(arr), pivot_index=min_idx, pointers={"i": i, "min": min_idx}, sorted_indices=list(sorted_idx), pseudo_line=1,
                status=f"Pass {i}: assume minimum at [{i}]={arr[i]}",
                variables={"i": i, "min_idx": min_idx, "min_val": arr[min_idx]},
            )
            for j in range(i + 1, n):
                yield AlgorithmStep(
                    array=list(arr), comparing=[j, min_idx], pointers={"i": i, "j": j, "min": min_idx}, pivot_index=min_idx,
                    sorted_indices=list(sorted_idx), pseudo_line=2,
                    status=f"arr[{j}]={arr[j]} vs current min arr[{min_idx}]={arr[min_idx]}",
                    variables={"i": i, "j": j, "min_idx": min_idx},
                )
                if arr[j] < arr[min_idx]:
                    min_idx = j
                    yield AlgorithmStep(
                        array=list(arr), pivot_index=min_idx, pointers={"i": i, "j": j, "min": min_idx}, sorted_indices=list(sorted_idx), pseudo_line=2,
                        status=f"👑 New min! arr[{min_idx}]={arr[min_idx]} is smallest so far",
                        variables={"i": i, "j": j, "min_idx": min_idx},
                    )
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                yield AlgorithmStep(
                    array=list(arr), swapping=[i, min_idx], pointers={"i": i, "min": min_idx}, sorted_indices=list(sorted_idx), pseudo_line=3,
                    status=f"↕ Swapped min {arr[i]} into position {i}", variables={"i": i, "swapped_with": min_idx},
                )
            sorted_idx.append(i)
            yield AlgorithmStep(
                array=list(arr), sorted_indices=list(sorted_idx), pseudo_line=3,
                status=f"✅ Position {i} locked — {arr[i]} is in its final place", variables={"i": i, "sorted_count": len(sorted_idx)},
            )
        yield AlgorithmStep(array=list(arr), sorted_indices=list(range(n)), pseudo_line=3,
                            status="Array is fully sorted!", variables={"status": "Complete"})


class MergeSort(AlgorithmBase):
    """Merge Sort: Divide and Conquer sorting using subarray division and merging."""

    def __init__(self) -> None:
        super().__init__(
            name="Merge Sort", category="sorting",
            time_best="O(n log n)", time_avg="O(n log n)", time_worst="O(n log n)", space_complexity="O(n)",
            description="Splits list in half recursively, then merges sorted halves together.",
            analogy="Splitting a deck of cards into pairs, sorting pairs, then merging stacks.",
            pseudo_code=[
                "merge_sort(arr, left, right):",
                "  if left < right:",
                "    mid = (left + right) // 2",
                "    merge_sort(left, mid); merge_sort(mid + 1, right)",
                "    merge(left, mid, right)",
            ],
        )

    def run(self, data: List[int], **kwargs: Any) -> Generator[AlgorithmStep, None, None]:
        arr, n = list(data), len(data)

        def _merge(left: int, mid: int, right: int) -> Generator[AlgorithmStep, None, None]:
            merged, i, j = [], left, mid + 1
            while i <= mid and j <= right:
                yield AlgorithmStep(
                    array=list(arr), comparing=[i, j], pointers={"i": i, "j": j}, pseudo_line=4,
                    status=f"Merge: arr[{i}]={arr[i]} vs arr[{j}]={arr[j]} → take {'left' if arr[i]<=arr[j] else 'right'}",
                    variables={"left": left, "mid": mid, "right": right, "i": i, "j": j},
                )
                if arr[i] <= arr[j]:
                    merged.append(arr[i]); i += 1
                else:
                    merged.append(arr[j]); j += 1
            while i <= mid:
                merged.append(arr[i]); i += 1
            while j <= right:
                merged.append(arr[j]); j += 1
            for k, val in enumerate(merged):
                arr[left + k] = val
                yield AlgorithmStep(
                    array=list(arr), swapping=[left + k], pointers={"pos": left+k}, pseudo_line=4,
                    status=f"Placed {val} → position {left+k}",
                    variables={"left": left, "right": right, "pos": left + k, "val": val},
                )

        def _sort(left: int, right: int) -> Generator[AlgorithmStep, None, None]:
            if left < right:
                mid = (left + right) // 2
                yield AlgorithmStep(
                    array=list(arr), pivot_index=mid, pointers={"mid": mid}, pseudo_line=2,
                    status=f"Divide [{left}..{right}] — left half [{left}..{mid}], right [{mid+1}..{right}]",
                    variables={"left": left, "mid": mid, "right": right},
                )
                yield from _sort(left, mid)
                yield from _sort(mid + 1, right)
                yield from _merge(left, mid, right)

        if n > 0:
            yield from _sort(0, n - 1)
        yield AlgorithmStep(array=list(arr), sorted_indices=list(range(n)), pseudo_line=4,
                            status="Array is fully sorted!", variables={"status": "Complete"})


class QuickSort(AlgorithmBase):
    """Quick Sort: Partitions array around a pivot placing smaller items left, larger right."""

    def __init__(self) -> None:
        super().__init__(
            name="Quick Sort", category="sorting",
            time_best="O(n log n)", time_avg="O(n log n)", time_worst="O(n²)", space_complexity="O(log n)",
            description="Partitions array around a pivot element, then recurses on subarrays.",
            analogy="Choosing a referee and having lower scores line up left, higher on right.",
            pseudo_code=[
                "quick_sort(arr, low, high):",
                "  if low < high:",
                "    p = partition(arr, low, high)",
                "    quick_sort(low, p - 1); quick_sort(p + 1, high)",
            ],
        )

    def run(self, data: List[int], **kwargs: Any) -> Generator[AlgorithmStep, None, None]:
        arr, n, confirmed = list(data), len(data), []

        def _sort(low: int, high: int) -> Generator[AlgorithmStep, None, None]:
            if low < high:
                pivot, i = arr[high], low - 1
                yield AlgorithmStep(array=list(arr), pivot_index=high, pointers={"pivot": high}, sorted_indices=list(confirmed),
                                    pseudo_line=2, status=f"🎯 Pivot = {pivot} (arr[{high}]) — elements < pivot go left, ≥ go right",
                                    variables={"low": low, "high": high, "pivot": pivot})
                for j in range(low, high):
                    yield AlgorithmStep(array=list(arr), comparing=[j, high], pointers={"i": i, "j": j, "pivot": high}, pivot_index=high,
                                        sorted_indices=list(confirmed), pseudo_line=2,
                                        status=f"arr[{j}]={arr[j]} {'< pivot='+str(pivot)+' → extends left zone' if arr[j]<pivot else '>= pivot → stays right'}",
                                        variables={"i": i, "j": j, "pivot": pivot})
                    if arr[j] < pivot:
                        i += 1
                        arr[i], arr[j] = arr[j], arr[i]
                        yield AlgorithmStep(array=list(arr), swapping=[i, j], pointers={"i": i, "j": j, "pivot": high}, pivot_index=high,
                                            sorted_indices=list(confirmed), pseudo_line=2,
                                            status=f"↕ Swapped arr[{i}]↔arr[{j}] — extending left partition",
                                            variables={"i": i, "j": j, "pivot": pivot})
                arr[i + 1], arr[high] = arr[high], arr[i + 1]
                p = i + 1
                yield AlgorithmStep(array=list(arr), swapping=[p, high], pointers={"pivot": p}, sorted_indices=list(confirmed),
                                    pseudo_line=2, status=f"✅ Pivot {pivot} placed at final index {p}!",
                                    variables={"pivot_pos": p, "pivot": pivot})
                confirmed.append(p)
                yield from _sort(low, p - 1)
                yield from _sort(p + 1, high)
            elif low == high:
                confirmed.append(low)

        if n > 0:
            yield from _sort(0, n - 1)
        yield AlgorithmStep(array=list(arr), sorted_indices=list(range(n)), pseudo_line=3,
                            status="Array is fully sorted!", variables={"status": "Complete"})


SORTING_ALGORITHMS: Dict[str, AlgorithmBase] = {
    "Bubble Sort": BubbleSort(),
    "Insertion Sort": InsertionSort(),
    "Selection Sort": SelectionSort(),
    "Merge Sort": MergeSort(),
    "Quick Sort": QuickSort(),
}
