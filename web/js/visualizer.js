// visualizer.js - HTML5 Canvas Rendering Engine for AlgoPlay Web

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

export class VisualizerCanvas {
  constructor(canvasElement, mode = "bars") {
    this.canvas = canvasElement;
    this.ctx = canvasElement.getContext("2d");
    this.mode = mode;
    this.lastStep = null;
    this.algoName = "";
    this.cmpCounter = 0;
    this.stepCounter = 0;
    this.confettiParticles = [];
    this.confettiAnimId = null;

    this.resizeObserver = new ResizeObserver(() => this.resizeAndRender());
    this.resizeObserver.observe(this.canvas.parentElement);

    themeManager.subscribe(() => {
      if (this.lastStep) {
        this.render(this.lastStep);
      }
    });

    this.resize();
  }

  setAlgoName(name) {
    this.algoName = name;
  }

  resetCounters() {
    this.cmpCounter = 0;
    this.stepCounter = 0;
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
    if (this.lastStep) {
      this.render(this.lastStep);
    }
  }

  render(step) {
    this.lastStep = step;
    if (this.mode === "boxes") {
      this.renderSearching(step);
    } else {
      this.renderSorting(step);
    }
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

    return 38; // padTop
  }

  // ───────────────────────────────────────────────────────────────────────────
  // Pointer Badge
  // ───────────────────────────────────────────────────────────────────────────
  drawPointerBadge(cx, tipY, name) {
    const ptr = PTR_COLORS[name];
    if (!ptr) return;
    const ctx = this.ctx;
    const { color, label } = ptr;

    const pw = Math.max(10, label.length * 4 + 6);
    const boxH = 15;
    const topY = tipY - 20;

    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(cx - pw, topY, pw * 2, boxH, 3);
    ctx.fill();

    // Arrow pointer
    ctx.beginPath();
    ctx.moveTo(cx - 3, topY + boxH);
    ctx.lineTo(cx + 3, topY + boxH);
    ctx.lineTo(cx, tipY);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = "#FFFFFF";
    ctx.font = "bold 9px Menlo, monospace";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(label, cx, topY + boxH / 2);
  }

