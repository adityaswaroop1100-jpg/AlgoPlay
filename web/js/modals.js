// modals.js - Pre-Flight Concept Briefing, Race Mode, Benchmark & Quiz Modals

import { SORTING_ALGORITHMS, SEARCHING_ALGORITHMS } from "./algorithms.js";
import { VisualizerCanvas } from "./visualizer.js";

export class ModalController {
  constructor(app) {
    this.app = app;
    this.raceRunning = false;
    this.raceTimer = null;
    this.raceCanvas1 = null;
    this.raceCanvas2 = null;
  }

  // ───────────────────────────────────────────────────────────────────────────
  // Concept & Complexity Briefing Modal
  // ───────────────────────────────────────────────────────────────────────────
  showBriefing(algoName, onStart, onStep) {
    const isSearch = this.app.currentTab === 1;
    const algo = (isSearch ? SEARCHING_ALGORITHMS : SORTING_ALGORITHMS)[algoName];
    if (!algo) return;

    const modal = document.getElementById("briefing-modal");
    const titleEl = document.getElementById("briefing-title");
    const descEl = document.getElementById("briefing-desc");
    const analogyEl = document.getElementById("briefing-analogy");
    const strategyEl = document.getElementById("briefing-strategy");

    const tBest = document.getElementById("briefing-t-best");
    const tAvg = document.getElementById("briefing-t-avg");
    const tWorst = document.getElementById("briefing-t-worst");
    const tSpace = document.getElementById("briefing-space");

    titleEl.textContent = `${algo.icon || "💡"} ${algo.name}`;
    descEl.textContent = algo.info.description;
    analogyEl.textContent = `💡 Real-World Analogy: "${algo.info.analogy}"`;

    if (tBest) tBest.textContent = algo.info.time_best;
    if (tAvg) tAvg.textContent = algo.info.time_avg;
    if (tWorst) tWorst.textContent = algo.info.time_worst;
    if (tSpace) tSpace.textContent = algo.info.space;

    // Working strategy list
    strategyEl.innerHTML = "";
    const points = [
      `Maintains the invariant: ${algo.info.invariant}`,
      `Executes in ${algo.info.time_avg} average-case time.`,
      `Requires ${algo.info.space} auxiliary space.`
    ];
    points.forEach(p => {
      const li = document.createElement("li");
      li.textContent = p;
      strategyEl.appendChild(li);
    });

    const startBtn = document.getElementById("btn-briefing-start");
    const stepBtn = document.getElementById("btn-briefing-step");

    startBtn.onclick = () => {
      this.closeModal("briefing-modal");
      if (onStart) onStart();
    };

    stepBtn.onclick = () => {
      this.closeModal("briefing-modal");
      if (onStep) onStep();
    };

    modal.classList.add("active");
  }

  // ───────────────────────────────────────────────────────────────────────────
  // Head-to-Head Race Mode
  // ───────────────────────────────────────────────────────────────────────────
  showRace() {
    const modal = document.getElementById("race-modal");
    modal.classList.add("active");

    const canvas1El = document.getElementById("race-canvas-1");
    const canvas2El = document.getElementById("race-canvas-2");

    if (!this.raceCanvas1) this.raceCanvas1 = new VisualizerCanvas(canvas1El, "bars");
    if (!this.raceCanvas2) this.raceCanvas2 = new VisualizerCanvas(canvas2El, "bars");

    this.resetRace();
  }

  resetRace() {
    if (this.raceTimer) {
      clearInterval(this.raceTimer);
      this.raceTimer = null;
    }
    this.raceRunning = false;

    const select1 = document.getElementById("race-algo-1");
    const select2 = document.getElementById("race-algo-2");
    const name1 = select1.value;
    const name2 = select2.value;

    const data = [...this.app.currentData];

    this.raceCanvas1.setAlgoName(name1);
    this.raceCanvas2.setAlgoName(name2);
    this.raceCanvas1.resetCounters();
    this.raceCanvas2.resetCounters();

    this.raceGen1 = SORTING_ALGORITHMS[name1].run(data);
    this.raceGen2 = SORTING_ALGORITHMS[name2].run(data);

    this.raceStep1 = this.raceGen1.next().value;
    this.raceStep2 = this.raceGen2.next().value;

    this.raceCanvas1.render(this.raceStep1);
    this.raceCanvas2.render(this.raceStep2);

    document.getElementById("race-status").textContent = "Ready. Click 'Start Race' to begin!";
    document.getElementById("btn-start-race").textContent = "▶ Start Race";
  }

