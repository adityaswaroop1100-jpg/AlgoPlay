// app.js - Main Application Controller for AlgoPlay Web

import { themeManager } from "./theme.js";
import { SORTING_ALGORITHMS, SEARCHING_ALGORITHMS, AlgorithmStep } from "./algorithms.js";
import { VisualizerCanvas } from "./visualizer.js";
import { CoachPanel } from "./coach.js";
import { ModalController } from "./modals.js";

const TICKER_TIPS = [
  "💡 Bubble Sort repeatedly swaps adjacent out-of-order pairs until no swaps occur.",
  "⚡ Quick Sort selects a pivot element and partitions smaller items left, larger right.",
  "🎯 Selection Sort always finds the minimum remaining element and swaps it to the front.",
  "🃏 Insertion Sort maintains a sorted prefix, inserting each new item into position.",
  "🔀 Merge Sort divides the array in half recursively, then zips them together in O(n log n).",
  "🔍 Binary Search cuts the active search candidates in half with every single probe.",
  "⚡ Space complexity of Bubble, Insertion, and Selection Sort is strictly O(1) auxiliary space.",
  "💡 Invariant: At step i in Bubble Sort, the i largest elements are in their final positions."
];

class AlgoPlayApp {
  constructor() {
    this.currentTab = 0; // 0 = Sorting, 1 = Searching
    this.currentSort = "Bubble Sort";
    this.currentSearch = "Linear Search";

    this.dataSize = 20;
    this.originalData = this.generateRandomData(this.dataSize);
    this.currentData = [...this.originalData];

    this.isRunning = false;
    this.isPaused = false;
    this.activeGenerator = null;
    this.animTimer = null;
    this.speedMs = 70;

    this.xp = parseInt(localStorage.getItem("algoplay_xp") || "0", 10);
    this.briefingShown = {};

    this.initDOM();
    this.initCanvas();
    this.initCoach();
    this.initModals();
    this.bindEvents();
    this.startTicker();

    this.selectSort("Bubble Sort");
    themeManager.apply();
  }

  generateRandomData(size) {
    return Array.from({ length: size }, () => Math.floor(Math.random() * 90) + 10);
  }

  initDOM() {
    this.canvasEl = document.getElementById("main-canvas");
    this.pseudoContainer = document.getElementById("pseudo-code-container");
    this.statusText = document.getElementById("status-text");
    this.xpLabel = document.getElementById("xp-label");
    this.elementCountLabel = document.getElementById("element-count-lbl");
    this.targetInput = document.getElementById("search-target-input");
    this.sizeInput = document.getElementById("size-slider");
    this.speedInput = document.getElementById("speed-slider");
    this.customInput = document.getElementById("custom-array-input");

    this.updateXP(0);
  }

  initCanvas() {
    this.canvas = new VisualizerCanvas(this.canvasEl, "bars");
  }

  initCoach() {
    this.coach = new CoachPanel(document.getElementById("coach-card"));
  }

  initModals() {
    this.modals = new ModalController(this);
  }

  updateXP(gain) {
    this.xp += gain;
    localStorage.setItem("algoplay_xp", String(this.xp));
    if (this.xpLabel) {
      this.xpLabel.textContent = `⚡ ${this.xp} XP`;
    }
  }

