# AlgoPlay — Interactive Algorithm Visualizer & Learning Engine

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/Live_Demo-GitHub_Pages-2563EB?style=for-the-badge&logo=githubpages&logoColor=white" alt="Live Demo" />
  <img src="https://img.shields.io/badge/GUI-Tkinter-informational?style=for-the-badge" alt="Tkinter" />
  <img src="https://img.shields.io/badge/Dependencies-Zero%20(Stdlib)-success?style=for-the-badge" alt="Zero Dependencies" />
  <img src="https://img.shields.io/badge/Platform-Web%20%7C%20macOS%20%7C%20Linux%20%7C%20Windows-lightgrey?style=for-the-badge" alt="Cross Platform" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

> 🌐 **Live Web Application:** Experience AlgoPlay directly in your browser without installing anything at [**adityaswaroop1100-jpg.github.io/AlgoPlay**](https://adityaswaroop1100-jpg.github.io/AlgoPlay/)

An interactive, responsive visualizer designed to make data structures and algorithms intuitive, visual, and engaging. Available both as a zero-dependency Python desktop application and as a responsive web app.

AlgoPlay pairs real-time animation with live pseudocode synchronization, step-by-step coaching, pre-flight algorithmic complexity briefings, head-to-head algorithm racing, and a gamified XP prediction engine — completely offline with zero external dependencies.

---

## Table of Contents

- [Key Features](#-key-features)
- [Supported Algorithms](#-supported-algorithms)
- [Architecture & Design Patterns](#-architecture--design-patterns)
- [Color System & Visual Legend](#-color-system--visual-legend)
- [Keyboard Shortcuts](#-keyboard-shortcuts)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [License](#-license)

---

## ✨ Key Features

### 1. Dual Canvas Visualization
- **Sorting Mode**: Vertical bars with proportional scaling, top cap highlights, in-bar action badges (`⇄`, `CMP`, `P`), relational comparison arches (`v1 > v2`), and subtle partition tints behind sorted elements.
- **Searching Mode**: Centered array cards with probe badges, active search range brackets (`[lo … hi]`), target match pulsing rings, and diagonal strikethroughs across eliminated candidates.

### 2. Synchronized Pseudocode & Step Coach
- **Live Pseudocode**: Displays accurate implementation steps with instant line-highlighting synchronized to the active generator yield.
- **Interactive Coach**: Plain-English explanations describing *what* just happened, *what to watch next*, and an expandable **"Why?"** breakdown explaining the underlying algorithm invariant.

### 3. Pre-Flight Concept & Complexity Briefing
- Before executing any sort or search, view a pre-flight modal summarizing:
  - Core algorithmic intuition & strategy
  - Real-world conceptual analogy (e.g., sorting playing cards, looking up a word in a dictionary)
  - Time & Space Complexity breakdown (Best $\Omega$, Average $\Theta$, Worst $O$, Auxiliary Space)

### 4. Head-to-Head Race Mode
- Launch a split-canvas window pitting any two sorting algorithms against one another on the exact same dataset.
- Features real-time comparison/swap counters, progress metrics, and celebration particle confetti upon completion.

### 5. Benchmark Performance Comparison
- Run all five sorting algorithms concurrently on the active dataset to generate an instant comparative bar chart tracking exact operation counts.

### 6. Gamified Quiz & Story Mode
- **Predict-Next-Step Engine**: Inline challenges prompt learners to forecast algorithm decisions (e.g., "Will these elements swap?"), awarding XP and tracking answer streaks.
- **Story Mode**: 8 narrative chapters led by 7 algorithm companion mascots, complete with dialogue bubbles, level progression, and 14 unlockable achievements saved locally.

### 7. Dual Modern Themes
- Switch seamlessly between a high-contrast dark theme (ink-black surfaces, vibrant cobalt/amber/rose data bars) and a crisp light theme with an observer-driven palette update across all widgets.

---

## 📊 Supported Algorithms

| Algorithm | Category | Best Case | Average Case | Worst Case | Space | Stable |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Bubble Sort** | Sorting | $\Omega(n)$ | $\Theta(n^2)$ | $O(n^2)$ | $O(1)$ | Yes |
| **Insertion Sort** | Sorting | $\Omega(n)$ | $\Theta(n^2)$ | $O(n^2)$ | $O(1)$ | Yes |
| **Selection Sort** | Sorting | $\Omega(n^2)$ | $\Theta(n^2)$ | $O(n^2)$ | $O(1)$ | No |
| **Merge Sort** | Sorting | $\Omega(n \log n)$ | $\Theta(n \log n)$ | $O(n \log n)$ | $O(n)$ | Yes |
| **Quick Sort** | Sorting | $\Omega(n \log n)$ | $\Theta(n \log n)$ | $O(n^2)$ | $O(\log n)$ | No |
| **Linear Search** | Searching | $\Omega(1)$ | $\Theta(n)$ | $O(n)$ | $O(1)$ | N/A |
| **Binary Search** | Searching | $\Omega(1)$ | $\Theta(\log n)$ | $O(\log n)$ | $O(1)$ | N/A |

---

## 🎨 Color System & Visual Legend

| State | Dark Theme | Light Theme | Meaning |
| :--- | :---: | :---: | :--- |
| **Default** | `#2563EB` | `#3B82F6` | Unsorted / unvisited element |
| **Comparing** | `#F59E0B` | `#D97706` | Active comparison probe |
| **Swapping** | `#F43F5E` | `#E11D48` | Elements actively being swapped or shifted |
| **Sorted** | `#10B981` | `#059669` | Element confirmed in its final position |
| **Pivot** | `#06B6D4` | `#0891B2` | Quick Sort partition pivot line / marker |
| **Target** | `#818CF8` | `#6366F1` | Active search target |
| **Eliminated** | `#16161E` | `#E5E5EF` | Candidate excluded from search space |

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
| :--- | :--- |
| <kbd>Space</kbd> / <kbd>→</kbd> | Step forward one algorithmic state |
| <kbd>Enter</kbd> | Start continuous animation |
| <kbd>P</kbd> | Pause / Resume animation |
| <kbd>R</kbd> | Reset dataset to initial state |
| <kbd>S</kbd> | Shuffle / generate new random array |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher.
- Tkinter (included with standard Python installers on macOS and Windows).

### Installation & Run

1. **Clone the repository:**
   ```bash
   git clone git@github.com:adityaswaroop1100-jpg/AlgoPlay.git
   cd AlgoPlay
   ```

2. **Launch the application:**
   ```bash
   python3 main.py
   ```

> **Note for macOS Homebrew users:** If your Python installation requires standalone Tkinter bindings, run:
> ```bash
> brew install python-tk
> python3 main.py
> ```

---

## 🏛️ Architecture & Design Patterns

AlgoPlay is structured with clean separation of concerns and modular component boundaries:

- **Strategy Pattern (`algorithm_base.py`)**: Defines standard abstract interfaces for algorithms. Concrete sorters and searchers inherit from `AlgorithmBase` and implement `run()`, decoupling the UI from execution logic.
- **Python Generators & Non-Blocking Event Loop**: Algorithms yield `AlgorithmStep` objects frame-by-frame. The UI drives these generators using Tkinter's `root.after()` ticks, keeping the GUI responsive during live runs.
- **Observer Pattern (`theme.py`)**: `ThemeManager` broadcasts theme changes to registered listeners across canvases, frames, and control cards.
- **State Persistence (`game_state.py`)**: Player XP, answering streaks, and unlocked achievements automatically serialize to `saves/progress.json` using the standard library.

```
AlgoPlay/
├── main.py              # Application shell, tab coordinator, and event loop
├── visualizer.py        # Canvas rendering engine (bars, cards, arches, confetti)
├── algorithm_base.py    # AlgorithmBase abstract class and AlgorithmStep dataclass
├── sorting.py           # Bubble, Insertion, Selection, Merge, Quick Sort generators
├── searching.py         # Linear and Binary Search generators
├── concept_briefing.py  # Pre-flight algorithm concept & complexity modal
├── coach.py             # Step-by-step explainer & "Why?" invariant guide
├── controls.py          # Steppers, sliders, custom array entry, and complexity cards
├── hint_engine.py       # Predict-next-step interactive quiz modal
├── progress_hud.py      # Completion percentage HUD & learning tip ticker
├── race_window.py       # Head-to-head algorithm race window
├── quiz.py              # Gamified algorithm trivia window
├── story_tab.py         # Story Mode tab controller
├── story.py             # Narrative chapters, level data, and boss challenges
├── mascots.py           # 7 algorithm companion mascots with dynamic expressions
├── predict_panel.py     # Story Mode decision panel
├── feedback.py          # Visual reward banners and streak toasts
├── game_state.py        # XP, streaks, level progression, and JSON persistence
├── badges.py            # Unlockable achievements evaluation
├── theme.py             # Dark/Light palettes, typography, and ThemeManager observer
├── widgets.py           # Custom macOS-compatible flat buttons with hover states
└── stats.py             # Performance counters and variable inspection
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
