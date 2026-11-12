// theme.js - Theme & Palette Management for AlgoPlay Web

export const THEMES = {
  dark: {
    bg_root: "#0A0A0F",
    bg_card: "#111118",
    bg_card_inner: "#0D0D13",
    bg_canvas: "#0D0D13",
    bg_code: "#0D0D13",
    border: "#1C1C28",
    border_focus: "#3B82F6",

    fg_primary: "#EEEEF2",
    fg_secondary: "#7E7E9A",
    fg_dim: "#44445A",

    accent: "#3B82F6",
    accent_hover: "#2563EB",
    accent_fg: "#FFFFFF",
    btn_secondary_bg: "#18181F",
    btn_secondary_fg: "#C8C8DC",
    entry_bg: "#09090E",
    entry_fg: "#EEEEF2",
    entry_border: "#252535",

    bar_default: "#2563EB",
    bar_cap_default: "#93C5FD",
    bar_comparing: "#F59E0B",
    bar_cap_comparing: "#FDE68A",
    bar_swapping: "#F43F5E",
    bar_cap_swapping: "#FDA4AF",
    bar_sorted: "#10B981",
    bar_cap_sorted: "#6EE7B7",
    bar_pivot: "#06B6D4",
    bar_cap_pivot: "#67E8F9",
    bar_target: "#818CF8",
    bar_eliminated: "#16161E",
    bar_text: "#EEEEF2",

    badge_best_bg: "#052E16",
    badge_best_fg: "#34D399",
    badge_best_border: "#064E3B",
    badge_avg_bg: "#0C1A3B",
    badge_avg_fg: "#60A5FA",
    badge_avg_border: "#1E3A6E",
    badge_worst_bg: "#2C0A14",
    badge_worst_fg: "#FB7185",
    badge_worst_border: "#881337",
    badge_space_bg: "#1C1300",
    badge_space_fg: "#FCD34D",
    badge_space_border: "#78350F",

    code_highlight_bg: "#0F1F4A",
    code_highlight_fg: "#93C5FD",
  },
  light: {
    bg_root: "#F5F5F7",
    bg_card: "#FFFFFF",
    bg_card_inner: "#F0F0F5",
    bg_canvas: "#FAFAFE",
    bg_code: "#F7F7FB",
    border: "#D8D8E8",
    border_focus: "#3B82F6",

    fg_primary: "#0C0C14",
    fg_secondary: "#5C5C78",
    fg_dim: "#A0A0BC",

    accent: "#2563EB",
    accent_hover: "#1D4ED8",
    accent_fg: "#FFFFFF",
    btn_secondary_bg: "#EBEBF3",
    btn_secondary_fg: "#1A1A2E",
    entry_bg: "#FFFFFF",
    entry_fg: "#0C0C14",
    entry_border: "#C8C8DC",

    bar_default: "#3B82F6",
    bar_cap_default: "#BFDBFE",
    bar_comparing: "#D97706",
    bar_cap_comparing: "#FDE68A",
    bar_swapping: "#E11D48",
    bar_cap_swapping: "#FECDD3",
    bar_sorted: "#059669",
    bar_cap_sorted: "#A7F3D0",
    bar_pivot: "#0891B2",
    bar_cap_pivot: "#A5F3FC",
    bar_target: "#6366F1",
    bar_eliminated: "#E5E5EF",
    bar_text: "#0C0C14",

    badge_best_bg: "#DCFCE7",
    badge_best_fg: "#15803D",
    badge_best_border: "#86EFAC",
    badge_avg_bg: "#DBEAFE",
    badge_avg_fg: "#1D4ED8",
    badge_avg_border: "#93C5FD",
    badge_worst_bg: "#FFE4E6",
    badge_worst_fg: "#BE123C",
    badge_worst_border: "#FDA4AF",
    badge_space_bg: "#FEF9C3",
    badge_space_fg: "#92400E",
    badge_space_border: "#FDE68A",

    code_highlight_bg: "#EFF6FF",
    code_highlight_fg: "#1D4ED8",
  }
};

class ThemeManager {
  constructor() {
    this.currentTheme = localStorage.getItem("algoplay_theme") || "dark";
    this.listeners = [];
  }

  get colors() {
    return THEMES[this.currentTheme];
  }

  toggle() {
    this.currentTheme = this.currentTheme === "dark" ? "light" : "dark";
    localStorage.setItem("algoplay_theme", this.currentTheme);
    this.apply();
    return this.currentTheme;
  }

  subscribe(listener) {
    this.listeners.push(listener);
  }

  apply() {
    const root = document.documentElement;
    const c = this.colors;
    root.setAttribute("data-theme", this.currentTheme);
    for (const [key, val] of Object.entries(c)) {
      root.style.setProperty(`--${key}`, val);
    }
    this.listeners.forEach(fn => fn(c, this.currentTheme));
  }
}

export const themeManager = new ThemeManager();
