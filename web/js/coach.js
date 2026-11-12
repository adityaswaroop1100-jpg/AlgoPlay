// coach.js - Step-by-Step Explainer, "Why?" Invariant Guide & Complexity Display

export class CoachPanel {
  constructor(container) {
    this.container = container;
    this.whyOpen = false;
    this.currentStep = null;
    this.currentAlgo = "";
  }

  update(algoName, step, info) {
    this.currentAlgo = algoName;
    this.currentStep = step;

    const phaseEl = this.container.querySelector("#coach-phase");
    const titleEl = this.container.querySelector("#coach-title");
    const descEl = this.container.querySelector("#coach-desc");
    const whyContentEl = this.container.querySelector("#coach-why-content");

    const explanation = this.getExplanation(algoName, step);

    if (phaseEl) phaseEl.textContent = explanation.phase;
    if (titleEl) titleEl.textContent = explanation.title;
    if (descEl) descEl.textContent = explanation.desc;
    if (whyContentEl) whyContentEl.textContent = info?.invariant || explanation.why;
  }

  getExplanation(algo, step) {
    const isSwp = step.swapping?.length > 0;
    const isCmp = step.comparing?.length > 0;
    const isFound = step.found_index !== null;

    if (algo === "Bubble Sort") {
      if (isSwp) {
        return {
          phase: "Step 3 of 4: Swap",
          title: "Swap Out-of-Order Adjacent Pair",
          desc: `Swapping ${step.array[step.swapping[0]]} and ${step.array[step.swapping[1]]}. The larger element bubbles rightward toward the sorted partition.`,
          why: "Bubble Sort maintains the invariant that after pass i, the i largest elements reside in their final sorted positions at the right end."
        };
      }
      if (isCmp) {
        return {
          phase: "Step 2 of 4: Compare",
          title: "Compare Adjacent Elements",
          desc: `Comparing adjacent values A[${step.comparing[0]}] and A[${step.comparing[1]}]. If the left element is greater, they must be swapped.`,
          why: "Adjacent comparisons allow local inversions to resolve, pushing larger values toward the end of the array."
        };
      }
      return {
        phase: "Step 1 of 4: Scan",
        title: "Scanning Array",
        desc: "Traversing adjacent elements to identify out-of-order pairs.",
        why: "A full pass without swaps indicates that the entire array is sorted (early exit optimization)."
      };
    }

    if (algo === "Insertion Sort") {
      if (isSwp) {
        return {
          phase: "Step 3 of 4: Shift",
          title: "Shift Larger Element Rightward",
          desc: "Shifting element to the right to open an insertion slot for the active key.",
          why: "By shifting larger elements, we preserve space for the key while keeping the prefix sorted."
        };
      }
      if (isCmp) {
        return {
          phase: "Step 2 of 4: Compare",
          title: "Compare Key Against Sorted Prefix",
          desc: "Comparing the active key against sorted prefix elements to pinpoint its insertion slot.",
          why: "The prefix A[0..i-1] is always kept in strictly sorted order."
        };
      }
      return {
        phase: "Step 1 of 4: Select Key",
        title: "Pick Next Unsorted Element",
        desc: "Selecting the next element from the unsorted section to insert into the sorted prefix.",
        why: "Like sorting cards in hand, each new item slides into its correct relative spot."
      };
    }

    if (algo === "Selection Sort") {
      if (isSwp) {
        return {
          phase: "Step 3 of 3: Swap",
          title: "Place Minimum in Final Position",
          desc: "Swapping the identified minimum value into the next available slot in the sorted prefix.",
          why: "Guarantees that each slot from 0 to n-1 receives its final sorted value with at most n-1 swaps."
        };
      }
      if (isCmp) {
        return {
          phase: "Step 2 of 3: Scan",
          title: "Compare Candidate With Running Minimum",
          desc: "Scanning unsorted elements to see if any value is smaller than our current minimum.",
          why: "Selection Sort requires inspecting all remaining items to ensure the true minimum is found."
        };
      }
      return {
        phase: "Step 1 of 3: Initialize",
        title: "Initialize Minimum Pointer",
        desc: "Setting current index as assumed minimum before scanning the remaining unsorted subarray.",
        why: "Prefix A[0..i] holds the i smallest elements in the array in sorted order."
      };
    }

    if (algo === "Quick Sort") {
      if (step.pivot_index !== null) {
        return {
          phase: "Partitioning",
          title: "Partition Around Pivot",
          desc: `Active pivot at index ${step.pivot_index}. Smaller elements move left; larger move right.`,
          why: "Once partitioned, the pivot element never moves again; subproblems to the left and right can be solved independently."
        };
      }
      return {
        phase: "Divide & Conquer",
        title: "Recursive Subproblem",
        desc: "Dividing array into smaller partitions around the pivot.",
        why: "Divide-and-conquer achieves O(n log n) average time by dividing problem depth logarithmically."
      };
    }

    if (algo === "Merge Sort") {
      return {
        phase: "Merge Phase",
        title: "Combine Sorted Subarrays",
        desc: "Comparing leading elements from two sorted halves and writing the smaller one back in order.",
        why: "Merging two already-sorted arrays takes linear O(n) time, guaranteeing overall O(n log n) runtime."
      };
    }

    if (algo === "Binary Search") {
      if (isFound) {
        return {
          phase: "Target Found",
          title: "Match Confirmed",
          desc: `Target matched at index ${step.found_index}!`,
          why: "Binary search locates elements in O(log n) time by eliminating half of the search space per probe."
        };
      }
      if (isCmp) {
        return {
          phase: "Probe Midpoint",
          title: "Compare Midpoint Against Target",
          desc: `Testing middle element against target. If smaller, discard left; if larger, discard right.`,
          why: "Because the array is sorted, comparing against the midpoint eliminates half of the remaining elements."
        };
      }
      return {
        phase: "Range Update",
        title: "Halve Search Interval",
        desc: `Updated active range to [${step.range_low} … ${step.range_high}].`,
        why: "Each probe halves the search space: N -> N/2 -> N/4 -> ... -> 1 in at most log2(N) steps."
      };
    }

    if (algo === "Linear Search") {
      if (isFound) {
        return {
          phase: "Match Found",
          title: "Target Located",
          desc: `Target found at index ${step.found_index}!`,
          why: "Linear search checks items sequentially; worst-case requires scanning all N elements."
        };
      }
      return {
        phase: "Sequential Probe",
        title: "Inspect Next Element",
        desc: "Checking current candidate against target.",
        why: "Works on unsorted arrays without requiring pre-sorting."
      };
    }

    return {
      phase: "Executing",
      title: algo,
      desc: step.status || "Algorithm executing step...",
      why: "Maintaining algorithm invariants to achieve sorted or searched order."
    };
  }
}