  selectSort(name) {
    this.currentSort = name;
    this.canvas.setAlgoName(name);
    this.canvas.mode = "bars";

    document.querySelectorAll(".chip-btn").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.algo === name);
    });

    const algo = SORTING_ALGORITHMS[name];
    this.renderPseudocode(algo.pseudo_code);
    this.updateComplexityCard(algo.info);
    this.actionReset();
  }

  selectSearch(name) {
    this.currentSearch = name;
    this.canvas.setAlgoName(name);
    this.canvas.mode = "boxes";

    document.querySelectorAll(".chip-btn").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.algo === name);
    });

    const algo = SEARCHING_ALGORITHMS[name];
    this.renderPseudocode(algo.pseudo_code);
    this.updateComplexityCard(algo.info);

    if (name === "Binary Search") {
      this.currentData.sort((a, b) => a - b);
    }
    this.actionReset();
  }

  switchTab(tabIndex) {
    this.currentTab = tabIndex;
    const isSearch = tabIndex === 1;

    document.getElementById("btn-tab-sort").classList.toggle("active", !isSearch);
    document.getElementById("btn-tab-search").classList.toggle("active", isSearch);

    document.getElementById("sorting-chips").style.display = isSearch ? "none" : "flex";
    document.getElementById("searching-chips").style.display = isSearch ? "flex" : "none";
    document.getElementById("search-target-group").style.display = isSearch ? "flex" : "none";

    if (isSearch) {
      this.selectSearch(this.currentSearch);
    } else {
      this.selectSort(this.currentSort);
    }
  }

  renderPseudocode(lines) {
    this.pseudoContainer.innerHTML = "";
    lines.forEach((line, idx) => {
      const div = document.createElement("div");
      div.className = "pseudo-line";
      div.id = `pseudo-line-${idx}`;

      const num = document.createElement("span");
      num.className = "line-num";
      num.textContent = idx + 1;

      const code = document.createElement("span");
      code.className = "line-text";
      code.textContent = line;

      div.appendChild(num);
      div.appendChild(code);
      this.pseudoContainer.appendChild(div);
    });
  }

  highlightPseudoLine(lineIdx) {
    document.querySelectorAll(".pseudo-line").forEach((el, idx) => {
      el.classList.toggle("active", idx === lineIdx);
    });
  }

  updateComplexityCard(info) {
    const elBest = document.getElementById("badge-best");
    const elAvg = document.getElementById("badge-avg");
    const elWorst = document.getElementById("badge-worst");
    const elSpace = document.getElementById("badge-space");

    if (elBest) elBest.textContent = info.time_best;
    if (elAvg) elAvg.textContent = info.time_avg;
    if (elWorst) elWorst.textContent = info.time_worst;
    if (elSpace) elSpace.textContent = info.space;
  }

  actionRandomize() {
    this.actionPause();
    this.originalData = this.generateRandomData(this.dataSize);
    this.currentData = [...this.originalData];

    if (this.currentTab === 1 && this.currentSearch === "Binary Search") {
      this.currentData.sort((a, b) => a - b);
    }

    if (this.targetInput) {
      const midVal = this.currentData[Math.floor(this.currentData.length / 2)];
      this.targetInput.value = String(midVal);
    }
    this.actionReset();
  }

  actionReset() {
    this.actionPause();
    this.currentData = [...this.originalData];
    if (this.currentTab === 1 && this.currentSearch === "Binary Search") {
      this.currentData.sort((a, b) => a - b);
    }
    this.activeGenerator = null;
    this.canvas.resetCounters();

    const isSearch = this.currentTab === 1;
    const tgt = isSearch ? parseInt(this.targetInput?.value || "0", 10) : null;
    const initStep = new AlgorithmStep({ array: [...this.currentData], target: tgt });

    this.canvas.render(initStep);
    this.highlightPseudoLine(-1);
    this.coach.update(isSearch ? this.currentSearch : this.currentSort, initStep, this.getActiveInfo());
    this.updateMetrics(0, 0, "00:00.0", "Ready");
  }

  actionStart() {
    if (this.isRunning) return;

    const algoName = this.currentTab === 1 ? this.currentSearch : this.currentSort;
    if (!this.briefingShown[algoName]) {
      this.briefingShown[algoName] = true;
      this.modals.showBriefing(algoName, () => this.startEngine(), () => this.actionStep());
      return;
    }

    this.startEngine();
  }

  startEngine() {
    if (this.isRunning) return;
    this.isRunning = true;
    this.isPaused = false;
    document.getElementById("btn-start").textContent = "⏸ Pause";

    if (!this.activeGenerator) {
      this.initGenerator();
    }
    this.animLoop();
  }

  actionPause() {
    this.isRunning = false;
    this.isPaused = true;
    if (this.animTimer) {
      clearTimeout(this.animTimer);
      this.animTimer = null;
    }
    document.getElementById("btn-start").textContent = "▶ Start";
  }

  actionStep() {
    if (!this.activeGenerator) {
      this.initGenerator();
    }
    this.advanceStep();
  }

  initGenerator() {
    const isSearch = this.currentTab === 1;
    if (isSearch) {
      const tgt = parseInt(this.targetInput.value || "0", 10);
      const algo = SEARCHING_ALGORITHMS[this.currentSearch];
      this.activeGenerator = algo.run(this.currentData, tgt);
    } else {
      const algo = SORTING_ALGORITHMS[this.currentSort];
      this.activeGenerator = algo.run(this.currentData);
    }
  }

  animLoop() {
    if (this.isRunning && this.activeGenerator) {
      const hasNext = this.advanceStep();
      if (hasNext) {
        this.animTimer = setTimeout(() => this.animLoop(), this.speedMs);
      } else {
        this.actionPause();
        this.canvas.launchConfetti(60);
        this.updateXP(10);
      }
    }
  }

  advanceStep() {
    if (!this.activeGenerator) return false;
    const res = this.activeGenerator.next();
    if (res.done) return false;

    const step = res.value;
    this.canvas.render(step);
    this.highlightPseudoLine(step.pseudo_line);

    const isSearch = this.currentTab === 1;
    const algoName = isSearch ? this.currentSearch : this.currentSort;
    this.coach.update(algoName, step, this.getActiveInfo());

    this.updateMetrics(this.canvas.cmpCounter, this.canvas.stepCounter, "", step.status);
    return true;
  }

  getActiveInfo() {
    const isSearch = this.currentTab === 1;
    return (isSearch ? SEARCHING_ALGORITHMS[this.currentSearch] : SORTING_ALGORITHMS[this.currentSort]).info;
  }

  updateMetrics(cmps, swaps, time, status) {
    const elCmps = document.getElementById("stat-cmps");
    const elSwaps = document.getElementById("stat-swaps");
    if (elCmps) elCmps.textContent = String(cmps);
    if (elSwaps) elSwaps.textContent = String(swaps);
    if (this.statusText) this.statusText.textContent = status || "Ready";
  }

  bindEvents() {
    // Theme toggle
    document.getElementById("btn-theme-toggle").onclick = () => {
      const newTheme = themeManager.toggle();
      document.getElementById("theme-toggle-icon").textContent = newTheme === "dark" ? "☀️ Light" : "🌙 Dark";
    };

    // Tabs
    document.getElementById("btn-tab-sort").onclick = () => this.switchTab(0);
    document.getElementById("btn-tab-search").onclick = () => this.switchTab(1);

    // Modals in top bar
    document.getElementById("btn-modal-race").onclick = () => this.modals.showRace();
    document.getElementById("btn-modal-benchmark").onclick = () => this.modals.showBenchmark();
    document.getElementById("btn-modal-quiz").onclick = () => {
      this.modals.showQuiz({
        question: "In Quick Sort, what is the best/average case time complexity?",
        options: ["O(n²)", "O(n log n)", "O(n)", "O(log n)"],
        correctIndex: 1
      }, (correct) => {
        if (correct) this.updateXP(15);
      });
    };

    // Algorithm chips
    document.querySelectorAll(".chip-btn").forEach(btn => {
      btn.onclick = () => {
        const algo = btn.dataset.algo;
        if (this.currentTab === 1) {
          this.selectSearch(algo);
        } else {
          this.selectSort(algo);
        }
      };
    });

    // Controls
    document.getElementById("btn-randomize").onclick = () => this.actionRandomize();
    document.getElementById("btn-start").onclick = () => {
      if (this.isRunning) this.actionPause();
      else this.actionStart();
    };
    document.getElementById("btn-step").onclick = () => this.actionStep();
    document.getElementById("btn-reset").onclick = () => this.actionReset();

    // Speed slider
    this.speedInput.oninput = (e) => {
      const val = parseInt(e.target.value, 10);
      // Map 1-100 to 200ms - 10ms
      this.speedMs = Math.round(200 - (val / 100) * 190);
    };

    // Size slider
    this.sizeInput.oninput = (e) => {
      const newSize = parseInt(e.target.value, 10);
      this.dataSize = newSize;
      if (this.elementCountLabel) {
        this.elementCountLabel.textContent = `${newSize} elements 📊`;
      }
      this.actionRandomize();
    };

    // Custom Array Input
    document.getElementById("btn-load-custom").onclick = () => {
      const raw = this.customInput.value.trim();
      if (!raw) return;
      const parsed = raw.split(/[\s,]+/).map(Number).filter(n => !isNaN(n) && n > 0);
      if (parsed.length >= 3) {
        this.originalData = parsed;
        this.dataSize = parsed.length;
        if (this.elementCountLabel) this.elementCountLabel.textContent = `${parsed.length} elements 📊`;
        this.actionReset();
      }
    };

    // Concept Briefing button
    document.getElementById("btn-open-briefing").onclick = () => {
      const algoName = this.currentTab === 1 ? this.currentSearch : this.currentSort;
      this.modals.showBriefing(algoName, () => this.startEngine(), () => this.actionStep());
    };

    // Modal Close buttons
    document.querySelectorAll(".modal-close-btn").forEach(btn => {
      btn.onclick = (e) => {
        const modal = e.target.closest(".modal-backdrop");
        if (modal) modal.classList.remove("active");
      };
    });

    // Race modal controls
    document.getElementById("btn-start-race").onclick = () => this.modals.startRace();
    document.getElementById("btn-reset-race").onclick = () => this.modals.resetRace();
    document.getElementById("race-algo-1").onchange = () => this.modals.resetRace();
    document.getElementById("race-algo-2").onchange = () => this.modals.resetRace();

    // Expandable "Why?" deep dive in Coach
    document.getElementById("btn-coach-why").onclick = () => {
      const content = document.getElementById("coach-why-content");
      const isVisible = content.style.display === "block";
      content.style.display = isVisible ? "none" : "block";
      document.getElementById("btn-coach-why").textContent = isVisible ? "🤔 Why? (Expand)" : "🤔 Why? (Collapse)";
    };

    // Global keyboard shortcuts
    window.addEventListener("keydown", (e) => {
      if (e.target.tagName === "INPUT") return;
      if (e.code === "Space" || e.code === "ArrowRight") {
        e.preventDefault();
        if (this.isRunning) this.actionPause();
        else this.actionStep();
      } else if (e.code === "Enter") {
        e.preventDefault();
        this.actionStart();
      } else if (e.key === "p" || e.key === "P") {
        e.preventDefault();
        if (this.isRunning) this.actionPause();
        else this.actionStart();
      } else if (e.key === "r" || e.key === "R") {
        e.preventDefault();
        this.actionReset();
      } else if (e.key === "s" || e.key === "S") {
        e.preventDefault();
        this.actionRandomize();
      }
    });
  }

  startTicker() {
    const el = document.getElementById("ticker-content");
    let idx = 0;
    setInterval(() => {
      idx = (idx + 1) % TICKER_TIPS.length;
      if (el) el.textContent = TICKER_TIPS[idx];
    }, 6000);
  }
}

window.addEventListener("DOMContentLoaded", () => {
  window.app = new AlgoPlayApp();
});
