"""
algorithm_base.py - Abstract Base Class and State Protocol for Algorithms.

Implements the Strategy Pattern foundation for sorting and searching algorithms,
defining algorithm metadata, complexity metrics, pseudo-code definitions,
and step-by-step generator protocols.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Generator, Iterator, List, Optional, Sequence, Set, Union


@dataclass
class AlgorithmStep:
    """
    Represents an immutable snapshot of an algorithm's state at a single step.
    
    Can be unpacked directly as a 6-tuple:
      (array_snapshot, indices_being_compared, indices_being_swapped,
       sorted_indices, pivot_index, current_pseudo_line)
    while also providing extended fields for searching and variable inspection.
    """
    array: List[int]
    comparing: List[int] = field(default_factory=list)
    swapping: List[int] = field(default_factory=list)
    sorted_indices: List[int] = field(default_factory=list)
    pivot_index: Optional[int] = None
    pseudo_line: int = -1
    
    # Extended context fields
    status: str = ""
    variables: Dict[str, Any] = field(default_factory=dict)
    eliminated_indices: List[int] = field(default_factory=list)
    found_index: Optional[int] = None
    target_value: Optional[int] = None
    pointers: Dict[str, int] = field(default_factory=dict)
    range_low: int = -1
    range_high: int = -1

    # NEW fields for Story Mode
    question: str = ""
    options: List[str] = field(default_factory=list)
    correct_index: int = -1
    explanation: str = ""
    hint: str = ""
    invariant: str = ""
    action: str = "none"

    def __iter__(self) -> Iterator[Any]:
        """
        Enables seamless 6-tuple unpacking:
        arr, comp, swap, sorted_idx, pivot, line = step
        """
        yield self.array
        yield self.comparing
        yield self.swapping
        yield self.sorted_indices
        yield self.pivot_index
        yield self.pseudo_line


class AlgorithmBase(ABC):
    """
    Abstract Strategy class that every sorting and searching algorithm subclasses.
    
    Encapsulates theoretical complexity metrics, educational analogies,
    algorithmic pseudo-code lines, and the step-generator contract.
    """

    def __init__(
        self,
        name: str,
        category: str,
        time_best: str,
        time_avg: str,
        time_worst: str,
        space_complexity: str,
        description: str,
        analogy: str,
        pseudo_code: List[str]
    ) -> None:
        """Initialize algorithm metadata and pedagogical specifications."""
        self.name: str = name
        self.category: str = category  # "sorting" or "searching"
        self.time_best: str = time_best
        self.time_avg: str = time_avg
        self.time_worst: str = time_worst
        self.space_complexity: str = space_complexity
        self.description: str = description
        self.analogy: str = analogy
        self.pseudo_code: List[str] = pseudo_code

    @abstractmethod
    def run(self, data: List[int], **kwargs: Any) -> Generator[AlgorithmStep, None, None]:
        """
        Generator driving the algorithm step-by-step.
        
        Yields an AlgorithmStep at each key decision or state modification point.
        Does NOT block the main UI thread.
        """
        raise NotImplementedError("Subclasses must implement the step-by-step generator.")

    def get_info(self) -> Dict[str, str]:
        """Return a structured dictionary of complexity and educational metadata."""
        return {
            "name": self.name,
            "category": self.category,
            "best": self.time_best,
            "average": self.time_avg,
            "worst": self.time_worst,
            "space": self.space_complexity,
            "description": self.description,
            "analogy": self.analogy,
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"


# Convenient alias matching Story Mode step conventions
Step = AlgorithmStep
