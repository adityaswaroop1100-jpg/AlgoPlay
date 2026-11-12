"""
concept_data.py - Conceptual metadata and Big-O complexity records for AlgoPlay.

Contains real-world analogies, working steps, invariant definitions,
and Best/Average/Worst/Space complexities for all sorting and searching algorithms.
"""

from typing import Dict, Any

ALGO_CONCEPTS: Dict[str, Dict[str, Any]] = {
    "Bubble Sort": {
        "icon": "🫧", "tag": "Comparison Sort • In-Place • Stable",
        "concept": "Repeatedly steps through the array, compares adjacent elements, and swaps them if they are in the wrong order.",
        "analogy": "Lining up students by height by repeatedly comparing pairs of neighbours and swapping them until everyone is in order.",
        "steps": [
            "1. Scan left to right, comparing adjacent pairs (arr[j] vs arr[j+1]).",
            "2. If left > right, swap them so the larger value moves rightward.",
            "3. After each full pass, the largest remaining unsorted element is locked into place.",
            "4. Stop early if a full pass completes with zero swaps.",
        ],
        "complexity": {
            "best": ("O(n)", "Already sorted array — early-exit pass detects 0 swaps."),
            "avg": ("O(n²)", "Random order requires ~n²/2 comparisons and ~n²/4 swaps."),
            "worst": ("O(n²)", "Reversed array causes maximum possible comparisons and swaps."),
            "space": ("O(1)", "In-place sort — auxiliary memory is strictly constant."),
        },
        "invariant": "After pass k, the last k elements are in their permanent, sorted positions.",
    },
    "Insertion Sort": {
        "icon": "🃏", "tag": "Incremental Sort • In-Place • Stable",
        "concept": "Builds the sorted array one item at a time. Takes the next unsorted element and shifts larger sorted elements rightward to insert it.",
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
            "space": ("O(1)", "In-place insertion sort requires O(1) auxiliary space."),
        },
        "invariant": "Prefix arr[0..i-1] contains the original elements in strictly sorted order.",
    },
    "Selection Sort": {
        "icon": "🎯", "tag": "Selection Sort • In-Place • Unstable",
        "concept": "Divides the array into a sorted and unsorted region. Repeatedly scans the unsorted region for the minimum element and swaps it to the front.",
        "analogy": "Scanning a messy bookshelf for the shortest book, placing it first, then repeating for the remaining unsorted books.",
        "steps": [
            "1. Maintain boundary i between sorted (left) and unsorted (right) portions.",
            "2. Scan all elements in the unsorted region to find the absolute minimum value.",
            "3. Swap that minimum element with the element at boundary index i.",
            "4. Advance boundary i rightward by 1 and repeat until the array is sorted.",
        ],
        "complexity": {
            "best": ("O(n²)", "Must always scan the full remaining array to verify the minimum."),
            "avg": ("O(n²)", "Always performs n*(n-1)/2 comparisons regardless of initial ordering."),
            "worst": ("O(n²)", "Consistent quadratic runtime — performs at most n-1 swaps."),
            "space": ("O(1)", "In-place algorithm requiring only min_idx and loop counters."),
        },
        "invariant": "Prefix arr[0..i] contains the i smallest elements in the array in sorted order.",
    },
    "Merge Sort": {
        "icon": "🔀", "tag": "Divide & Conquer • Out-of-Place • Stable",
        "concept": "Recursively splits the array into two halves until single-element subarrays remain, then merges them back together in sorted order.",
        "analogy": "Splitting a huge pile of exam papers among two teaching assistants, each sorts their half, and they zip the two sorted stacks together.",
        "steps": [
            "1. Divide: Find the midpoint and split array into left and right halves.",
            "2. Conquer: Recursively sort each half until sub-arrays of size 1 are reached.",
            "3. Combine (Merge): Compare heads of both sorted halves and output the smaller.",
            "4. Copy any remaining elements into the output array.",
        ],
        "complexity": {
            "best": ("O(n log n)", "Splitting takes log n levels; each level does n work."),
            "avg": ("O(n log n)", "Consistently divides work evenly into balanced binary tree."),
            "worst": ("O(n log n)", "Guaranteed O(n log n) even in pathological worst-case inputs."),
            "space": ("O(n)", "Requires auxiliary buffer equal to the size of the input array."),
        },
        "invariant": "After merge(low, mid, high), subarray arr[low..high] contains all items in sorted order.",
    },
    "Quick Sort": {
        "icon": "⚡", "tag": "Divide & Conquer • In-Place • Unstable",
        "concept": "Picks a 'pivot' element, partitions the array so smaller elements go left and larger go right, then recursively sorts both partitions.",
        "analogy": "Sorting students by choosing one reference student: everyone shorter moves left, everyone taller moves right.",
        "steps": [
            "1. Select a pivot element (Lomuto scheme chooses the last element arr[high]).",
            "2. Partition: scan array and swap elements so all values <= pivot end up on the left.",
            "3. Place the pivot in its final sorted position between the two partitions.",
            "4. Recursively apply Quick Sort to the left and right sub-arrays.",
        ],
        "complexity": {
            "best": ("O(n log n)", "Balanced partitions divide the array into equal halves."),
            "avg": ("O(n log n)", "Expected runtime over all permutations of distinct elements."),
            "worst": ("O(n²)", "Pathological case when pivot is always smallest or largest."),
            "space": ("O(log n)", "Call stack depth on average; O(n) in worst unbalanced case."),
        },
        "invariant": "All elements left of pivot are <= pivot; all elements right of pivot are >= pivot.",
    },
    "Linear Search": {
        "icon": "🔍", "tag": "Sequential • Unsorted Data • O(1) Space",
        "concept": "Sequentially inspects each element from index 0 to n-1 until target is found or list is exhausted.",
        "analogy": "Flipping through a shuffled deck of cards one by one looking for the Ace of Spades.",
        "steps": [
            "1. Start at index 0 and inspect the current element.",
            "2. If arr[i] == target: declare victory and return index i.",
            "3. If not equal: mark index i as eliminated and increment i.",
            "4. If end of array is reached without a match: return -1.",
        ],
        "complexity": {
            "best": ("O(1)", "Target is at index 0 (first element inspected)."),
            "avg": ("O(n)", "On average, inspects n/2 elements for an item present in array."),
            "worst": ("O(n)", "Target is at the last index or absent entirely."),
            "space": ("O(1)", "Only requires loop index pointer variable."),
        },
        "invariant": "Target is guaranteed not to exist in indices [0..i-1] after i failed probes.",
    },
    "Binary Search": {
        "icon": "⚡🔍", "tag": "Divide & Conquer • Sorted Data • O(1) Space",
        "concept": "Repeatedly halves the active search interval in a sorted array by probing the midpoint.",
        "analogy": "Opening a dictionary in the middle: if word comes alphabetically earlier, discard right half.",
        "steps": [
            "1. Maintain search range pointers: low = 0, high = n - 1.",
            "2. Calculate midpoint index: mid = (low + high) // 2.",
            "3. If arr[mid] == target: match confirmed!",
            "4. If arr[mid] < target: discard left half (low = mid + 1).",
            "5. If arr[mid] > target: discard right half (high = mid - 1).",
        ],
        "complexity": {
            "best": ("O(1)", "Target happens to be at the exact first midpoint probed."),
            "avg": ("O(log n)", "Cuts the remaining search candidates in half with every probe."),
            "worst": ("O(log n)", "Takes at most log2(n) comparisons to locate or confirm absence."),
            "space": ("O(1)", "Iterative search requires only low, mid, and high pointer variables."),
        },
        "invariant": "The target, if present, is strictly contained within the active slice arr[low..high].",
    },
    "Jump Search": {
        "icon": "🦘", "tag": "Block Stepping • Sorted Data • O(1) Space",
        "concept": "Jumps ahead in fixed strides of size m = √n. Once it overshoots the target, it performs a local linear scan backward.",
        "analogy": "Flipping through an encyclopedia volume by jumping 10 pages at a time, then flipping page-by-page when past your topic.",
        "steps": [
            "1. Calculate optimal jump step size: m = floor(sqrt(n)).",
            "2. Probe block endpoints at indices m, 2m, 3m... until arr[min(m, n)-1] >= target.",
            "3. Identify the candidate block bounded between previous jump and current jump.",
            "4. Perform a local linear search within the identified block to locate the exact index.",
        ],
        "complexity": {
            "best": ("O(1)", "Target located on the very first jump probe."),
            "avg": ("O(√n)", "Performs at most n/m jumps + m linear probes, minimized when m = √n."),
            "worst": ("O(√n)", "Target is at the last position of the last candidate block."),
            "space": ("O(1)", "Requires only step and previous block pointer variables."),
        },
        "invariant": "Target cannot exist before index prev; if present, it must be in slice arr[prev..min(step, n)-1].",
    },
    "Interpolation Search": {
        "icon": "📖", "tag": "Value Probing • Uniformly Distributed Data • O(1) Space",
        "concept": "Calculates the likely position of the target using linear interpolation based on the numerical value range.",
        "analogy": "Opening a dictionary near the end when looking up 'Zebra', rather than opening the exact middle.",
        "steps": [
            "1. Check that low <= high and target lies between arr[low] and arr[high].",
            "2. Compute probe position: pos = low + ((target-arr[low])*(high-low)) // (arr[high]-arr[low]).",
            "3. If arr[pos] == target: element found!",
            "4. If arr[pos] < target: narrow search to right sub-range (low = pos + 1).",
            "5. If arr[pos] > target: narrow search to left sub-range (high = pos - 1).",
        ],
        "complexity": {
            "best": ("O(1)", "Formula accurately estimates the exact target index on the first probe."),
            "avg": ("O(log log n)", "Extremely fast sub-logarithmic time on uniformly distributed data."),
            "worst": ("O(n)", "Degrades to linear search on exponentially skewed data distributions."),
            "space": ("O(1)", "Maintains only low, high, and pos pointer variables."),
        },
        "invariant": "Target is strictly contained within arr[low..high] when arr[low] <= target <= arr[high].",
    },
    "Exponential Search": {
        "icon": "⚡🔍", "tag": "Bounded Leaping • Sorted Data • O(1) Space",
        "concept": "Finds a range bounding the target by repeated power-of-two doubling (1, 2, 4, 8...), then runs Binary Search on that bounded interval.",
        "analogy": "Testing WiFi range by walking 1m, 2m, 4m, 8m... then backtracking into the interval once signal drops.",
        "steps": [
            "1. If arr[0] == target: return 0 immediately.",
            "2. Initialize index i = 1; while i < n and arr[i] <= target, double i (i = i * 2).",
            "3. Bounded range is confirmed between low = i // 2 and high = min(i, n - 1).",
            "4. Execute standard Binary Search on the subarray arr[low..high].",
        ],
        "complexity": {
            "best": ("O(1)", "Target located at index 0 or on an exponential boundary."),
            "avg": ("O(log n)", "Takes O(log i) doubling steps + O(log i) binary search steps."),
            "worst": ("O(log n)", "At most 2 * log2(n) comparisons total."),
            "space": ("O(1)", "Operates iteratively with constant auxiliary variables."),
        },
        "invariant": "Target, if present, is bounded between index i/2 and min(i, n-1).",
    },
    "Ternary Search": {
        "icon": "📐", "tag": "Tri-Section • Sorted Data • O(1) Space",
        "concept": "Divides the search interval into three equal sections using two midpoints (mid1, mid2), discarding two-thirds or one-third per step.",
        "analogy": "Surveying a parcel of land by dividing it into three equal plots and eliminating non-promising sectors.",
        "steps": [
            "1. Compute two trisection points: mid1 = low + (high-low)//3, mid2 = high - (high-low)//3.",
            "2. Probe arr[mid1] and arr[mid2] against target.",
            "3. If match at mid1 or mid2: target located!",
            "4. If target < arr[mid1]: discard right two-thirds (high = mid1 - 1).",
            "5. If target > arr[mid2]: discard left two-thirds (low = mid2 + 1).",
            "6. Else: target lies in middle third (low = mid1 + 1, high = mid2 - 1).",
        ],
        "complexity": {
            "best": ("O(1)", "Target matches either mid1 or mid2 on the first probe."),
            "avg": ("O(log₃ n)", "Each iteration reduces the search interval by a factor of 3."),
            "worst": ("O(log₃ n)", "Requires at most 2 * log3(n) comparisons total."),
            "space": ("O(1)", "Iterative implementation uses constant memory."),
        },
        "invariant": "Target is strictly contained within the surviving one-third slice of arr[low..high].",
    },
}
