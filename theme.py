"""
theme.py - Theme & Palette Management for AlgoPlay.

Professional palettes inspired by Linear, Vercel, and Raycast design systems.
Dark: deep cool-black surfaces with precise contrast and vivid purposeful data colors.
Light: clean warm-white with crisp ink contrast — both feel polished, not vibe-coded.
"""

from typing import Callable, Dict, List


THEMES: Dict[str, Dict[str, str]] = {
    "dark": {
        # ── Surfaces (cool-neutral ink blacks, not blue-grey) ────────────────
        "bg_root":       "#0A0A0F",   # True near-black, slightly cool
        "bg_card":       "#111118",   # Elevated surface — 1 step lighter
        "bg_card_inner": "#0D0D13",   # Recessed inset well
        "bg_canvas":     "#0D0D13",   # Visualizer canvas
        "bg_code":       "#0D0D13",   # Pseudocode panel
        "border":        "#1C1C28",   # Barely-visible hairline
        "border_focus":  "#3B82F6",   # Keyboard-focus ring

        # ── Typography ──────────────────────────────────────────────────────
        "fg_primary":   "#EEEEF2",   # Off-white — easier on eyes than pure white
        "fg_secondary": "#7E7E9A",   # Cool mid-grey, legible but recessed
        "fg_dim":       "#44445A",   # Truly dim — grid labels, indices

        # ── Controls ────────────────────────────────────────────────────────
        "accent":           "#3B82F6",   # Bright, clean blue (not neon, not dull)
        "accent_hover":     "#2563EB",
        "accent_fg":        "#FFFFFF",
        "btn_secondary_bg": "#18181F",   # Dark glass button
        "btn_secondary_fg": "#C8C8DC",   # Soft lavender-white
        "entry_bg":         "#09090E",
        "entry_fg":         "#EEEEF2",
        "entry_border":     "#252535",

        # ── Data Bar Colors (vivid, distinct, harmonious) ───────────────────
        # Default: a confident cobalt blue with bright sky cap
        "bar_default":        "#2563EB",
        "bar_cap_default":    "#93C5FD",

        # Comparing: rich saffron-gold — immediately reads "attention"
        "bar_comparing":      "#F59E0B",
        "bar_cap_comparing":  "#FDE68A",

        # Swapping: saturated coral-red — danger/action signal
        "bar_swapping":       "#F43F5E",
        "bar_cap_swapping":   "#FDA4AF",

        # Sorted: deep emerald — calm success signal
        "bar_sorted":         "#10B981",
        "bar_cap_sorted":     "#6EE7B7",

        # Pivot: cyan-teal — clearly distinct from blue/green/red
        "bar_pivot":          "#06B6D4",
        "bar_cap_pivot":      "#67E8F9",

        # Target / eliminated
        "bar_target":         "#818CF8",   # Soft indigo accent (search target)
        "bar_eliminated":     "#16161E",   # Almost invisible — intentionally faded
        "bar_text":           "#EEEEF2",

        # ── Complexity Badges ───────────────────────────────────────────────
        "badge_best_bg":      "#052E16",
        "badge_best_fg":      "#34D399",
        "badge_best_border":  "#064E3B",
        "badge_avg_bg":       "#0C1A3B",
        "badge_avg_fg":       "#60A5FA",
        "badge_avg_border":   "#1E3A6E",
        "badge_worst_bg":     "#2C0A14",
        "badge_worst_fg":     "#FB7185",
        "badge_worst_border": "#881337",
        "badge_space_bg":     "#1C1300",
        "badge_space_fg":     "#FCD34D",
        "badge_space_border": "#78350F",

        # ── Code Highlight ──────────────────────────────────────────────────
        "code_highlight_bg": "#0F1F4A",
        "code_highlight_fg": "#93C5FD",

        # ── Semantic ────────────────────────────────────────────────────────
        "success": "#10B981",
        "warning": "#F59E0B",
        "danger":  "#F43F5E",
        "info":    "#3B82F6",
    },

    "light": {
        # ── Surfaces (warm-white, clean paper feel) ──────────────────────────
        "bg_root":       "#F5F5F7",   # Apple-style warm near-white
        "bg_card":       "#FFFFFF",
        "bg_card_inner": "#F0F0F5",
        "bg_canvas":     "#FAFAFE",
        "bg_code":       "#F7F7FB",
        "border":        "#D8D8E8",
        "border_focus":  "#3B82F6",

        # ── Typography ──────────────────────────────────────────────────────
        "fg_primary":   "#0C0C14",   # Deep near-black ink
        "fg_secondary": "#5C5C78",   # Cool mid-tone
        "fg_dim":       "#A0A0BC",   # Recessed labels

        # ── Controls ────────────────────────────────────────────────────────
        "accent":           "#2563EB",
        "accent_hover":     "#1D4ED8",
        "accent_fg":        "#FFFFFF",
        "btn_secondary_bg": "#EBEBF3",
        "btn_secondary_fg": "#1A1A2E",
        "entry_bg":         "#FFFFFF",
        "entry_fg":         "#0C0C14",
        "entry_border":     "#C8C8DC",

        # ── Data Bar Colors ─────────────────────────────────────────────────
        "bar_default":        "#3B82F6",
        "bar_cap_default":    "#BFDBFE",

        "bar_comparing":      "#D97706",
        "bar_cap_comparing":  "#FDE68A",

        "bar_swapping":       "#E11D48",
        "bar_cap_swapping":   "#FECDD3",

        "bar_sorted":         "#059669",
        "bar_cap_sorted":     "#A7F3D0",

        "bar_pivot":          "#0891B2",
        "bar_cap_pivot":      "#A5F3FC",

        "bar_target":         "#6366F1",
        "bar_eliminated":     "#E5E5EF",
        "bar_text":           "#0C0C14",

        # ── Complexity Badges ───────────────────────────────────────────────
        "badge_best_bg":      "#DCFCE7",
        "badge_best_fg":      "#15803D",
        "badge_best_border":  "#86EFAC",
        "badge_avg_bg":       "#DBEAFE",
        "badge_avg_fg":       "#1D4ED8",
        "badge_avg_border":   "#93C5FD",
        "badge_worst_bg":     "#FFE4E6",
        "badge_worst_fg":     "#BE123C",
        "badge_worst_border": "#FDA4AF",
        "badge_space_bg":     "#FEF9C3",
        "badge_space_fg":     "#92400E",
        "badge_space_border": "#FDE68A",

        # ── Code Highlight ──────────────────────────────────────────────────
        "code_highlight_bg": "#EFF6FF",
        "code_highlight_fg": "#1D4ED8",

        # ── Semantic ────────────────────────────────────────────────────────
        "success": "#059669",
        "warning": "#D97706",
        "danger":  "#E11D48",
        "info":    "#2563EB",
    },
}


