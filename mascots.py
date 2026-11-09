"""
mascots.py - Mascot Characters, Dynamic Speech, and Personalities for Story Mode.

Defines 7 algorithm companion mascots with unique voices, contextual reactions,
streaks, hints, and dynamic state-based facial expressions.
Standard library only (dataclasses, random, typing).
"""

from dataclasses import dataclass, field
import random
from typing import Dict, List, Optional


@dataclass
class Mascot:
    """
    Algorithm companion character with unique dialogue style and reactions.

    Attributes:
        name: Mascot character name (e.g. 'Bubble Buddy').
        emoji: Mascot avatar emoji.
        color: Primary accent hex color for speech bubble borders and badges.
        catchphrase: Signature character motto.
        intro_line: Opening dialogue when a level begins.
        win_line: Celebratory dialogue on level clear.
        reaction_correct: List of 5+ praise lines on correct predictions.
        reaction_wrong: List of 5+ encouraging correction lines.
        reaction_streak: Milestone praise for streaks at 5, 10, 20.
        hint_style: Mascot prefix tag for hints.
    """
    name: str
    emoji: str
    color: str
    catchphrase: str
    intro_line: str
    win_line: str
    reaction_correct: List[str]
    reaction_wrong: List[str]
    reaction_streak: Dict[int, str]
    hint_style: str = "💡"

    def get_reaction(self, kind: str) -> str:
        """Return a random contextual response line ('correct' or 'wrong')."""
        if kind == "correct" and self.reaction_correct:
            return random.choice(self.reaction_correct)
        if kind == "wrong" and self.reaction_wrong:
            return random.choice(self.reaction_wrong)
        return self.catchphrase

    def get_expression(self, state: str) -> str:
        """Return character emoji adapted for current emotion."""
        if state == "thinking":
            return f"{self.emoji} 🤔"
        if state == "happy":
            return f"{self.emoji} ✨"
        if state == "sad":
            return f"{self.emoji} 💧"
        if state == "excited":
            return f"{self.emoji} 🔥"
        return self.emoji


# ── The 7 Mascot Characters ──────────────────────────────────────────────────

