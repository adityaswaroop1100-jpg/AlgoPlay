// visualizer.js - HTML5 Canvas Rendering Engine with 60FPS Fluid Animation, Audio Synthesis & Glow Effects

import { themeManager } from "./theme.js";

const PTR_COLORS = {
  i: { color: "#2563EB", label: "i" },
  j: { color: "#F59E0B", label: "j" },
  min: { color: "#0284C7", label: "min" },
  pivot: { color: "#06B6D4", label: "P" },
  mid: { color: "#10B981", label: "mid" },
  low: { color: "#06B6D4", label: "lo" },
  high: { color: "#EF4444", label: "hi" },
  pos: { color: "#EAB308", label: "pos" },
};

// Web Audio API Synthesizer (Zero External Files)
class AudioEngine {
  constructor() {
    this.ctx = null;
    this.enabled = true;
  }

  init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) this.ctx = new AudioCtx();
    }
    if (this.ctx && this.ctx.state === "suspended") {
      this.ctx.resume();
    }
  }

  playTone(val, maxVal = 100, type = "sine") {
    if (!this.enabled) return;
    try {
      this.init();
      if (!this.ctx) return;

      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      // Map value (10-100) to musical frequency (220Hz - 880Hz, A3 to A5)
      const freq = 220 + (val / maxVal) * 660;
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

      gain.gain.setValueAtTime(0.04, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + 0.12);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start();
      osc.stop(this.ctx.currentTime + 0.12);
    } catch (_) {}
  }

  playSwapChord(v1, v2) {
    if (!this.enabled) return;
    this.playTone(v1, 100, "triangle");
    setTimeout(() => this.playTone(v2, 100, "triangle"), 30);
  }
}

export const audioEngine = new AudioEngine();

export class VisualizerCanvas {
  constructor(canvasElement, mode = "bars") {
    this.canvas = canvasElement;
    this.ctx = canvasElement.getContext("2d");
    this.mode = mode;
    this.lastStep = null;
    this.algoName = "";
    this.cmpCounter = 0;
    this.stepCounter = 0;

    // Fluid Animation States
    this.displayHeights = [];
    this.particles = [];
    this.searchPings = [];
    this.pulseAngle = 0;

    this.resizeObserver = new ResizeObserver(() => this.resizeAndRender());
    this.resizeObserver.observe(this.canvas.parentElement);

    themeManager.subscribe(() => {
      if (this.lastStep) this.render(this.lastStep);
    });

    this.resize();
    this.startAnimationLoop();
  }

  setAlgoName(name) {
    this.algoName = name;
  }

  resetCounters() {
    this.cmpCounter = 0;
    this.stepCounter = 0;
    this.displayHeights = [];
  }

  resize() {
    const parent = this.canvas.parentElement;
    const rect = parent.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;

    const w = rect.width > 50 ? rect.width : 750;
    const h = rect.height > 50 ? rect.height : 420;

    this.width = w;
    this.height = h;

    this.canvas.width = w * dpr;
    this.canvas.height = h * dpr;
    this.canvas.style.width = `${w}px`;
    this.canvas.style.height = `${h}px`;

    this.ctx.resetTransform?.();
    this.ctx.scale(dpr, dpr);
  }

  resizeAndRender() {
    this.resize();
    if (this.lastStep) this.render(this.lastStep);
  }

