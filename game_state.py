"""
game_state.py - Persistent Game State, XP, Streak, and Progression for Story Mode.

Manages player experience points, answering streaks, level completion,
unlocked achievements/badges, and auto-saves progress to saves/progress.json.
Standard library only (json, os, time, dataclasses, typing).
"""

from dataclasses import asdict, dataclass, field
import json
import os
import time
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class GameState:
    """
    Tracks and persists the player's Story Mode progression.

    Attributes:
        xp: Total experience points earned.
        streak: Current count of consecutive correct predictions.
        best_streak: Highest streak achieved across all sessions.
        current_chapter: Identifier of the active chapter (e.g., 'ch1').
        current_level: Identifier of the active level (e.g., 'ch1_lvl1').
        completed_levels: List of level IDs that have been cleared.
        badges: List of unlocked badge identifier strings.
        last_played_date: ISO date string of the last recorded interaction.
        level_mistakes: Mistakes made in the current level (for perfect run bonuses).
        consecutive_wrongs: Tracks repeated errors to trigger mascot coaching.
    """
    xp: int = 0
    streak: int = 0
    best_streak: int = 0
    current_chapter: str = "ch1"
    current_level: str = "ch1_lvl1"
    completed_levels: List[str] = field(default_factory=list)
    badges: List[str] = field(default_factory=list)
    last_played_date: str = ""
    level_mistakes: int = 0
    consecutive_wrongs: int = 0

    @property
    def level(self) -> int:
        """Calculate player level based on total XP (every 100 XP is 1 level)."""
        return max(1, (self.xp // 100) + 1)

    @property
    def xp_in_level(self) -> int:
        """XP accumulated towards the next level threshold."""
        return self.xp % 100

    def add_xp(self, amount: int) -> int:
        """Add positive XP to the player's total and return new total."""
        if amount > 0:
            self.xp += amount
        return self.xp

    def correct_answer(self) -> Tuple[int, int]:
        """
        Record a correct prediction: +10 XP, increment streak, update best streak.
        Returns:
            Tuple of (xp_awarded, current_streak)
        """
        xp_gain = 10
        self.streak += 1
        if self.streak > self.best_streak:
            self.best_streak = self.streak
        self.consecutive_wrongs = 0
        self.add_xp(xp_gain)
        self.last_played_date = time.strftime("%Y-%m-%d %H:%M:%S")
        self.check_badges()
        return xp_gain, self.streak

    def wrong_answer(self) -> Tuple[int, int]:
        """
        Record an incorrect prediction: +2 XP consolation, reset streak.
        Returns:
            Tuple of (xp_awarded, consecutive_wrongs)
        """
        xp_gain = 2
        self.streak = 0
        self.level_mistakes += 1
        self.consecutive_wrongs += 1
        self.add_xp(xp_gain)
        self.last_played_date = time.strftime("%Y-%m-%d %H:%M:%S")
        self.check_badges()
        return xp_gain, self.consecutive_wrongs

    def use_hint(self) -> int:
        """Deduct 5 XP (floor at 0) for consulting the mascot hint."""
        cost = min(5, self.xp)
        self.xp -= cost
        return cost

    def complete_level(self, level_id: str, is_boss: bool = False, base_reward: int = 100) -> int:
        """
        Process level completion bonuses and mark as cleared.

        Bonuses:
            - base_reward: Standard chapter level reward (default 100 XP)
            - Perfect run (0 wrong in level): +50 XP bonus
            - Boss level: +100 XP extra bonus
        """
        earned = base_reward
        if self.level_mistakes == 0:
            earned += 50
        if is_boss:
            earned += 100

        self.add_xp(earned)
        if level_id not in self.completed_levels:
            self.completed_levels.append(level_id)

        self.level_mistakes = 0
        self.consecutive_wrongs = 0
        self.check_badges()
        self.save()
        return earned

    def check_badges(self) -> List[str]:
        """Check all badge rules against current state and return newly unlocked IDs."""
        try:
            from badges import check_and_unlock
            new_badges = check_and_unlock(self)
            return new_badges
        except ImportError:
            return []

    def _get_default_save_path(self) -> str:
        """Resolve canonical path to saves/progress.json in AlgoPlay directory."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(base_dir, "saves")
        os.makedirs(save_dir, exist_ok=True)
        return os.path.join(save_dir, "progress.json")

    def save(self, filepath: Optional[str] = None) -> bool:
        """
        Serialize game state to JSON on disk.
        Returns True on success, False if file writing encounters an error.
        """
        target = filepath or self._get_default_save_path()
        try:
            dir_name = os.path.dirname(target)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            data = asdict(self)
            with open(target, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False

    def load(self, filepath: Optional[str] = None) -> bool:
        """
        Load player progress from JSON file. Initializes defaults if missing.
        """
        target = filepath or self._get_default_save_path()
        if not os.path.exists(target):
            self.save(target)
            return False

        try:
            with open(target, "r", encoding="utf-8") as f:
                data: Dict[str, Any] = json.load(f)
            self.xp = int(data.get("xp", 0))
            self.streak = int(data.get("streak", 0))
            self.best_streak = int(data.get("best_streak", 0))
            self.current_chapter = str(data.get("current_chapter", "ch1"))
            self.current_level = str(data.get("current_level", "ch1_lvl1"))
            self.completed_levels = list(data.get("completed_levels", []))
            self.badges = list(data.get("badges", []))
            self.last_played_date = str(data.get("last_played_date", ""))
            self.level_mistakes = int(data.get("level_mistakes", 0))
            self.consecutive_wrongs = int(data.get("consecutive_wrongs", 0))
            return True
        except Exception:
            return False

    def reset(self) -> None:
        """Reset player progress back to day 1 defaults."""
        self.xp = 0
        self.streak = 0
        self.best_streak = 0
        self.current_chapter = "ch1"
        self.current_level = "ch1_lvl1"
        self.completed_levels = []
        self.badges = []
        self.last_played_date = ""
        self.level_mistakes = 0
        self.consecutive_wrongs = 0
        self.save()
