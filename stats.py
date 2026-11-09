"""
stats.py - Metrics Tracking and Variable Watch Engine for AlgoPlay.

Maintains execution statistics (comparisons, swaps, elapsed time, status messages)
and runtime variable states for live inspection during algorithm visualization
and race modes.
"""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class VariableState:
    """Stores key algorithm variables for the Variable Watch panel."""
    variables: Dict[str, Any] = field(default_factory=dict)

    def update(self, **kwargs: Any) -> None:
        """Update or insert variable key-value pairs."""
        for key, val in kwargs.items():
            if val is not None:
                self.variables[key] = val
            elif key in self.variables:
                del self.variables[key]

    def clear(self) -> None:
        """Clear all active variables."""
        self.variables.clear()

    def get_formatted_pairs(self) -> Dict[str, str]:
        """Return formatted string representations for UI display."""
        return {k: str(v) for k, v in self.variables.items()}


class StatsTracker:
    """
    Tracks comparisons, swaps, runtime duration, status explanations,
    and variable values for an active algorithm run.
    """

    def __init__(self, name: str = "Algorithm") -> None:
        """Initialize tracker with zeroed metrics."""
        self.name: str = name
        self.comparisons: int = 0
        self.swaps: int = 0
        self.array_accesses: int = 0
        
        # Timing
        self._start_time: Optional[float] = None
        self._elapsed_offset: float = 0.0
        self._is_running: bool = False
        self._is_paused: bool = False
        self._pause_time: Optional[float] = None
        
        # Status and Variables
        self.status_message: str = "Ready"
        self.variables: VariableState = VariableState()

    def start(self) -> None:
        """Start or restart the performance timer."""
        self._start_time = time.perf_counter()
        self._elapsed_offset = 0.0
        self._is_running = True
        self._is_paused = False
        self.status_message = "Running..."

    def pause(self) -> None:
        """Pause the performance timer."""
        if self._is_running and not self._is_paused:
            self._pause_time = time.perf_counter()
            self._is_paused = True
            if self._start_time is not None:
                self._elapsed_offset += self._pause_time - self._start_time
            self.status_message = "Paused"

    def resume(self) -> None:
        """Resume timing after being paused."""
        if self._is_running and self._is_paused:
            self._start_time = time.perf_counter()
            self._is_paused = False
            self.status_message = "Running..."

    def stop(self, final_status: str = "Completed") -> None:
        """Stop timing upon algorithm completion."""
        if self._is_running and not self._is_paused:
            if self._start_time is not None:
                self._elapsed_offset += time.perf_counter() - self._start_time
        self._is_running = False
        self._is_paused = False
        self.status_message = final_status

    def reset(self) -> None:
        """Reset all metrics back to initial zero states."""
        self.comparisons = 0
        self.swaps = 0
        self.array_accesses = 0
        self._start_time = None
        self._elapsed_offset = 0.0
        self._is_running = False
        self._is_paused = False
        self._pause_time = None
        self.status_message = "Ready"
        self.variables.clear()

    def increment_comparisons(self, count: int = 1) -> None:
        """Increment comparison count."""
        self.comparisons += count

    def increment_swaps(self, count: int = 1) -> None:
        """Increment swap count."""
        self.swaps += count

    def increment_accesses(self, count: int = 1) -> None:
        """Increment array access count."""
        self.array_accesses += count

    def set_status(self, message: str) -> None:
        """Update current status description."""
        self.status_message = message

    def update_variables(self, **kwargs: Any) -> None:
        """Update active variables for the Variable Watch panel."""
        self.variables.update(**kwargs)

    @property
    def elapsed_time(self) -> float:
        """Calculate and return total elapsed execution time in seconds."""
        if not self._is_running:
            return self._elapsed_offset
        if self._is_paused:
            return self._elapsed_offset
        if self._start_time is None:
            return self._elapsed_offset
        return self._elapsed_offset + (time.perf_counter() - self._start_time)

    @property
    def formatted_time(self) -> str:
        """Return human-readable elapsed time string with ms precision."""
        seconds = self.elapsed_time
        if seconds < 1.0:
            return f"{seconds * 1000:.1f} ms"
        return f"{seconds:.2f} s"

    def get_summary(self) -> Dict[str, Any]:
        """Return a dictionary snapshot of current metrics."""
        return {
            "name": self.name,
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "array_accesses": self.array_accesses,
            "elapsed_time": self.elapsed_time,
            "formatted_time": self.formatted_time,
            "status": self.status_message,
            "variables": self.variables.get_formatted_pairs(),
        }
