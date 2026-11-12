// algorithms.js - Core Sorting & Searching Algorithm Step Generators

export class AlgorithmStep {
  constructor(data = {}) {
    this.array = data.array ? [...data.array] : [];
    this.comparing = data.comparing || [];
    this.swapping = data.swapping || [];
    this.sorted_indices = data.sorted_indices || [];
    this.pivot_index = data.pivot_index ?? null;
    this.pseudo_line = data.pseudo_line ?? 0;
    this.pointers = data.pointers || {};
    this.eliminated_indices = data.eliminated_indices || [];
    this.found_index = data.found_index ?? null;
    this.range_low = data.range_low ?? -1;
    this.range_high = data.range_high ?? -1;
    this.status = data.status || "";
    this.target = data.target ?? null;
    this.variables = data.variables || {};
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Sorting Algorithms
// ─────────────────────────────────────────────────────────────────────────────

export const SORTING_ALGORITHMS = {
  "Bubble Sort": {
    name: "Bubble Sort",
    icon: "🫧",
    pseudo_code: [
      "procedure bubbleSort(A : list of sortable items)",
      "  n := length(A)",
      "  for i := 0 to n-1 do",
      "    swapped := false",
      "    for j := 0 to n-i-2 do",
      "      if A[j] > A[j+1] then",
      "        swap(A[j], A[j+1])",
      "        swapped := true",
      "    if not swapped then break"
    ],
    info: {
      name: "Bubble Sort",
      time_best: "O(n)",
      time_avg: "O(n²)",
      time_worst: "O(n²)",
      space: "O(1)",
      description: "Repeatedly steps through the list, compares adjacent elements and swaps them if out of order.",
      analogy: "Lining up students by height by repeatedly swapping adjacent pairs who are out of order.",
      invariant: "After i passes, the last i elements are guaranteed to be in their final sorted positions."
    },
    *run(arr) {
      const a = [...arr];
      const n = a.length;
      const sorted = [];

      yield new AlgorithmStep({ array: a, pseudo_line: 1, status: "Starting Bubble Sort" });

      for (let i = 0; i < n; i++) {
        let swapped = false;
        yield new AlgorithmStep({ array: a, sorted_indices: sorted, pseudo_line: 3, pointers: { i }, status: `Pass ${i + 1} of ${n}` });

        for (let j = 0; j < n - i - 1; j++) {
          yield new AlgorithmStep({
            array: a,
            comparing: [j, j + 1],
            sorted_indices: sorted,
            pseudo_line: 5,
            pointers: { i, j },
            status: `Comparing A[${j}]=${a[j]} and A[${j + 1}]=${a[j + 1]}`
          });

          if (a[j] > a[j + 1]) {
            yield new AlgorithmStep({
              array: a,
              swapping: [j, j + 1],
              sorted_indices: sorted,
              pseudo_line: 6,
              pointers: { i, j },
              status: `Swapping ${a[j]} and ${a[j + 1]}`
            });

            const temp = a[j];
            a[j] = a[j + 1];
            a[j + 1] = temp;
            swapped = true;

            yield new AlgorithmStep({
              array: a,
              swapping: [j, j + 1],
              sorted_indices: sorted,
              pseudo_line: 7,
              pointers: { i, j },
              status: `Swapped: A[${j}]=${a[j]}, A[${j + 1}]=${a[j + 1]}`
            });
          }
        }
        sorted.unshift(n - 1 - i);
        yield new AlgorithmStep({
          array: a,
          sorted_indices: sorted,
          pseudo_line: 8,
          status: `Element ${a[n - 1 - i]} locked in sorted position`
        });
        if (!swapped) break;
      }

      for (let k = 0; k < n; k++) {
        if (!sorted.includes(k)) sorted.push(k);
      }
      yield new AlgorithmStep({ array: a, sorted_indices: sorted, pseudo_line: 8, status: "Array fully sorted!" });
    }
  },

  "Insertion Sort": {
    name: "Insertion Sort",
    icon: "🃏",
    pseudo_code: [
      "procedure insertionSort(A : list of sortable items)",
      "  for i := 1 to length(A)-1 do",
      "    key := A[i]",
      "    j := i - 1",
      "    while j >= 0 and A[j] > key do",
      "      A[j+1] := A[j]",
      "      j := j - 1",
      "    A[j+1] := key"
    ],
    info: {
      name: "Insertion Sort",
      time_best: "O(n)",
      time_avg: "O(n²)",
      time_worst: "O(n²)",
      space: "O(1)",
      description: "Builds sorted array one item at a time by picking the next element and inserting it into its proper position.",
      analogy: "Sorting playing cards in your hand by sliding each new card into its ordered place.",
      invariant: "At the start of each iteration i, the sub-array A[0..i-1] consists of elements originally in A[0..i-1], but in sorted order."
    },
    *run(arr) {
      const a = [...arr];
      const n = a.length;
      const sorted = [0];

      yield new AlgorithmStep({ array: a, sorted_indices: sorted, pseudo_line: 1, status: "Starting Insertion Sort" });

      for (let i = 1; i < n; i++) {
        const key = a[i];
        let j = i - 1;

        yield new AlgorithmStep({
          array: a,
          sorted_indices: sorted,
          pseudo_line: 2,
          pointers: { i, pos: i },
          status: `Selected key = ${key} at index ${i}`
        });

        while (j >= 0) {
          yield new AlgorithmStep({
            array: a,
            comparing: [j, j + 1],
            sorted_indices: sorted,
            pseudo_line: 4,
            pointers: { i, j },
            status: `Comparing A[${j}]=${a[j]} with key ${key}`
          });

          if (a[j] > key) {
            a[j + 1] = a[j];
            yield new AlgorithmStep({
              array: a,
              swapping: [j, j + 1],
              sorted_indices: sorted,
              pseudo_line: 5,
              pointers: { i, j },
              status: `Shifted ${a[j]} rightward to position ${j + 1}`
            });
            j--;
          } else {
            break;
          }
        }
        a[j + 1] = key;
        sorted.push(i);
        yield new AlgorithmStep({
          array: a,
          sorted_indices: [...sorted],
          pseudo_line: 7,
          pointers: { pos: j + 1 },
          status: `Inserted key ${key} at index ${j + 1}`
        });
      }

      yield new AlgorithmStep({
        array: a,
        sorted_indices: Array.from({ length: n }, (_, k) => k),
        pseudo_line: 7,
        status: "Array fully sorted!"
      });
    }
  },

  "Selection Sort": {
    name: "Selection Sort",
    icon: "🎯",
    pseudo_code: [
      "procedure selectionSort(A : list of sortable items)",
      "  n := length(A)",
      "  for i := 0 to n-2 do",
      "    min_idx := i",
      "    for j := i+1 to n-1 do",
      "      if A[j] < A[min_idx] then",
      "        min_idx := j",
      "    if min_idx != i then swap(A[i], A[min_idx])"
    ],
    info: {
      name: "Selection Sort",
      time_best: "O(n²)",
      time_avg: "O(n²)",
      time_worst: "O(n²)",
      space: "O(1)",
      description: "Divides list into sorted and unsorted portions; repeatedly finds minimum in unsorted part and moves it to sorted part.",
      analogy: "Scanning a bookshelf for the shortest book, placing it first, and repeating for the rest.",
      invariant: "A[0..i-1] contains the i smallest elements of A, in sorted order."
    },
    *run(arr) {
      const a = [...arr];
      const n = a.length;
      const sorted = [];

      for (let i = 0; i < n - 1; i++) {
        let min_idx = i;
        yield new AlgorithmStep({
          array: a,
          sorted_indices: sorted,
          pseudo_line: 3,
          pointers: { i, min: min_idx },
          status: `Assume A[${i}]=${a[i]} is minimum for now`
        });

        for (let j = i + 1; j < n; j++) {
          yield new AlgorithmStep({
            array: a,
            comparing: [j, min_idx],
            sorted_indices: sorted,
            pseudo_line: 5,
            pointers: { i, j, min: min_idx },
            status: `Checking if A[${j}]=${a[j]} < A[${min_idx}]=${a[min_idx]}`
          });

          if (a[j] < a[min_idx]) {
            min_idx = j;
            yield new AlgorithmStep({
              array: a,
              sorted_indices: sorted,
              pseudo_line: 6,
              pointers: { i, min: min_idx },
              status: `New minimum found: A[${min_idx}]=${a[min_idx]}`
            });
          }
        }

        if (min_idx !== i) {
          yield new AlgorithmStep({
            array: a,
            swapping: [i, min_idx],
            sorted_indices: sorted,
            pseudo_line: 7,
            pointers: { i, min: min_idx },
            status: `Swapping minimum ${a[min_idx]} into position ${i}`
          });
          const temp = a[i];
          a[i] = a[min_idx];
          a[min_idx] = temp;
        }

        sorted.push(i);
        yield new AlgorithmStep({
          array: a,
          sorted_indices: [...sorted],
          pseudo_line: 7,
          status: `Position ${i} finalized with value ${a[i]}`
        });
      }

      sorted.push(n - 1);
      yield new AlgorithmStep({
        array: a,
        sorted_indices: sorted,
        pseudo_line: 7,
        status: "Array fully sorted!"
      });
    }
  },

  "Merge Sort": {
    name: "Merge Sort",
    icon: "🔀",
    pseudo_code: [
      "procedure mergeSort(A, left, right)",
      "  if left < right then",
      "    mid := (left + right) / 2",
      "    mergeSort(A, left, mid)",
      "    mergeSort(A, mid + 1, right)",
      "    merge(A, left, mid, right)"
    ],
    info: {
      name: "Merge Sort",
      time_best: "O(n log n)",
      time_avg: "O(n log n)",
      time_worst: "O(n log n)",
      space: "O(n)",
      description: "Divide-and-conquer: recursively splits array in half, sorts each half, and merges sorted halves.",
      analogy: "Splitting a deck of cards into two halves, sorting each half, and zipping them back together in order.",
      invariant: "After merging, the subarray A[left..right] contains all original elements in sorted order."
    },
    *run(arr) {
      const a = [...arr];
      const sorted = [];

      function* merge(left, mid, right) {
        const leftArr = a.slice(left, mid + 1);
        const rightArr = a.slice(mid + 1, right + 1);
        let i = 0, j = 0, k = left;

        while (i < leftArr.length && j < rightArr.length) {
          yield new AlgorithmStep({
            array: a,
            comparing: [left + i, mid + 1 + j],
            sorted_indices: sorted,
            pseudo_line: 5,
            pointers: { low: left, mid, high: right },
            status: `Merging: comparing ${leftArr[i]} and ${rightArr[j]}`
          });

          if (leftArr[i] <= rightArr[j]) {
            a[k] = leftArr[i++];
          } else {
            a[k] = rightArr[j++];
          }

          yield new AlgorithmStep({
            array: a,
            swapping: [k],
            sorted_indices: sorted,
            pseudo_line: 5,
            status: `Placed ${a[k]} at position ${k}`
          });
          k++;
        }

        while (i < leftArr.length) {
          a[k] = leftArr[i++];
          yield new AlgorithmStep({ array: a, swapping: [k], sorted_indices: sorted, pseudo_line: 5 });
          k++;
        }
        while (j < rightArr.length) {
          a[k] = rightArr[j++];
          yield new AlgorithmStep({ array: a, swapping: [k], sorted_indices: sorted, pseudo_line: 5 });
          k++;
        }
      }

      function* sort(left, right) {
        if (left < right) {
          const mid = Math.floor((left + right) / 2);
          yield new AlgorithmStep({
            array: a,
            pseudo_line: 2,
            pointers: { low: left, mid, high: right },
            status: `Divide: [${left}..${mid}] and [${mid + 1}..${right}]`
          });
          yield* sort(left, mid);
          yield* sort(mid + 1, right);
          yield* merge(left, mid, right);
        }
      }

      yield* sort(0, a.length - 1);
      yield new AlgorithmStep({
        array: a,
        sorted_indices: Array.from({ length: a.length }, (_, k) => k),
        pseudo_line: 5,
        status: "Array fully sorted!"
      });
    }
  },

  "Quick Sort": {
    name: "Quick Sort",
    icon: "⚡",
    pseudo_code: [
      "procedure quickSort(A, low, high)",
      "  if low < high then",
      "    p := partition(A, low, high)",
      "    quickSort(A, low, p - 1)",
      "    quickSort(A, p + 1, high)",
      "",
      "function partition(A, low, high)",
      "  pivot := A[high]",
      "  i := low - 1",
      "  for j := low to high - 1 do",
      "    if A[j] < pivot then",
      "      i := i + 1; swap(A[i], A[j])",
      "  swap(A[i + 1], A[high])",
      "  return i + 1"
    ],
    info: {
      name: "Quick Sort",
      time_best: "O(n log n)",
      time_avg: "O(n log n)",
      time_worst: "O(n²)",
      space: "O(log n)",
      description: "Picks a pivot element, partitions array so smaller elements go left and larger right, then recurses.",
      analogy: "Organizing students by selecting one student as reference: shorter on left, taller on right.",
      invariant: "All elements left of pivot are <= pivot; all elements right of pivot are >= pivot."
    },
    *run(arr) {
      const a = [...arr];
      const sorted = [];

      function* partition(low, high) {
        const pivot = a[high];
        let i = low - 1;

        yield new AlgorithmStep({
          array: a,
          pivot_index: high,
          sorted_indices: sorted,
          pseudo_line: 7,
          pointers: { pivot: high, low, high },
          status: `Selected pivot = ${pivot} at index ${high}`
        });

        for (let j = low; j < high; j++) {
          yield new AlgorithmStep({
            array: a,
            comparing: [j, high],
            pivot_index: high,
            sorted_indices: sorted,
            pseudo_line: 10,
            pointers: { i: Math.max(low, i), j, pivot: high },
            status: `Comparing A[${j}]=${a[j]} against pivot ${pivot}`
          });

          if (a[j] < pivot) {
            i++;
            if (i !== j) {
              const temp = a[i];
              a[i] = a[j];
              a[j] = temp;

              yield new AlgorithmStep({
                array: a,
                swapping: [i, j],
                pivot_index: high,
                sorted_indices: sorted,
                pseudo_line: 11,
                pointers: { i, j, pivot: high },
                status: `Swapped ${a[i]} and ${a[j]}`
              });
            }
          }
        }

        const temp = a[i + 1];
        a[i + 1] = a[high];
        a[high] = temp;

        const p = i + 1;
        sorted.push(p);

        yield new AlgorithmStep({
          array: a,
          swapping: [p, high],
          pivot_index: p,
          sorted_indices: [...sorted],
          pseudo_line: 12,
          pointers: { pivot: p },
          status: `Pivot ${a[p]} placed in its final position index ${p}`
        });

        return p;
      }

      function* sort(low, high) {
        if (low < high) {
          const p = yield* partition(low, high);
          yield* sort(low, p - 1);
          yield* sort(p + 1, high);
        } else if (low === high && !sorted.includes(low)) {
          sorted.push(low);
        }
      }

      yield* sort(0, a.length - 1);
      yield new AlgorithmStep({
        array: a,
        sorted_indices: Array.from({ length: a.length }, (_, k) => k),
        pseudo_line: 13,
        status: "Array fully sorted!"
      });
    }
  }
};

// ─────────────────────────────────────────────────────────────────────────────
// Searching Algorithms
// ─────────────────────────────────────────────────────────────────────────────

export const SEARCHING_ALGORITHMS = {
  "Linear Search": {
    name: "Linear Search",
    icon: "🔍",
    pseudo_code: [
      "procedure linearSearch(A, target)",
      "  for i := 0 to length(A) - 1 do",
      "    if A[i] == target then",
      "      return i",
      "  return -1"
    ],
    info: {
      name: "Linear Search",
      time_best: "O(1)",
      time_avg: "O(n)",
      time_worst: "O(n)",
      space: "O(1)",
      description: "Sequentially inspects each element in array until target is found or end of array is reached.",
      analogy: "Flipping through a deck of cards one by one until finding the Ace of Spades.",
      invariant: "Target does not exist in A[0..i-1] after i failed probes."
    },
    *run(arr, target) {
      const a = [...arr];
      const eliminated = [];

      yield new AlgorithmStep({
        array: a,
        target,
        pseudo_line: 1,
        status: `Searching for target ${target}`
      });

      for (let i = 0; i < a.length; i++) {
        yield new AlgorithmStep({
          array: a,
          comparing: [i],
          eliminated_indices: [...eliminated],
          target,
          pointers: { i },
          pseudo_line: 2,
          status: `Checking A[${i}]=${a[i]} == target ${target}`
        });

        if (a[i] === target) {
          yield new AlgorithmStep({
            array: a,
            found_index: i,
            eliminated_indices: [...eliminated],
            target,
            pointers: { i },
            pseudo_line: 3,
            status: `Target ${target} found at index ${i}!`
          });
          return;
        }

        eliminated.push(i);
        yield new AlgorithmStep({
          array: a,
          eliminated_indices: [...eliminated],
          target,
          pseudo_line: 2,
          status: `A[${i}] != target. Eliminated index ${i}`
        });
      }

      yield new AlgorithmStep({
        array: a,
        eliminated_indices: [...eliminated],
        target,
        pseudo_line: 4,
        status: `Target ${target} not found in array.`
      });
    }
  },

  "Binary Search": {
    name: "Binary Search",
    icon: "⚡🔍",
    pseudo_code: [
      "procedure binarySearch(A, target)",
      "  low := 0; high := length(A) - 1",
      "  while low <= high do",
      "    mid := floor((low + high) / 2)",
      "    if A[mid] == target then",
      "      return mid",
      "    else if A[mid] < target then",
      "      low := mid + 1",
      "    else",
      "      high := mid - 1",
      "  return -1"
    ],
    info: {
      name: "Binary Search",
      time_best: "O(1)",
      time_avg: "O(log n)",
      time_worst: "O(log n)",
      space: "O(1)",
      description: "Search in a sorted array by repeatedly dividing the search interval in half.",
      analogy: "Opening a telephone dictionary right in the middle to look up a name.",
      invariant: "If target exists in A, it is strictly within A[low..high]."
    },
    *run(arr, target) {
      // Binary search requires sorted array
      const a = [...arr].sort((x, y) => x - y);
      let low = 0;
      let high = a.length - 1;
      const eliminated = [];

      yield new AlgorithmStep({
        array: a,
        range_low: low,
        range_high: high,
        target,
        pseudo_line: 1,
        status: `Starting Binary Search for ${target} in sorted array`
      });

      while (low <= high) {
        const mid = Math.floor((low + high) / 2);

        yield new AlgorithmStep({
          array: a,
          range_low: low,
          range_high: high,
          comparing: [mid],
          eliminated_indices: [...eliminated],
          target,
          pointers: { low, mid, high },
          pseudo_line: 3,
          status: `Testing midpoint A[${mid}]=${a[mid]} against target ${target}`
        });

        if (a[mid] === target) {
          yield new AlgorithmStep({
            array: a,
            found_index: mid,
            range_low: low,
            range_high: high,
            eliminated_indices: [...eliminated],
            target,
            pointers: { mid },
            pseudo_line: 5,
            status: `Target ${target} found at index ${mid}!`
          });
          return;
        } else if (a[mid] < target) {
          for (let k = low; k <= mid; k++) {
            if (!eliminated.includes(k)) eliminated.push(k);
          }
          low = mid + 1;
          yield new AlgorithmStep({
            array: a,
            range_low: low,
            range_high: high,
            eliminated_indices: [...eliminated],
            target,
            pointers: { low, high },
            pseudo_line: 7,
            status: `A[${mid}] < ${target}: discarded left half [${low - 1} and below]`
          });
        } else {
          for (let k = mid; k <= high; k++) {
            if (!eliminated.includes(k)) eliminated.push(k);
          }
          high = mid - 1;
          yield new AlgorithmStep({
            array: a,
            range_low: low,
            range_high: high,
            eliminated_indices: [...eliminated],
            target,
            pointers: { low, high },
            pseudo_line: 9,
            status: `A[${mid}] > ${target}: discarded right half [${mid} and above]`
          });
        }
      }

      yield new AlgorithmStep({
        array: a,
        eliminated_indices: Array.from({ length: a.length }, (_, k) => k),
        target,
        pseudo_line: 10,
        status: `Target ${target} not found in array.`
      });
    }
  }
};
