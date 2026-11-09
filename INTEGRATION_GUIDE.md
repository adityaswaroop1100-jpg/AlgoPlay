# AlgoPlay Story Mode — Integration & Architecture Guide

Story Mode transforms **AlgoPlay** into an interactive narrative learning game where 7 unique algorithm mascots guide learners through chapter-based levels, branching step predictions, XP progression, streaks, and badge unlocks.

---

## 1. Architecture & Component Hierarchy

```
AlgoPlay Shell (main.py)
 └── Tab Container / ttk.Notebook
      ├── ↕ Sorting Tab
      ├── 🔍 Searching Tab
      └── 📖 Story Mode Tab (story_tab.py)
           ├── Top Bar (Chapter Selector, Level Advance, Stats & Badges, Predict Toggle)
           ├── Visualizer Canvas (visualizer.py)
           │    └── Canvas Speech Bubble (Mascot dialogue + dynamic expressions)
           ├── PredictPanel (predict_panel.py) [Branching decisions & hints]
           ├── FeedbackPanel (feedback.py)     [XP awards, streaks, & reactions]
           └── Controls Bar (Start / Step / Reset / Status)
```

---

## 2. File Directory & Component Manifest

All files strictly adhere to Python's standard library and tkinter (zero pip dependencies) with a clean modular separation of concerns:

| File | Purpose | Line Count |
| :--- | :--- | :--- |
| [`game_state.py`](game_state.py) | XP, streak, levels, badges tracker with auto-save to `saves/progress.json` | 193 lines |
| [`badges.py`](badges.py) | 14 badge definitions and unlock evaluation logic | 183 lines |
| [`mascots.py`](mascots.py) | 7 algorithm mascots with personalized voices, reactions, and facial expressions | 282 lines |
| [`story.py`](story.py) | 8 chapters, boss levels, and level sequence progression helpers | 215 lines |
| [`predict_panel.py`](predict_panel.py) | "What happens next?" 3-option decision widget with instant green/red feedback | 289 lines |
| [`feedback.py`](feedback.py) | Mascot praise banner, XP toasts, and auto-dismiss timers | 246 lines |
| [`story_tab.py`](story_tab.py) | Self-contained Story Mode page uniting visualizer, speech bubble, and game loop | 281 lines |
| [`algorithm_base.py`](algorithm_base.py) | Extended `AlgorithmStep` with prediction fields + `Step` alias | 122 lines |
| [`steps.py`](steps.py) | Compatibility module forwarding `Step` and `AlgorithmStep` | 9 lines |
| [`main.py`](main.py) | Tab registration, 3-way switching, and app shutdown save hooks | 298 lines |

---

## 3. The 7 Mascots & Dialogue System

Each mascot features custom speech bubbles drawn directly onto the visualizer canvas with five dynamic emotion states (`idle`, `thinking`, `happy`, `sad`, `excited`):

1. **Bubble Buddy 🫧** (Bubble Sort) — Cheerful, bubbly, and enthusiastic (`#3B82F6`)
2. **Insertion Iggy 🃏** (Insertion Sort) — Methodical card dealer who loves tidy order (`#10B981`)
3. **Selection Sia 👑** (Selection Sort) — Regal, decisive scout always searching for the minimum (`#F59E0B`)
4. **Merge Mia 🧩** (Merge Sort) — Wise strategist who conquers by dividing (`#6366F1`)
5. **Quick Quinn ⚡** (Quick Sort) — High-energy speedster commanding pivot strikes (`#EF4444`)
6. **Binary Bot 🤖** (Binary Search) — Precise, algorithmic calculator halving search space (`#06B6D4`)
7. **Linear Luna 🌙** (Linear Search) — Calm, poetic traveler checking elements one by one (`#8B5CF6`)

---

## 4. Gamification Rules & Mechanics

- **XP Awards:**
  - `+10 XP`: Correct step prediction.
  - `+2 XP`: Consolation XP for thoughtful incorrect predictions.
  - `-5 XP`: Revealing a pedagogical hint.
  - `+50 XP`: Standard level completion bonus.
  - `+100 XP`: Chapter Boss level completion.
  - `+50 XP`: Perfect level bonus (0 incorrect predictions).
- **Streak Multipliers:**
  - Increments on correct answers; resets to 0 on incorrect answers.
  - Milestones at 5, 10, and 20 consecutive correct predictions trigger special mascot fanfare and XP bonuses.
- **Persistence:**
  - Saves progress automatically to `saves/progress.json` upon level completion and on app exit (`WM_DELETE_WINDOW`).

---

## 5. Running the Application

To launch AlgoPlay with Story Mode:

```bash
cd /Users/adityaswaroop/Downloads/AlgoPlay
python3 main.py
```

Switch to **📖 Story Mode** using the top navigation bar to play through chapters!