  // ───────────────────────────────────────────────────────────────────────────
  // Sorting Render
  // ───────────────────────────────────────────────────────────────────────────
  renderSorting(step) {
    if (step.comparing?.length) this.cmpCounter++;
    if (step.swapping?.length || step.comparing?.length) this.stepCounter++;

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

    // Ground baseline
    ctx.strokeStyle = c.border;
    ctx.lineWidth = 1;
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
        ctx.fillStyle = themeManager.currentTheme === "dark" ? "#061A10" : "#E8F5E9";
        ctx.fillRect(rx0, padTop, rx1 - rx0, y1 - padTop);
      }
    }

    // Pivot dashed line
    if (step.pivot_index !== null && step.pivot_index >= 0 && step.pivot_index < n) {
      const pvY = y1 - (arr[step.pivot_index] / maxVal) * availH;
      ctx.strokeStyle = c.bar_pivot;
      ctx.lineWidth = 1;
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

    // Draw bars
    for (let idx = 0; idx < n; idx++) {
      const val = arr[idx];
      const isSwp = step.swapping?.includes(idx);
      const isCmp = step.comparing?.includes(idx);
      const isSrt = step.sorted_indices?.includes(idx);
      const isPvt = step.pivot_index === idx;

      let fill = c.bar_default;
      let cap = c.bar_cap_default;

      if (isSwp) {
        fill = c.bar_swapping;
        cap = c.bar_cap_swapping;
      } else if (isCmp) {
        fill = c.bar_comparing;
        cap = c.bar_cap_comparing;
      } else if (isSrt) {
        fill = c.bar_sorted;
        cap = c.bar_cap_sorted;
      } else if (isPvt) {
        fill = c.bar_pivot;
        cap = c.bar_cap_pivot;
      }

      const barH = (val / maxVal) * availH;
      const x0 = padX + idx * bw + gap / 2;
      const x1 = padX + (idx + 1) * bw - gap / 2;
      const y0 = y1 - barH;
      barTops[idx] = { cx: (x0 + x1) / 2, y0 };

      // Bar body
      ctx.fillStyle = fill;
      ctx.fillRect(x0, y0, x1 - x0, barH);

      // Top cap highlight
      if (barH >= 6) {
        ctx.fillStyle = cap;
        ctx.fillRect(x0, y0, x1 - x0, 3);
      }

      // Double-ring glow on comparing / swapping
      if (isSwp) {
        ctx.strokeStyle = "#FDA4AF";
        ctx.lineWidth = 1;
        ctx.strokeRect(x0 - 2, y0 - 2, (x1 - x0) + 4, barH + 2);
        ctx.strokeStyle = c.bar_swapping;
        ctx.lineWidth = 2;
        ctx.strokeRect(x0 - 1, y0 - 1, (x1 - x0) + 2, barH + 1);
      } else if (isCmp) {
        ctx.strokeStyle = "#FDE68A";
        ctx.lineWidth = 1;
        ctx.strokeRect(x0 - 2, y0 - 2, (x1 - x0) + 4, barH + 2);
        ctx.strokeStyle = c.bar_comparing;
        ctx.lineWidth = 2;
        ctx.strokeRect(x0 - 1, y0 - 1, (x1 - x0) + 2, barH + 1);
      } else if (isPvt) {
        ctx.strokeStyle = c.bar_pivot;
        ctx.lineWidth = 2;
        ctx.strokeRect(x0 - 1, y0 - 1, (x1 - x0) + 2, barH + 1);
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
          ctx.fillStyle = fill;
          ctx.beginPath();
          ctx.roundRect(cx - 14, lblY - 8, 28, 16, 4);
          ctx.fill();

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

    // Comparison / Swap Arches
    const drawArch = (i1, i2, col, label, isSwap) => {
      const p1 = barTops[i1];
      const p2 = barTops[i2];
      if (!p1 || !p2) return;

      const archTop = Math.min(p1.y0, p2.y0) - 22;
      const midX = (p1.cx + p2.cx) / 2;

      ctx.strokeStyle = col;
      ctx.lineWidth = isSwap ? 2.5 : 2;
      ctx.setLineDash([3, 2]);
      ctx.beginPath();
      ctx.moveTo(p1.cx, p1.y0 - 4);
      ctx.quadraticCurveTo(midX, archTop, p2.cx, p2.y0 - 4);
      ctx.stroke();
      ctx.setLineDash([]);

      const pillW = isSwap ? 68 : 62;
      ctx.fillStyle = isSwap ? col : c.bg_card;
      ctx.beginPath();
      ctx.roundRect(midX - pillW / 2, archTop - 9, pillW, 18, 4);
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

    // Compact bottom legend
    this.drawLegend(w, h - 14);
  }

  // ───────────────────────────────────────────────────────────────────────────
  // Searching Render
  // ───────────────────────────────────────────────────────────────────────────
  renderSearching(step) {
    if (step.comparing?.length) this.cmpCounter++;
    this.stepCounter++;

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

    // Active range background highlight
    if (rLo >= 0 && rHi >= 0 && rLo <= rHi) {
      const rx0 = startX + rLo * boxW;
      const rx1 = startX + (rHi + 1) * boxW;
      ctx.fillStyle = themeManager.currentTheme === "dark" ? "#0A1520" : "#E0F2FE";
      ctx.fillRect(rx0 - 2, cy - boxH / 2 - 4, (rx1 - rx0) + 4, boxH + 8);
      ctx.strokeStyle = c.accent;
      ctx.lineWidth = 1;
      ctx.setLineDash([3, 3]);
      ctx.strokeRect(rx0 - 2, cy - boxH / 2 - 4, (rx1 - rx0) + 4, boxH + 8);
      ctx.setLineDash([]);
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
      const bw2 = (isFound || isCmp) ? 2 : 1;

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

      // Box body
      ctx.fillStyle = fill;
      ctx.fillRect(x0, y0, x1 - x0, boxH);
      ctx.strokeStyle = bdr;
      ctx.lineWidth = bw2;
      ctx.strokeRect(x0, y0, x1 - x0, boxH);

      // Top cap highlight
      if (!isElim) {
        const cap = isFound ? c.bar_cap_sorted : (isCmp ? c.bar_cap_comparing : c.bar_cap_default);
        ctx.fillStyle = cap;
        ctx.fillRect(x0, y0, x1 - x0, 3);
      }

      // Strikethrough on eliminated
      if (isElim) {
        ctx.strokeStyle = c.border;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(x0 + 2, y0 + 2);
        ctx.lineTo(x1 - 2, y1 - 2);
        ctx.moveTo(x1 - 2, y0 + 2);
        ctx.lineTo(x0 + 2, y1 - 2);
        ctx.stroke();
      }

      // Found badge / pulse ring
      if (isFound) {
        ctx.strokeStyle = c.bar_sorted;
        ctx.lineWidth = 2;
        ctx.strokeRect(x0 - 4, y0 - 4, (x1 - x0) + 8, boxH + 8);

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