  startAnimationLoop() {
    const loop = () => {
      this.pulseAngle = (this.pulseAngle + 0.05) % (Math.PI * 2);

      // Only re-draw frame if actively displaying or animating particles
      if (this.lastStep) {
        if (this.mode === "boxes") {
          this.renderSearching(this.lastStep);
        } else {
          this.renderSorting(this.lastStep);
        }
      }

      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  render(step) {
    this.lastStep = step;

    // Trigger audio feedback
    if (step.swapping?.length >= 2) {
      const v1 = step.array[step.swapping[0]] || 50;
      const v2 = step.array[step.swapping[1]] || 50;
      audioEngine.playSwapChord(v1, v2);
      this.emitSparks(step.swapping);
    } else if (step.comparing?.length > 0) {
      const v = step.array[step.comparing[0]] || 50;
      audioEngine.playTone(v, Math.max(...(step.array || [100])));
    }
  }

  emitSparks(indices) {
    if (!this.width || !this.lastStep?.array) return;
    const padX = 42;
    const availW = this.width - padX - 20;
    const bw = availW / this.lastStep.array.length;

    indices.forEach(idx => {
      const cx = padX + idx * bw + bw / 2;
      for (let k = 0; k < 4; k++) {
        this.particles.push({
          x: cx,
          y: this.height * 0.5 + (Math.random() - 0.5) * 40,
          vx: (Math.random() - 0.5) * 5,
          vy: (Math.random() - 0.5) * 5 - 2,
          r: Math.random() * 3 + 2,
          color: Math.random() > 0.5 ? "#F43F5E" : "#FDE68A",
          alpha: 1,
        });
      }
    });
  }

  // ───────────────────────────────────────────────────────────────────────────
  // Header Strip
  // ───────────────────────────────────────────────────────────────────────────
  drawHeader(algoTitle, subText) {
    const ctx = this.ctx;
    const c = themeManager.colors;
    const w = this.width;

    ctx.fillStyle = c.bg_card;
    ctx.fillRect(0, 0, w, 34);

    ctx.strokeStyle = c.border;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, 34);
    ctx.lineTo(w, 34);
    ctx.stroke();

    ctx.fillStyle = c.fg_primary;
    ctx.font = "bold 13px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    ctx.fillText(algoTitle, 14, 17);

    if (subText) {
      ctx.fillStyle = c.fg_secondary;
      ctx.font = "11px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
      ctx.textAlign = "right";
      ctx.fillText(subText, w - 12, 17);
    }

    return 38;
  }

  // ───────────────────────────────────────────────────────────────────────────
  // Pointer Badge with gentle floating wave
  // ───────────────────────────────────────────────────────────────────────────
  drawPointerBadge(cx, tipY, name) {
    const ptr = PTR_COLORS[name];
    if (!ptr) return;
    const ctx = this.ctx;
    const { color, label } = ptr;

    // Gentle float wave
    const floatOffset = Math.sin(this.pulseAngle * 2 + cx * 0.05) * 2;
    const actualTipY = tipY + floatOffset;

    const pw = Math.max(10, label.length * 4 + 6);
    const boxH = 15;
    const topY = actualTipY - 20;

    // Glow aura around badge
    ctx.save();
    ctx.shadowColor = color;
    ctx.shadowBlur = 8;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(cx - pw, topY, pw * 2, boxH, 3);
    ctx.fill();

    // Arrow pointer
    ctx.beginPath();
    ctx.moveTo(cx - 3, topY + boxH);
    ctx.lineTo(cx + 3, topY + boxH);
    ctx.lineTo(cx, actualTipY);
    ctx.closePath();
    ctx.fill();
    ctx.restore();

    ctx.fillStyle = "#FFFFFF";
    ctx.font = "bold 9px Menlo, monospace";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(label, cx, topY + boxH / 2);
  }

  // ───────────────────────────────────────────────────────────────────────────
  // Sorting Render (Fluid 60FPS with Gradients & Glows)
  // ───────────────────────────────────────────────────────────────────────────
  renderSorting(step) {
    const ctx = this.ctx;
    const c = themeManager.colors;
    const w = this.width;
    const h = this.height;
    const arr = step.array;

    ctx.fillStyle = c.bg_canvas;
    ctx.fillRect(0, 0, w, h);

    if (!arr || !arr.length) return;

    const sub = `Cmps: ${this.cmpCounter}  |  Steps: ${this.stepCounter}`;
    const padTop = this.drawHeader(this.algoName || "Sorting", sub);

    const padX = 42;
    const padBot = 48;
    const n = arr.length;
    const maxVal = Math.max(...arr, 1);
    const availW = w - padX - 20;
    const availH = h - padTop - padBot;
    const bw = availW / n;
    const y1 = h - padBot;

    // Y-axis gridlines & ticks
    ctx.textAlign = "right";
    ctx.textBaseline = "middle";
    for (const [pct, lbl] of [[1.0, "100"], [0.75, "75"], [0.5, "50"], [0.25, "25"], [0.0, "0"]]) {
      const gy = y1 - availH * pct;
      if (pct > 0) {
        ctx.strokeStyle = c.border;
        ctx.lineWidth = 1;
        ctx.setLineDash([2, 5]);
        ctx.beginPath();
        ctx.moveTo(padX, gy);
        ctx.lineTo(w - 20, gy);
        ctx.stroke();
        ctx.setLineDash([]);
      }
      ctx.fillStyle = c.fg_dim;
      ctx.font = "10px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.fillText(lbl, padX - 8, gy);
    }

    // Ground line with subtle neon gradient
    const groundGrad = ctx.createLinearGradient(padX, 0, w - 20, 0);
    groundGrad.addColorStop(0, c.border);
    groundGrad.addColorStop(0.5, c.accent);
    groundGrad.addColorStop(1, c.border);
    ctx.strokeStyle = groundGrad;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(padX - 4, y1);
    ctx.lineTo(w - 20, y1);
    ctx.stroke();

    const gap = bw >= 12 ? Math.max(2, Math.floor(bw * 0.12)) : 1;

    // Sorted partition background tint
    if (step.sorted_indices?.length) {
      const sortedSet = new Set(step.sorted_indices);
      const run = [];
      for (let i = n - 1; i >= 0; i--) {
        if (sortedSet.has(i)) run.push(i);
        else break;
      }
      if (run.length >= 2) {
        const rx0 = padX + Math.min(...run) * bw;
        const rx1 = padX + (Math.max(...run) + 1) * bw;
        const partGrad = ctx.createLinearGradient(rx0, padTop, rx0, y1);
        partGrad.addColorStop(0, themeManager.currentTheme === "dark" ? "rgba(16, 185, 129, 0.08)" : "rgba(16, 185, 129, 0.12)");
        partGrad.addColorStop(1, "rgba(16, 185, 129, 0.02)");
        ctx.fillStyle = partGrad;
        ctx.fillRect(rx0, padTop, rx1 - rx0, y1 - padTop);
      }
    }

    // Pivot dashed line
    if (step.pivot_index !== null && step.pivot_index >= 0 && step.pivot_index < n) {
      const pvY = y1 - (arr[step.pivot_index] / maxVal) * availH;
      ctx.strokeStyle = c.bar_pivot;
      ctx.lineWidth = 1.5;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(padX, pvY);
      ctx.lineTo(w - 20, pvY);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = c.bar_pivot;
      ctx.font = "bold 9px Menlo, monospace";
      ctx.textAlign = "right";
      ctx.fillText("pivot", w - 24, pvY - 6);
    }

    const barTops = {};

    // Render bars with multi-stop gradients and rounded top caps
    for (let idx = 0; idx < n; idx++) {
      const val = arr[idx];
      const isSwp = step.swapping?.includes(idx);
      const isCmp = step.comparing?.includes(idx);
      const isSrt = step.sorted_indices?.includes(idx);
      const isPvt = step.pivot_index === idx;

      const targetH = (val / maxVal) * availH;
      // Initialize or smoothly interpolate display heights
      if (this.displayHeights[idx] === undefined) {
        this.displayHeights[idx] = targetH;
      } else {
        this.displayHeights[idx] += (targetH - this.displayHeights[idx]) * 0.35;
      }
      const barH = Math.max(3, this.displayHeights[idx]);

      const x0 = padX + idx * bw + gap / 2;
      const x1 = padX + (idx + 1) * bw - gap / 2;
      const barW = Math.max(2, x1 - x0);
      const y0 = y1 - barH;
      barTops[idx] = { cx: (x0 + x1) / 2, y0 };

      // Create rich vertical bar gradient
      const barGrad = ctx.createLinearGradient(x0, y0, x0, y1);
      if (isSwp) {
        barGrad.addColorStop(0, "#FDA4AF");
        barGrad.addColorStop(0.3, "#F43F5E");
        barGrad.addColorStop(1, "#881337");
      } else if (isCmp) {
        barGrad.addColorStop(0, "#FDE68A");
        barGrad.addColorStop(0.3, "#F59E0B");
        barGrad.addColorStop(1, "#78350F");
      } else if (isSrt) {
        barGrad.addColorStop(0, "#6EE7B7");
        barGrad.addColorStop(0.3, "#10B981");
        barGrad.addColorStop(1, "#064E3B");
      } else if (isPvt) {
        barGrad.addColorStop(0, "#67E8F9");
        barGrad.addColorStop(0.3, "#06B6D4");
        barGrad.addColorStop(1, "#164E63");
      } else {
        barGrad.addColorStop(0, c.bar_cap_default || "#93C5FD");
        barGrad.addColorStop(0.3, c.bar_default || "#2563EB");
        barGrad.addColorStop(1, themeManager.currentTheme === "dark" ? "#1E3A8A" : "#1D4ED8");
      }

      // Draw rounded top bar
      ctx.save();
      if (isSwp || isCmp || isPvt) {
        // Dynamic glowing aura
        const glowColor = isSwp ? "#F43F5E" : (isCmp ? "#F59E0B" : "#06B6D4");
        const pulse = 6 + Math.sin(this.pulseAngle * 3) * 3;
        ctx.shadowColor = glowColor;
        ctx.shadowBlur = pulse;
      }

      ctx.fillStyle = barGrad;
      ctx.beginPath();
      // Rounded top corners
      const cornerR = Math.min(4, barW / 2);
      ctx.roundRect(x0, y0, barW, barH, [cornerR, cornerR, 0, 0]);
      ctx.fill();
      ctx.restore();

      // Top cap highlight
      if (barH >= 8) {
        ctx.fillStyle = isSwp ? "#FFF1F2" : (isCmp ? "#FFFBEB" : (isSrt ? "#ECFDF5" : "#EFF6FF"));
        ctx.globalAlpha = 0.6;
        ctx.fillRect(x0 + 1, y0, barW - 2, 2);
        ctx.globalAlpha = 1.0;
      }

      // In-bar action badge
      if (barH >= 24 && bw >= 18) {
        const badge = isSwp ? "⇄" : (isCmp ? "CMP" : (isPvt ? "P" : null));
        if (badge) {
          ctx.fillStyle = (isSwp || isPvt) ? "#FFFFFF" : "#0F172A";
          ctx.font = isSwp ? "bold 13px sans-serif" : "bold 9px sans-serif";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(badge, (x0 + x1) / 2, y0 + Math.min(16, barH / 2));
        }
      }

      // Value label above bar
      if (bw >= 14) {
        const cx = (x0 + x1) / 2;
        const lblY = Math.max(padTop + 24, y0 - 12);

        if (isSwp || isCmp) {
          const pillCol = isSwp ? c.bar_swapping : c.bar_comparing;
          ctx.save();
          ctx.shadowColor = pillCol;
          ctx.shadowBlur = 6;
          ctx.fillStyle = pillCol;
          ctx.beginPath();
          ctx.roundRect(cx - 14, lblY - 8, 28, 16, 4);
          ctx.fill();
          ctx.restore();

          ctx.fillStyle = isSwp ? "#FFFFFF" : "#0F172A";
          ctx.font = "bold 10px -apple-system, BlinkMacSystemFont, sans-serif";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(String(val), cx, lblY);
        } else {
          ctx.fillStyle = c.fg_primary;
          ctx.font = "bold 10px -apple-system, BlinkMacSystemFont, sans-serif";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(String(val), cx, lblY);
        }

        // Index below ground line
        ctx.fillStyle = c.fg_secondary;
        ctx.font = "10px -apple-system, BlinkMacSystemFont, sans-serif";
        ctx.fillText(String(idx), cx, y1 + 12);
      }
    }

    // Animated Flowing Arches between compared / swapped pairs
    const drawArch = (i1, i2, col, label, isSwap) => {
      const p1 = barTops[i1];
      const p2 = barTops[i2];
      if (!p1 || !p2) return;

      const archTop = Math.min(p1.y0, p2.y0) - 24;
      const midX = (p1.cx + p2.cx) / 2;

      ctx.save();
      ctx.shadowColor = col;
      ctx.shadowBlur = 8;
      ctx.strokeStyle = col;
      ctx.lineWidth = isSwap ? 2.5 : 2;
      // Flowing dashed animation
      ctx.setLineDash([4, 3]);
      ctx.lineDashOffset = -Date.now() / 25;

      ctx.beginPath();
      ctx.moveTo(p1.cx, p1.y0 - 4);
      ctx.quadraticCurveTo(midX, archTop, p2.cx, p2.y0 - 4);
      ctx.stroke();
      ctx.restore();

      const pillW = isSwap ? 72 : 64;
      ctx.fillStyle = isSwap ? col : c.bg_card;
      ctx.beginPath();
      ctx.roundRect(midX - pillW / 2, archTop - 9, pillW, 18, 5);
      ctx.fill();

      if (!isSwap) {
        ctx.strokeStyle = col;
        ctx.lineWidth = 1.5;
        ctx.stroke();
      }

      ctx.fillStyle = isSwap ? "#FFFFFF" : c.fg_primary;
      ctx.font = "bold 10px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(label, midX, archTop);
    };

    if (step.swapping?.length >= 2) {
      drawArch(step.swapping[0], step.swapping[1], c.bar_swapping, "⟷ SWAP", true);
    } else if (step.comparing?.length >= 2) {
      const v1 = arr[step.comparing[0]];
      const v2 = arr[step.comparing[1]];
      const op = v1 > v2 ? ">" : (v1 < v2 ? "<" : "=");
      drawArch(step.comparing[0], step.comparing[1], c.bar_comparing, `${v1} ${op} ${v2}`, false);
    }

    // Pointer badges above
    for (const [name, idx] of Object.entries(step.pointers || {})) {
      if (idx >= 0 && idx < n) {
        const cx = padX + idx * bw + bw / 2;
        this.drawPointerBadge(cx, padTop + 24, name);
      }
    }

    // Animate & draw spark particles
    this.renderParticles();

    // Compact bottom legend
    this.drawLegend(w, h - 14);
  }

  // ───────────────────────────────────────────────────────────────────────────
  // Searching Render (With Sonar Pings & Highlight Rays)
  // ───────────────────────────────────────────────────────────────────────────
  renderSearching(step) {
    const ctx = this.ctx;
    const c = themeManager.colors;
    const w = this.width;
    const h = this.height;
    const arr = step.array;

    ctx.fillStyle = c.bg_canvas;
    ctx.fillRect(0, 0, w, h);

    if (!arr || !arr.length) return;

    const tgt = step.target !== null ? `Target: ${step.target}  |  ` : "";
    const sub = `${tgt}Probe #${this.cmpCounter}`;
    const padTop = this.drawHeader(this.algoName || "Searching", sub);

    const n = arr.length;
    const boxW = Math.min(54, Math.max(28, (w - 60) / n));
    const boxH = boxW * 1.15;
    const totalW = n * boxW;
    const startX = Math.max(20, (w - totalW) / 2);
    const cy = (h - padTop) / 2 + padTop - 10;

    const rLo = step.range_low ?? -1;
    const rHi = step.range_high ?? -1;

    // Active range background highlight with animated border
    if (rLo >= 0 && rHi >= 0 && rLo <= rHi) {
      const rx0 = startX + rLo * boxW;
      const rx1 = startX + (rHi + 1) * boxW;
      const rangeGrad = ctx.createLinearGradient(rx0, cy - boxH / 2, rx1, cy + boxH / 2);
      rangeGrad.addColorStop(0, "rgba(59, 130, 246, 0.1)");
      rangeGrad.addColorStop(1, "rgba(6, 182, 212, 0.05)");

      ctx.fillStyle = rangeGrad;
      ctx.fillRect(rx0 - 2, cy - boxH / 2 - 4, (rx1 - rx0) + 4, boxH + 8);

      ctx.save();
      ctx.strokeStyle = c.accent;
      ctx.lineWidth = 1.5;
      ctx.setLineDash([4, 4]);
      ctx.lineDashOffset = -Date.now() / 40;
      ctx.strokeRect(rx0 - 2, cy - boxH / 2 - 4, (rx1 - rx0) + 4, boxH + 8);
      ctx.restore();
    }

    for (let i = 0; i < n; i++) {
      const val = arr[i];
      const isFound = step.found_index === i;
      const isCmp = step.comparing?.includes(i);
      let isElim = step.eliminated_indices?.includes(i);

      if (rLo >= 0 && rHi >= 0 && (i < rLo || i > rHi) && !isFound) {
        isElim = true;
      }

      const x0 = startX + i * boxW + 3;
      const x1 = startX + (i + 1) * boxW - 3;
      const y0 = cy - boxH / 2;
      const y1 = cy + boxH / 2;
      const cardW = x1 - x0;

      let fill = c.bg_card;
      let bdr = c.border;
      if (isFound) {
        fill = c.bar_sorted;
        bdr = c.fg_primary;
      } else if (isCmp) {
        fill = c.bar_comparing;
        bdr = c.accent;
      } else if (isElim) {
        fill = c.bar_eliminated;
        bdr = c.border;
      }

      // Box body with rounded corners
      ctx.save();
      if (isCmp) {
        // Sonar radar pulse ring
        const pingR = (Date.now() / 20) % (boxW * 0.8);
        ctx.strokeStyle = "rgba(245, 158, 11, " + (1 - pingR / (boxW * 0.8)) + ")";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc((x0 + x1) / 2, cy, boxH / 2 + pingR, 0, Math.PI * 2);
        ctx.stroke();

        ctx.shadowColor = c.bar_comparing;
        ctx.shadowBlur = 10;
      } else if (isFound) {
        ctx.shadowColor = c.bar_sorted;
        ctx.shadowBlur = 15;
      }

      ctx.fillStyle = fill;
      ctx.beginPath();
      ctx.roundRect(x0, y0, cardW, boxH, 6);
      ctx.fill();

      ctx.strokeStyle = bdr;
      ctx.lineWidth = (isFound || isCmp) ? 2 : 1;
      ctx.stroke();
      ctx.restore();

      // Top cap highlight
      if (!isElim) {
        const cap = isFound ? c.bar_cap_sorted : (isCmp ? c.bar_cap_comparing : c.bar_cap_default);
        ctx.fillStyle = cap;
        ctx.beginPath();
        ctx.roundRect(x0, y0, cardW, 3, [6, 6, 0, 0]);
        ctx.fill();
      }

      // Diagonal strikethrough on eliminated
      if (isElim) {
        ctx.strokeStyle = c.border;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(x0 + 4, y0 + 4);
        ctx.lineTo(x1 - 4, y1 - 4);
        ctx.moveTo(x1 - 4, y0 + 4);
        ctx.lineTo(x0 + 4, y1 - 4);
        ctx.stroke();
      }

      // Found badge / pulse ring
      if (isFound) {
        ctx.fillStyle = c.bar_sorted;
        ctx.font = "bold 10px sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "bottom";
        ctx.fillText("✓ FOUND", (x0 + x1) / 2, y0 - 4);
      } else if (isCmp) {
        ctx.fillStyle = c.bar_comparing;
        ctx.font = "bold 9px sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "bottom";
        ctx.fillText("PROBE", (x0 + x1) / 2, y0 - 4);
      }

      // Value text
      const txtColor = (isCmp && themeManager.currentTheme === "dark") ? "#000000" : (isElim ? c.fg_dim : c.fg_primary);
      ctx.fillStyle = txtColor;
      ctx.font = "bold 13px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(String(val), (x0 + x1) / 2, cy + 2);

      // Index label
      ctx.fillStyle = c.fg_secondary;
      ctx.font = "10px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.fillText(`[${i}]`, (x0 + x1) / 2, y1 + 14);
    }

    // Range bracket
    if (rLo >= 0 && rHi >= 0 && rLo <= rHi) {
      const bx0 = startX + rLo * boxW + 3;
      const bx1 = startX + (rHi + 1) * boxW - 3;
      const by = cy + boxH / 2 + 28;

      ctx.strokeStyle = c.accent;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(bx0, by - 8);
      ctx.lineTo(bx0, by);
      ctx.lineTo(bx1, by);
      ctx.lineTo(bx1, by - 8);
      ctx.stroke();

      ctx.fillStyle = c.accent;
      ctx.font = "bold 10px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "top";
      ctx.fillText(`Active Range  [${rLo} … ${rHi}]`, (bx0 + bx1) / 2, by + 4);
    }

    // Pointers
    for (const [name, idx] of Object.entries(step.pointers || {})) {
      if (idx >= 0 && idx < n) {
        const cx2 = startX + idx * boxW + boxW / 2;
        this.drawPointerBadge(cx2, cy - boxH / 2 - 8, name);
      }
    }
  }

  // ───────────────────────────────────────────────────────────────────────────
  // Particle Sparks
  // ───────────────────────────────────────────────────────────────────────────
  renderParticles() {
    const ctx = this.ctx;
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.alpha -= 0.03;

      if (p.alpha <= 0) {
        this.particles.splice(i, 1);
        continue;
      }

      ctx.save();
      ctx.globalAlpha = p.alpha;
      ctx.fillStyle = p.color;
      ctx.shadowColor = p.color;
      ctx.shadowBlur = 6;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  // ───────────────────────────────────────────────────────────────────────────
  // Legend
  // ───────────────────────────────────────────────────────────────────────────
  drawLegend(w, y) {
    const ctx = this.ctx;
    const c = themeManager.colors;
    const items = [
      { label: "Default", color: c.bar_default },
      { label: "Comparing", color: c.bar_comparing },
      { label: "Swapping", color: c.bar_swapping },
      { label: "Sorted", color: c.bar_sorted },
    ];
    const itemW = 90;
    const startX = (w - items.length * itemW) / 2;

    ctx.textAlign = "left";
    ctx.textBaseline = "middle";

    items.forEach((item, i) => {
      const x = startX + i * itemW;
      ctx.fillStyle = item.color;
      ctx.beginPath();
      ctx.arc(x + 4, y, 4, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = c.fg_secondary;
      ctx.font = "10px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.fillText(item.label, x + 14, y);
    });
  }

  // ───────────────────────────────────────────────────────────────────────────
  // Confetti Particle Celebration
  // ───────────────────────────────────────────────────────────────────────────
  launchConfetti(count = 70) {
    const pal = ["#2563EB", "#10B981", "#F59E0B", "#F43F5E", "#06B6D4", "#8B5CF6"];
    this.confettiParticles = Array.from({ length: count }, () => ({
      x: Math.random() * this.width,
      y: Math.random() * (this.height * 0.4),
      r: Math.random() * 4 + 3,
      color: pal[Math.floor(Math.random() * pal.length)],
      vx: (Math.random() - 0.5) * 4,
      vy: Math.random() * 3 + 2,
      tilt: Math.random() * 10,
      tiltAngle: 0,
      tiltAngleInc: Math.random() * 0.1 + 0.05,
    }));

    if (this.confettiAnimId) cancelAnimationFrame(this.confettiAnimId);

    const animate = () => {
      const ctx = this.ctx;
      let active = false;

      this.confettiParticles.forEach(p => {
        p.tiltAngle += p.tiltAngleInc;
        p.y += p.vy;
        p.x += Math.sin(p.tiltAngle) * 2;

        if (p.y < this.height) {
          active = true;
          ctx.fillStyle = p.color;
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fill();
        }
      });

      if (active) {
        this.confettiAnimId = requestAnimationFrame(animate);
      }
    };
    animate();
  }
}
