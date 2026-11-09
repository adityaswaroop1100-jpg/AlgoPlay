"""
widgets.py — macOS-Compatible Flat Button for AlgoPlay.

FlatButton wraps tk.Label with mouse-event bindings to guarantee bg/fg
colour rendering on macOS Tk 9.0 with hover glowing and tactile press animations.
"""

import tkinter as tk
from typing import Callable, Optional
from theme import FONTS


def _lighten(hex_c: str, p: float = 0.22) -> str:
    """Blend hex_c toward #FFFFFF by fraction p."""
    r, g, b = int(hex_c[1:3], 16), int(hex_c[3:5], 16), int(hex_c[5:7], 16)
    return (f"#{min(255, int(r+(255-r)*p)):02x}"
            f"{min(255, int(g+(255-g)*p)):02x}"
            f"{min(255, int(b+(255-b)*p)):02x}")


def _darken(hex_c: str, p: float = 0.25) -> str:
    """Blend hex_c toward #000000 by fraction p."""
    r, g, b = int(hex_c[1:3], 16), int(hex_c[3:5], 16), int(hex_c[5:7], 16)
    return (f"#{max(0, int(r*(1-p))):02x}"
            f"{max(0, int(g*(1-p))):02x}"
            f"{max(0, int(b*(1-p))):02x}")


class FlatButton(tk.Label):
    """Pixel-accurate button built on tk.Label with hover glow & press feedback."""

    def __init__(
        self,
        parent: tk.Widget,
        text: str = "",
        font=None,
        bg: str = "#334155",
        fg: str = "#FFFFFF",
        hover_bg: Optional[str] = None,
        padx: int = 12,
        pady: int = 5,
        command: Optional[Callable] = None,
        **kwargs,
    ) -> None:
        kwargs.setdefault("cursor", "hand2")
        kwargs.setdefault("relief", "flat")
        bdr = kwargs.pop("highlightbackground", _lighten(bg, 0.12) if bg.startswith("#") and bg != "#000000" else "#222D42")
        kwargs.setdefault("highlightthickness", 1)
        kwargs.setdefault("highlightbackground", bdr)
        super().__init__(
            parent, text=text,
            font=font or FONTS["body_bold"],
            bg=bg, fg=fg, padx=padx, pady=pady,
            **kwargs,
        )
        self._bg = bg
        self._fg = fg
        self._border_col = bdr
        self._hover_bg = hover_bg or _lighten(bg, 0.18)
        self._press_bg = _darken(bg, 0.15)
        self._command = command
        self._disabled = False

        self.bind("<ButtonPress-1>",   lambda _: self._press(True))
        self.bind("<ButtonRelease-1>", lambda _: (self._press(False), self._fire()))
        self.bind("<Enter>",          lambda _: self._glow(True))
        self.bind("<Leave>",          lambda _: self._glow(False))

    def _fire(self) -> None:
        if not self._disabled and self._command:
            self._command()

    def _glow(self, on: bool) -> None:
        if not self._disabled:
            bdr = _lighten(self._border_col, 0.35) if on else self._border_col
            tk.Label.configure(self, bg=self._hover_bg if on else self._bg, highlightbackground=bdr)

    def _press(self, down: bool) -> None:
        if not self._disabled:
            tk.Label.configure(self, bg=self._press_bg if down else self._hover_bg)

    def config(self, **kw) -> None:  # type: ignore[override]
        if "command" in kw: self._command = kw.pop("command")
        if "state" in kw:
            s = kw.pop("state"); self._disabled = (s == "disabled")
            eff_bg = _darken(self._bg, 0.30) if self._disabled else self._bg
            eff_fg = "#4A5568"                 if self._disabled else self._fg
            tk.Label.configure(self, bg=eff_bg, fg=eff_fg)
        if "bg" in kw:
            self._bg = kw.pop("bg")
            self._hover_bg = _lighten(self._bg, 0.20)
            self._press_bg = _darken(self._bg, 0.15)
            self._border_col = _lighten(self._bg, 0.12) if self._bg.startswith("#") else "#222D42"
            tk.Label.configure(self, bg=_darken(self._bg, 0.30) if self._disabled else self._bg, highlightbackground=self._border_col)
        if "fg" in kw:
            self._fg = kw.pop("fg")
            if not self._disabled: tk.Label.configure(self, fg=self._fg)
        if kw: tk.Label.configure(self, **kw)

    configure = config