MASCOTS: Dict[str, Mascot] = {
    "bubble": Mascot(
        name="Bubble Buddy",
        emoji="🫧",
        color="#0284C7",
        catchphrase="Pop, float, and rise to the top!",
        intro_line="🫧 Whoosh! Bubble Buddy is here! Let's float the giants rightward!",
        win_line="🎉 Pop-tastic! Every single bar is in its happy sorted home!",
        reaction_correct=[
            "🫧 WHOOSH! Up it floats! You called that perfectly! +10 XP",
            "🫧 POP! Right on the money! That giant is bubbling up!",
            "🫧 Spot on! You've got an eagle eye for adjacent pairs! +10 XP",
            "🫧 Sizzling soda! That was exactly the right call!",
            "🫧 Bubbles don't lie, and neither do you! Beautiful logic! +10 XP",
        ],
        reaction_wrong=[
            "🫧 Oopsie! No worries at all, let's keep floating! +2 XP",
            "🫧 Pop! A tiny slip, but learning is how we grow! +2 XP",
            "🫧 Almost! Just compare the two neighbors side-by-side! +2 XP",
            "🫧 Don't fret! Even the biggest bubbles wobble before they rise!",
            "🫧 Hang in there! Watch which neighbor is taller next time!",
        ],
        reaction_streak={
            5: "🫧 5 in a row! You're bubbling with sheer brilliance!",
            10: "🫧 10 STREAK! Unstoppable bubble vortex unleashed!",
            20: "🫧 20 STREAK! Legendary Bubble Grandmaster status!",
        },
        hint_style="🫧 Bubble Tip:",
    ),

    "insertion": Mascot(
        name="Insertion Iggy",
        emoji="🃏",
        color="#2563EB",
        catchphrase="A tidy hand makes a winning deck.",
        intro_line="🃏 Greetings! Iggy here. Let's arrange these numbers like playing cards.",
        win_line="✨ Immaculate order! Every card has slid into its rightful slot.",
        reaction_correct=[
            "🃏 Crisp as a fresh deck! Exactly where it belonged! +10 XP",
            "🃏 Smooth shuffle! You slid that right into place! +10 XP",
            "🃏 Tidy thinking! Left portion stays sorted, just as planned!",
            "🃏 Clean execution! You read that hand like a pro! +10 XP",
            "🃏 Precision insertion! Not a single step out of place!",
        ],
        reaction_wrong=[
            "🃏 A minor misdeal! Take another look at the sorted cards! +2 XP",
            "🃏 Keep your cool! Look backwards from the key to find its spot! +2 XP",
            "🃏 Cards take patience! We only shift when the neighbor is bigger!",
            "🃏 Easy now, steady hands! Re-examine the left prefix! +2 XP",
            "🃏 No sweat! Even seasoned players re-check their hand!",
        ],
        reaction_streak={
            5: "🃏 5 consecutive tidy insertions! You're in the zone!",
            10: "🃏 10 streak! A masterclass in systematic sorting!",
            20: "🃏 20 streak! Pure cardistry perfection!",
        },
        hint_style="🃏 Iggy's Playbook:",
    ),

    "selection": Mascot(
        name="Selection Sia",
        emoji="👑",
        color="#D97706",
        catchphrase="Seek the crown jewel; settle for nothing less.",
        intro_line="👑 Royal greetings! I am Sia. We shall survey all and crown the true minimum.",
        win_line="🏰 Magnificent! A kingdom organized from the humblest to the greatest!",
        reaction_correct=[
            "👑 Splendid decree! You identified the true sovereign! +10 XP",
            "👑 Crowned with precision! That is undeniably the smallest! +10 XP",
            "👑 A royal deduction! Minimum secured without hesitation!",
            "👑 Majestically done! Your analytical gaze misses nothing! +10 XP",
            "👑 Impeccable taste! Locked into position with supreme grace!",
        ],
        reaction_wrong=[
            "👑 Patience, courtier! Scan until the very end before crowning! +2 XP",
            "👑 A noble effort! Remember, a smaller candidate may hide ahead! +2 XP",
            "👑 Do not rush the throne! Let all elements be weighed first!",
            "👑 Regroup your focus! Seek the smallest in the unsorted realm! +2 XP",
            "👑 Even monarchs calibrate! Gaze upon the remaining line!",
        ],
        reaction_streak={
            5: "👑 5 royal victories in a row! The court applauds!",
            10: "👑 10 consecutive crowns! An empire of intellect!",
            20: "👑 20 streak! Hail the Supreme Sovereign of Selection!",
        },
        hint_style="👑 Sia's Decree:",
    ),

    "merge": Mascot(
        name="Merge Mia",
        emoji="🧩",
        color="#0D9488",
        catchphrase="Divided we conquer; united we soar.",
        intro_line="🧩 Hello friend! I'm Mia. Together we'll break big puzzles into bite-sized wins!",
        win_line="🌟 Harmony achieved! All sub-arrays have merged in flawless sync!",
        reaction_correct=[
            "🧩 Click! The pieces fit together like clockwork! +10 XP",
            "🧩 Teamwork triumph! You picked the winning front-runner! +10 XP",
            "🧩 Beautiful merge! Left and right united in harmony!",
            "🧩 That's Divide & Conquer mastery in action! +10 XP",
            "🧩 Flawless assembly! Both halves respect your keen eye!",
        ],
        reaction_wrong=[
            "🧩 Just a puzzle mismatch! Compare only the heads of each half! +2 XP",
            "🧩 No stress! Divide the problem down and try again! +2 XP",
            "🧩 Keep piecing it together! Which sub-array has the smaller leader?",
            "🧩 We learn by reconnecting the pieces! Steady on! +2 XP",
            "🧩 Good try! A gentle breath, then compare the front runners!",
        ],
        reaction_streak={
            5: "🧩 5 merged solutions in a row! Complete harmony!",
            10: "🧩 10 streak! A grand symphony of algorithmic unity!",
            20: "🧩 20 streak! Master of the Divide & Conquer arts!",
        },
        hint_style="🧩 Mia's Blueprint:",
    ),

    "quick": Mascot(
        name="Quick Quinn",
        emoji="⚡",
        color="#E11D48",
        catchphrase="Speed is an art; the pivot leads the charge.",
        intro_line="⚡ Zap! Quinn here! Pick your pivot, partition fast, and leave dust behind!",
        win_line="⚡ Lightning strike! Partitioned, sorted, and done in record time!",
        reaction_correct=[
            "⚡ ZAP! Bullseye on that pivot boundary! +10 XP",
            "⚡ Blazing speed! Left or right, you called it instantly! +10 XP",
            "⚡ High voltage logic! Partition locked and loaded!",
            "⚡ Sonic precision! That pivot referee salutes you! +10 XP",
            "⚡ Electrifying! That's how we sort at terminal velocity!",
        ],
        reaction_wrong=[
            "⚡ Static hiccup! Check whether it's smaller than the pivot! +2 XP",
            "⚡ Shake it off fast! Speed comes from quick recovery! +2 XP",
            "⚡ Mind the pivot line! Less goes left, greater stays right!",
            "⚡ Quick reboot! Re-check the pivot value and blast back in! +2 XP",
            "⚡ Close spark! Keep your eye on that reference marker!",
        ],
        reaction_streak={
            5: "⚡ 5 lightning strikes! You're burning through the array!",
            10: "⚡ 10 streak! Supersonic sorting overdrive!",
            20: "⚡ 20 streak! Pure uncontainable computational plasma!",
        },
        hint_style="⚡ Quinn's Spark:",
    ),

    "binary": Mascot(
        name="Binary Bot",
        emoji="🤖",
        color="#2563EB",
        catchphrase="Halve the space. Locate target. Compute.",
        intro_line="🤖 Beep-boop! Binary Bot online. Initiating O(log n) subspace elimination.",
        win_line="🎯 Target acquired and verified. Logarithmic efficiency: 100%.",
        reaction_correct=[
            "🤖 CALCULATION: 100% ACCURATE. Subspace halved. +10 XP",
            "🤖 OPTIMAL TRAJECTORY CONFIRMED. Left/Right decision sound!",
            "🤖 BEEP! Target quadrant successfully isolated. +10 XP",
            "🤖 LOGARITHMIC EFFICIENCY MAXIMIZED. Stellar logic processor!",
            "🤖 HIGH-PRECISION PROBE REGISTERED. Zero computational waste! +10 XP",
        ],
        reaction_wrong=[
            "🤖 RECALIBRATING SENSORS. Target value vs midpoint value comparison mismatch. +2 XP",
            "🤖 MINOR SYNTAX VARIANCE. Check if target is greater or lesser than mid! +2 XP",
            "🤖 COMPUTATION ADJUSTED. Discard the opposite half next iteration!",
            "🤖 BUFFER CLEARED. Re-evaluating interval bounds [low..high]! +2 XP",
            "🤖 ADAPTIVE LEARNING ENGAGED. Next cycle will succeed!",
        ],
        reaction_streak={
            5: "🤖 5 CONSECUTIVE HITS. Algorithmic efficiency exceeding spec!",
            10: "🤖 10 STREAK. Processor running at optimal clock frequency!",
            20: "🤖 20 STREAK. QUANTUM-TIER LOGARITHMIC SAGE DETECTED!",
        },
        hint_style="🤖 Bot Telemetry:",
    ),

    "linear": Mascot(
        name="Linear Luna",
        emoji="🌙",
        color="#0891B2",
        catchphrase="Step by step, the truth reveals itself under starlight.",
        intro_line="🌙 Soft greetings traveler. I am Luna. Let us walk the path element by element.",
        win_line="🌌 Journey fulfilled. Every star counted, the destination reached in peace.",
        reaction_correct=[
            "🌙 Wonderfully perceived. The path unfolds before your calm gaze. +10 XP",
            "🌙 Like starlight through mist, your insight is clear and true. +10 XP",
            "🌙 Patiently seen. You recognized the sequential step with grace.",
            "🌙 Beautiful intuition. Step by step, wisdom grows. +10 XP",
            "🌙 The stars align with your prediction. Peaceful and sure. +10 XP",
        ],
        reaction_wrong=[
            "🌙 A gentle detour. Take your time; the night is young. +2 XP",
            "🌙 Even wandering footsteps find the constellation. Breathe and look again. +2 XP",
            "🌙 No rush along this road. Check the current element beside the target.",
            "🌙 Softly now. Each stone on the path teaches something precious. +2 XP",
            "🌙 Let calm guide your next step. You will see it clearly.",
        ],
        reaction_streak={
            5: "🌙 5 serene steps in unison. The moon smiles upon you.",
            10: "🌙 10 steps of unwavering focus. A tranquil constellation shines!",
            20: "🌙 20 streak. You walk the eternal path with masterly peace.",
        },
        hint_style="🌙 Luna's Guiding Star:",
    ),
}


def get_mascot(key: str) -> Mascot:
    """Retrieve mascot by identifier key; falls back to Bubble Buddy."""
    return MASCOTS.get(key.lower().strip(), MASCOTS["bubble"])


def get_mascot_for_algorithm(algo_name: str) -> Mascot:
    """Resolve companion mascot based on algorithm title (e.g. 'Bubble Sort')."""
    clean = algo_name.lower().strip()
    for key in ("bubble", "insertion", "selection", "merge", "quick", "binary", "linear"):
        if key in clean:
            return MASCOTS[key]
    return MASCOTS["bubble"]