  startRace() {
    if (this.raceRunning) {
      this.raceRunning = false;
      clearInterval(this.raceTimer);
      document.getElementById("btn-start-race").textContent = "▶ Resume Race";
      return;
    }

    this.raceRunning = true;
    document.getElementById("btn-start-race").textContent = "⏸ Pause Race";

    let done1 = false;
    let done2 = false;

    this.raceTimer = setInterval(() => {
      if (!done1) {
        const res = this.raceGen1.next();
        if (res.done) {
          done1 = true;
        } else {
          this.raceStep1 = res.value;
          this.raceCanvas1.render(this.raceStep1);
        }
      }

      if (!done2) {
        const res = this.raceGen2.next();
        if (res.done) {
          done2 = true;
        } else {
          this.raceStep2 = res.value;
          this.raceCanvas2.render(this.raceStep2);
        }
      }

      if (done1 && !done2) {
        document.getElementById("race-status").textContent = `🏆 ${document.getElementById("race-algo-1").value} Finished First!`;
        this.raceCanvas1.launchConfetti(50);
      } else if (done2 && !done1) {
        document.getElementById("race-status").textContent = `🏆 ${document.getElementById("race-algo-2").value} Finished First!`;
        this.raceCanvas2.launchConfetti(50);
      }

      if (done1 && done2) {
        clearInterval(this.raceTimer);
        this.raceRunning = false;
        document.getElementById("btn-start-race").textContent = "🏁 Race Finished";
      }
    }, 40);
  }

  // ───────────────────────────────────────────────────────────────────────────
  // Benchmark Comparison Chart
  // ───────────────────────────────────────────────────────────────────────────
  showBenchmark() {
    const modal = document.getElementById("benchmark-modal");
    modal.classList.add("active");

    const data = [...this.app.currentData];
    const results = {};

    for (const [name, algo] of Object.entries(SORTING_ALGORITHMS)) {
      const gen = algo.run(data);
      let ops = 0;
      for (const step of gen) {
        if (step.comparing?.length) ops++;
      }
      results[name] = ops;
    }

    const container = document.getElementById("benchmark-chart-body");
    container.innerHTML = "";

    const maxOps = Math.max(...Object.values(results), 1);
    const minOps = Math.min(...Object.values(results));

    for (const [name, ops] of Object.entries(results)) {
      const row = document.createElement("div");
      row.className = "benchmark-row";

      const pct = (ops / maxOps) * 100;
      const isWinner = ops === minOps;

      row.innerHTML = `
        <div class="benchmark-label">${name}</div>
        <div class="benchmark-bar-track">
          <div class="benchmark-bar ${isWinner ? 'winner' : ''}" style="width: ${pct}%"></div>
        </div>
        <div class="benchmark-value">${ops} ops ${isWinner ? '⚡' : ''}</div>
      `;
      container.appendChild(row);
    }
  }

  // ───────────────────────────────────────────────────────────────────────────
  // Quiz Modal
  // ───────────────────────────────────────────────────────────────────────────
  showQuiz(questionData, onAnswer) {
    const modal = document.getElementById("quiz-modal");
    modal.classList.add("active");

    document.getElementById("quiz-question").textContent = questionData.question;
    const optsContainer = document.getElementById("quiz-options");
    optsContainer.innerHTML = "";

    questionData.options.forEach((opt, idx) => {
      const btn = document.createElement("button");
      btn.className = "quiz-opt-btn";
      btn.textContent = opt;
      btn.onclick = () => {
        const isCorrect = idx === questionData.correctIndex;
        btn.classList.add(isCorrect ? "correct" : "incorrect");
        setTimeout(() => {
          this.closeModal("quiz-modal");
          if (onAnswer) onAnswer(isCorrect);
        }, 1200);
      };
      optsContainer.appendChild(btn);
    });
  }

  closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.remove("active");
    if (id === "race-modal" && this.raceTimer) {
      clearInterval(this.raceTimer);
      this.raceRunning = false;
    }
  }
}
