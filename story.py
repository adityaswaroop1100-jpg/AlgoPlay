"""
story.py - Story Mode Chapters, Levels, and Narrative Content.

Contains 8 narrative chapters featuring companion mascots, array challenges,
and boss encounters. Standard library only (dataclasses, typing).
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Chapter:
    """
    Narrative chapter teaching an algorithmic concept through story challenges.

    Attributes:
        id: Unique chapter identifier (e.g. 'ch1').
        title: Player-facing chapter name.
        mascot_key: Associated mascot identifier in mascots.py.
        intro_text: Story briefing when player opens the chapter.
        algorithm: Associated algorithm title (e.g. 'Bubble Sort').
        levels: List of challenge level dictionaries.
        outro_text: Celebratory story conclusion upon chapter completion.
    """
    id: str
    title: str
    mascot_key: str
    intro_text: str
    algorithm: str
    levels: List[Dict[str, Any]]
    outro_text: str


CHAPTERS: List[Chapter] = [
    Chapter(
        id="ch1",
        title="Chapter 1: The Chaos Begins",
        mascot_key="bubble",
        intro_text=(
            "The Kingdom's vault of numbers has been scrambled by a mischievous storm! "
            "Bubble Buddy bounces into action to teach you how adjacent bubbles float the largest values rightward."
        ),
        algorithm="Bubble Sort",
        levels=[
            {"id": "ch1_lvl1", "title": "Warm-Up Bubbles", "array": [5, 3, 8, 1, 9], "goal": "Sort the 5 numbers", "xp_reward": 100, "is_boss": False},
            {"id": "ch1_lvl2", "title": "Twice Scrambled", "array": [7, 4, 9, 2, 6, 1], "goal": "Float bigger numbers right", "xp_reward": 120, "is_boss": False},
            {"id": "ch1_lvl3", "title": "Boss: The Boiling Cauldron", "array": [9, 8, 7, 6, 5, 4, 3, 2], "goal": "Overcome the worst-case reverse array!", "xp_reward": 250, "is_boss": True},
        ],
        outro_text="🫧 Incredible work! Bubble Buddy bubbles with joy as the vault settles into tranquil harmony!",
    ),

    Chapter(
        id="ch2",
        title="Chapter 2: The Royal Library",
        mascot_key="insertion",
        intro_text=(
            "The ancient scrolls and card decks in the Royal Library are scattered across the floor! "
            "Insertion Iggy arrives with a tidy plan: take one item at a time and insert it where it belongs."
        ),
        algorithm="Insertion Sort",
        levels=[
            {"id": "ch2_lvl1", "title": "Dealing the Hand", "array": [6, 2, 8, 4, 1], "goal": "Insert each key into sorted hand", "xp_reward": 100, "is_boss": False},
            {"id": "ch2_lvl2", "title": "Shelving Folios", "array": [12, 5, 18, 9, 3, 7], "goal": "Slide books into proper shelf order", "xp_reward": 130, "is_boss": False},
            {"id": "ch2_lvl3", "title": "Boss: The Grand Archive", "array": [15, 13, 11, 9, 7, 5, 3, 1], "goal": "Sort the reversed library catalogue!", "xp_reward": 250, "is_boss": True},
        ],
        outro_text="🃏 Splendid precision! Every tome is neatly filed, and Iggy presents you with the Card Shuffler badge!",
    ),

    Chapter(
        id="ch3",
        title="Chapter 3: The Crown Jewels",
        mascot_key="selection",
        intro_text=(
            "The Queen's prized gemstone collection has been mixed up in royal banquet trays! "
            "Selection Sia will guide you to survey every jewel and place the true minimum in order, one by one."
        ),
        algorithm="Selection Sort",
        levels=[
            {"id": "ch3_lvl1", "title": "Emerald Inspection", "array": [29, 10, 14, 37, 13], "goal": "Select and place smallest gems", "xp_reward": 100, "is_boss": False},
            {"id": "ch3_lvl2", "title": "Diamond Chamber", "array": [45, 12, 88, 23, 5, 67], "goal": "Scan thoroughly before swapping", "xp_reward": 130, "is_boss": False},
            {"id": "ch3_lvl3", "title": "Boss: The Royal Treasury", "array": [99, 81, 63, 45, 36, 27, 18], "goal": "Crown every minimum in minimum swaps!", "xp_reward": 250, "is_boss": True},
        ],
        outro_text="👑 Long live the strategist! Sia bows with royal grace as the treasury sparkles in pristine order!",
    ),

    Chapter(
        id="ch4",
        title="Chapter 4: The Grand Tournament",
        mascot_key="merge",
        intro_text=(
            "Contenders from across the land have arrived for the Kingdom's sorting tournament! "
            "Merge Mia demonstrates the wisdom of Divide & Conquer: break large problems down, then merge solutions."
        ),
        algorithm="Merge Sort",
        levels=[
            {"id": "ch4_lvl1", "title": "Quarter-Finals", "array": [38, 27, 43, 3, 9, 82], "goal": "Divide into halves and merge in sync", "xp_reward": 120, "is_boss": False},
            {"id": "ch4_lvl2", "title": "Semi-Finals", "array": [50, 20, 40, 10, 60, 30, 70], "goal": "Coordinate sub-array merges", "xp_reward": 150, "is_boss": False},
            {"id": "ch4_lvl3", "title": "Boss: The Arena Finals", "array": [64, 34, 25, 12, 22, 11, 90, 80], "goal": "Achieve O(n log n) championship victory!", "xp_reward": 300, "is_boss": True},
        ],
        outro_text="🧩 A masterclass in unity! Mia cheers as both halves unite into a harmonious, unbroken sequence!",
    ),

    Chapter(
        id="ch5",
        title="Chapter 5: Lightning Peak",
        mascot_key="quick",
        intro_text=(
            "High atop the tempestuous Lightning Peak, thunderbolts split the sky! "
            "Quick Quinn charges in to teach high-velocity partitioning around a referee pivot."
        ),
        algorithm="Quick Sort",
        levels=[
            {"id": "ch5_lvl1", "title": "First Spark", "array": [10, 80, 30, 90, 40, 50], "goal": "Partition smaller left, larger right", "xp_reward": 120, "is_boss": False},
            {"id": "ch5_lvl2", "title": "Thunder Ridge", "array": [24, 9, 29, 14, 39, 19], "goal": "Master pivot placement at speed", "xp_reward": 150, "is_boss": False},
            {"id": "ch5_lvl3", "title": "Boss: The Supercell Tempest", "array": [88, 12, 74, 31, 95, 23, 67, 42], "goal": "Conquer the storm at lightning speed!", "xp_reward": 300, "is_boss": True},
        ],
        outro_text="⚡ Sonic boom! Quinn gives a high-voltage salute as the mountain path is cleared in record time!",
    ),

    Chapter(
        id="ch6",
        title="Chapter 6: The Secret Archives",
        mascot_key="binary",
        intro_text=(
            "Deep within the royal cyber-vault, millions of entries are catalogued in order. "
            "Binary Bot boots up to demonstrate how cutting the search interval in half discovers any target in record time."
        ),
        algorithm="Binary Search",
        levels=[
            {"id": "ch6_lvl1", "title": "Access Protocol", "array": [10, 20, 30, 40, 50, 60, 70], "target": 50, "goal": "Find 50 by halving the space", "xp_reward": 120, "is_boss": False},
            {"id": "ch6_lvl2", "title": "Security Check", "array": [11, 22, 33, 44, 55, 66, 77, 88], "target": 22, "goal": "Locate 22 in sorted data", "xp_reward": 150, "is_boss": False},
            {"id": "ch6_lvl3", "title": "Boss: The Mainframe Core", "array": [4, 8, 15, 16, 23, 42, 58, 64, 79, 91], "target": 42, "goal": "Pinpoint target 42 in minimum probes!", "xp_reward": 300, "is_boss": True},
        ],
        outro_text="🤖 TASK COMPLETE. Logarithmic efficiency verified. Binary Bot awards you the Half-Time Hero commendation!",
    ),

    Chapter(
        id="ch7",
        title="Chapter 7: The Whispering Forest",
        mascot_key="linear",
        intro_text=(
            "Night has fallen over the enchanted Whispering Forest, where numbers roam in total disarray! "
            "Linear Luna guides you with starlight patience: when data has no order, step by step is the only true way."
        ),
        algorithm="Linear Search",
        levels=[
            {"id": "ch7_lvl1", "title": "Starlit Path", "array": [42, 17, 89, 33, 56], "target": 33, "goal": "Find 33 in scrambled forest data", "xp_reward": 100, "is_boss": False},
            {"id": "ch7_lvl2", "title": "Hidden Glade", "array": [91, 14, 68, 25, 77, 43], "target": 25, "goal": "Locate 25 step by patient step", "xp_reward": 130, "is_boss": False},
            {"id": "ch7_lvl3", "title": "Boss: Midnight Labyrinth", "array": [60, 22, 93, 11, 49, 78, 35, 84], "target": 84, "goal": "Walk the labyrinth to discover 84!", "xp_reward": 250, "is_boss": True},
        ],
        outro_text="🌙 The moon beams warmly upon your journey. Luna whispers that patience and perseverance conquer all unknowns.",
    ),

    Chapter(
        id="ch8",
        title="Chapter 8: The Grand Master's Trial",
        mascot_key="quick",
        intro_text=(
            "The High Council of Algorithms summons you to the summit of computational mastery! "
            "All seven mascots assemble to cheer you on as you face the ultimate array challenges."
        ),
        algorithm="Quick Sort",
        levels=[
            {"id": "ch8_lvl1", "title": "Council's Gambit", "array": [35, 12, 78, 44, 91, 23, 67], "goal": "Prove mastery of algorithm flow", "xp_reward": 180, "is_boss": False},
            {"id": "ch8_lvl2", "title": "Dual Dimension", "array": [85, 24, 63, 45, 17, 31, 96, 52], "goal": "Sort the Council's master array", "xp_reward": 220, "is_boss": False},
            {"id": "ch8_boss", "title": "FINAL BOSS: The Grand Matrix", "array": [98, 45, 12, 87, 34, 65, 23, 76, 54, 89], "goal": "Achieve total algorithmic enlightenment!", "xp_reward": 500, "is_boss": True},
        ],
        outro_text="🏆 STAND PROUD, GRAND ARCHITECT! The entire kingdom of AlgoPlay hails you as the Supreme Master of Algorithms!",
    ),
]


_CHAPTER_MAP: Dict[str, Chapter] = {c.id: c for c in CHAPTERS}


def get_chapter(chapter_id: str) -> Optional[Chapter]:
    """Retrieve chapter metadata by identifier (e.g. 'ch1')."""
    return _CHAPTER_MAP.get(chapter_id)


def get_level(chapter_id: str, level_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve level configuration dictionary by chapter and level IDs."""
    chap = get_chapter(chapter_id)
    if not chap:
        return None
    for lvl in chap.levels:
        if lvl["id"] == level_id:
            return lvl
    return None


def get_next_level(chapter_id: str, level_id: str) -> Optional[Tuple[str, str]]:
    """
    Determine the next level in progression.
    Returns (next_chapter_id, next_level_id) or None if completed all.
    """
    chap = get_chapter(chapter_id)
    if not chap:
        return None

    # Check for next level in current chapter
    for i, lvl in enumerate(chap.levels):
        if lvl["id"] == level_id and i + 1 < len(chap.levels):
            return chapter_id, chap.levels[i + 1]["id"]

    # Current chapter finished -> advance to next chapter's first level
    for i, c in enumerate(CHAPTERS):
        if c.id == chapter_id and i + 1 < len(CHAPTERS):
            next_chap = CHAPTERS[i + 1]
            if next_chap.levels:
                return next_chap.id, next_chap.levels[0]["id"]

    return None
