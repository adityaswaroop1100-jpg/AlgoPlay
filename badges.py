"""
badges.py - Achievements and Unlockable Badges for Story Mode.

Defines badge achievements, tracking conditions, and unlock evaluators.
Standard library only (dataclasses, typing).
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


@dataclass
class Badge:
    """
    Represents an unlockable achievement in Story Mode.

    Attributes:
        id: Unique identifier for progress persistence.
        name: Player-facing title.
        emoji: Visual icon badge.
        description: How the player earns this badge.
        unlock_condition: Callable taking GameState returning True when criteria met.
    """
    id: str
    name: str
    emoji: str
    description: str
    unlock_condition: Callable[[Any], bool]


BADGES: List[Badge] = [
    Badge(
        id="first_spark",
        name="First Spark",
        emoji="🌱",
        description="Make your very first correct algorithm prediction (+10 XP).",
        unlock_condition=lambda gs: gs.xp >= 10,
    ),
    Badge(
        id="streak_5",
        name="On a Roll",
        emoji="🔥",
        description="Achieve a prediction streak of 5 correct answers in a row.",
        unlock_condition=lambda gs: gs.best_streak >= 5,
    ),
    Badge(
        id="streak_10",
        name="Unstoppable",
        emoji="⚡",
        description="Achieve a prediction streak of 10 correct answers in a row.",
        unlock_condition=lambda gs: gs.best_streak >= 10,
    ),
    Badge(
        id="perfect_20",
        name="Perfect 20",
        emoji="✨",
        description="Achieve a legendary streak of 20 correct answers in a row.",
        unlock_condition=lambda gs: gs.best_streak >= 20,
    ),
    Badge(
        id="bubble_master",
        name="Bubble Master",
        emoji="🫧",
        description="Complete Chapter 1: Help Bubble Buddy bring order to the royal array.",
        unlock_condition=lambda gs: (
            "ch1_lvl3" in gs.completed_levels or
            gs.current_chapter not in ("ch1", "")
        ),
    ),
    Badge(
        id="card_shuffler",
        name="Card Shuffler",
        emoji="🃏",
        description="Complete Chapter 2: Master Insertion Sort with Insertion Iggy.",
        unlock_condition=lambda gs: (
            "ch2_lvl3" in gs.completed_levels or
            gs.current_chapter in ("ch3", "ch4", "ch5", "ch6", "ch7", "ch8")
        ),
    ),
    Badge(
        id="crown_finder",
        name="Crown Finder",
        emoji="👑",
        description="Complete Chapter 3: Locate true minimums with Selection Sia.",
        unlock_condition=lambda gs: (
            "ch3_lvl3" in gs.completed_levels or
            gs.current_chapter in ("ch4", "ch5", "ch6", "ch7", "ch8")
        ),
    ),
    Badge(
        id="divide_conqueror",
        name="Divide & Conqueror",
        emoji="🧩",
        description="Complete Chapter 4: Merge sub-problems seamlessly with Merge Mia.",
        unlock_condition=lambda gs: (
            "ch4_lvl3" in gs.completed_levels or
            gs.current_chapter in ("ch5", "ch6", "ch7", "ch8")
        ),
    ),
    Badge(
        id="speed_demon",
        name="Speed Demon",
        emoji="⚡",
        description="Complete Chapter 5: Partition like lightning with Quick Quinn.",
        unlock_condition=lambda gs: (
            "ch5_lvl3" in gs.completed_levels or
            gs.current_chapter in ("ch6", "ch7", "ch8")
        ),
    ),
    Badge(
        id="half_time_hero",
        name="Half-Time Hero",
        emoji="🤖",
        description="Complete Chapter 6: Cut search spaces in half with Binary Bot.",
        unlock_condition=lambda gs: (
            "ch6_lvl3" in gs.completed_levels or
            gs.current_chapter in ("ch7", "ch8")
        ),
    ),
    Badge(
        id="patient_pacer",
        name="Patient Pacer",
        emoji="🌙",
        description="Complete Chapter 7: Search through chaotic data with Linear Luna.",
        unlock_condition=lambda gs: (
            "ch7_lvl3" in gs.completed_levels or
            gs.current_chapter == "ch8"
        ),
    ),
    Badge(
        id="grand_architect",
        name="Grand Architect",
        emoji="🏆",
        description="Complete all 8 Chapters of Story Mode!",
        unlock_condition=lambda gs: (
            "ch8_boss" in gs.completed_levels or
            len(gs.completed_levels) >= 16
        ),
    ),
    Badge(
        id="century_club",
        name="Century Club",
        emoji="💯",
        description="Accumulate 500 total XP through predictions and level clears.",
        unlock_condition=lambda gs: gs.xp >= 500,
    ),
    Badge(
        id="algorithm_sage",
        name="Algorithm Sage",
        emoji="🧙‍♂️",
        description="Reach Level 10 (earn 1,000+ total XP).",
        unlock_condition=lambda gs: gs.level >= 10,
    ),
]


_BADGE_MAP: Dict[str, Badge] = {b.id: b for b in BADGES}


def get_badge_by_id(badge_id: str) -> Optional[Badge]:
    """Retrieve a badge definition by its identifier string."""
    return _BADGE_MAP.get(badge_id)


def check_and_unlock(gs: Any) -> List[str]:
    """
    Evaluate all registered badges against current player state.
    Adds newly unlocked badge IDs to gs.badges and returns list of new unlocks.
    """
    newly_unlocked: List[str] = []
    current_badges = set(getattr(gs, "badges", []))

    for badge in BADGES:
        if badge.id not in current_badges:
            try:
                if badge.unlock_condition(gs):
                    gs.badges.append(badge.id)
                    current_badges.add(badge.id)
                    newly_unlocked.append(badge.id)
            except Exception:
                pass

    return newly_unlocked