# ── Typography Standards ──────────────────────────────────────────────────────
# Avenir Next gives a clean, premium sans-serif feel on macOS.
# Menlo is used for pseudocode panels (monospaced, great legibility).
FONTS = {
    "display":      ("Avenir Next", 17, "bold"),
    "title":        ("Avenir Next", 14, "bold"),
    "subtitle":     ("Avenir Next", 12, "bold"),
    "body":         ("Avenir Next", 11),
    "body_bold":    ("Avenir Next", 11, "bold"),
    "caption":      ("Avenir Next", 10),
    "caption_bold": ("Avenir Next", 10, "bold"),
    "small":        ("Avenir Next", 9),
    "small_bold":   ("Avenir Next", 9, "bold"),
    "code":         ("Menlo", 10),
    "code_bold":    ("Menlo", 10, "bold"),
}


class ThemeManager:
    """Manages active theme state and notifies registered observer callbacks."""

    def __init__(self, default_theme: str = "dark") -> None:
        self._current_theme: str = default_theme if default_theme in THEMES else "dark"
        self._listeners: List[Callable[[Dict[str, str]], None]] = []

    @property
    def current_theme(self) -> str:
        return self._current_theme

    @property
    def colors(self) -> Dict[str, str]:
        return THEMES[self._current_theme]

    def get(self, key: str, fallback: str = "#000000") -> str:
        return self.colors.get(key, fallback)

    def toggle_theme(self) -> str:
        self._current_theme = "light" if self._current_theme == "dark" else "dark"
        self._notify(); return self._current_theme

    def set_theme(self, theme_name: str) -> None:
        if theme_name in THEMES and theme_name != self._current_theme:
            self._current_theme = theme_name; self._notify()

    def register_listener(self, cb: Callable[[Dict[str, str]], None]) -> None:
        if cb not in self._listeners: self._listeners.append(cb)

    def unregister_listener(self, cb: Callable[[Dict[str, str]], None]) -> None:
        if cb in self._listeners: self._listeners.remove(cb)

    def _notify(self) -> None:
        c = self.colors
        for cb in self._listeners:
            try: cb(c)
            except Exception: pass

    def get_toggle_icon(self) -> str:
        return "☀️ Light" if self._current_theme == "dark" else "🌙 Dark"


theme_manager = ThemeManager(default_theme="dark")
