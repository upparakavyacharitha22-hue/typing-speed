"""
ui_components.py - Reusable styled UI widgets for TypeMaster Tkinter GUI.
Includes modern dark-themed cards, custom styled buttons with hover effects,
stat badges, and smooth canvas-based progress bars.
"""

import tkinter as tk
from tkinter import font as tkfont
from typing import Callable, Optional, Tuple


# ============================================================================
# DESIGN SYSTEM & COLOR PALETTE
# ============================================================================
COLOR_BG = "#0B0F19"             # Deep Navy / Dark Slate background
COLOR_SURFACE = "#1E293B"        # Card / panel background
COLOR_SURFACE_LIGHT = "#283548"  # Slightly lighter card surface / header
COLOR_SURFACE_HOVER = "#334155"  # Card hover / border highlight
COLOR_BORDER = "#334155"         # Subtle card border
COLOR_BORDER_LIGHT = "#475569"   # Active border

COLOR_PRIMARY = "#6366F1"        # Vibrant Indigo / Purple accent
COLOR_PRIMARY_HOVER = "#4F46E5"  # Darker Indigo for button hover
COLOR_PRIMARY_ACTIVE = "#4338CA" # Pressed state

COLOR_SECONDARY = "#0EA5E9"      # Sky Blue secondary accent
COLOR_SECONDARY_HOVER = "#0284C7"

COLOR_ACCENT_PURPLE = "#8B5CF6"  # Violet accent
COLOR_SUCCESS = "#10B981"        # Emerald Green (correct, high score)
COLOR_SUCCESS_BG = "#064E3B"     # Dark green background tag
COLOR_WARNING = "#F59E0B"        # Amber / Orange (timer low, beginner)
COLOR_DANGER = "#EF4444"         # Rose / Coral Red (mistakes, errors)
COLOR_DANGER_BG = "#451A1A"      # Dark red background tag

COLOR_TEXT_PRIMARY = "#FFFFFF"   # Bright White text
COLOR_TEXT_SECONDARY = "#94A3B8" # Muted Slate secondary text
COLOR_TEXT_MUTED = "#64748B"     # Darker muted helper text
COLOR_INPUT_BG = "#0F172A"       # Deep dark background for typing area


def get_font(family: str = "Segoe UI", size: int = 11, weight: str = "normal", slant: str = "roman"):
    """Safely return a font tuple, defaulting gracefully across operating systems."""
    return (family, size, weight, slant)


class ModernButton(tk.Frame):
    """
    A modern styled flat button with custom hover animations, rounded feel,
    border highlight, and pointer feedback.
    """

    def __init__(
        self,
        parent,
        text: str,
        command: Optional[Callable] = None,
        bg_color: str = COLOR_PRIMARY,
        hover_color: str = COLOR_PRIMARY_HOVER,
        active_color: str = COLOR_PRIMARY_ACTIVE,
        text_color: str = COLOR_TEXT_PRIMARY,
        font_tuple: Tuple = ("Segoe UI", 11, "bold"),
        padx: int = 20,
        pady: int = 10,
        width: Optional[int] = None,
        cursor: str = "hand2",
        **kwargs,
    ):
        super().__init__(parent, bg=bg_color, **kwargs)
        self.command = command
        self.default_bg = bg_color
        self.hover_bg = hover_color
        self.active_bg = active_color
        self.text_color = text_color
        self.is_enabled = True

        self.label = tk.Label(
            self,
            text=text,
            bg=bg_color,
            fg=text_color,
            font=font_tuple,
            cursor=cursor,
            padx=padx,
            pady=pady,
        )
        if width:
            self.label.config(width=width)
        self.label.pack(fill="both", expand=True)

        # Bind hover and click events on both frame and label for smooth UX
        for widget in (self, self.label):
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<Button-1>", self._on_press)
            widget.bind("<ButtonRelease-1>", self._on_release)

    def _on_enter(self, event=None):
        if self.is_enabled:
            self.config(bg=self.hover_bg)
            self.label.config(bg=self.hover_bg)

    def _on_leave(self, event=None):
        if self.is_enabled:
            self.config(bg=self.default_bg)
            self.label.config(bg=self.default_bg)

    def _on_press(self, event=None):
        if self.is_enabled:
            self.config(bg=self.active_bg)
            self.label.config(bg=self.active_bg)

    def _on_release(self, event=None):
        if self.is_enabled:
            self.config(bg=self.hover_bg)
            self.label.config(bg=self.hover_bg)
            if self.command:
                self.command()

    def set_text(self, text: str):
        self.label.config(text=text)

    def set_enabled(self, enabled: bool):
        self.is_enabled = enabled
        if enabled:
            self.config(bg=self.default_bg)
            self.label.config(bg=self.default_bg, fg=self.text_color, cursor="hand2")
        else:
            disabled_bg = "#334155"
            disabled_fg = "#64748B"
            self.config(bg=disabled_bg)
            self.label.config(bg=disabled_bg, fg=disabled_fg, cursor="arrow")


class CardFrame(tk.Frame):
    """A styled card container with subtle borders and dark navy surface."""

    def __init__(
        self,
        parent,
        bg: str = COLOR_SURFACE,
        border_color: str = COLOR_BORDER,
        border_width: int = 1,
        padx: int = 16,
        pady: int = 16,
        **kwargs,
    ):
        super().__init__(
            parent,
            bg=border_color,
            padx=border_width,
            pady=border_width,
            **kwargs,
        )
        self.inner_frame = tk.Frame(self, bg=bg, padx=padx, pady=pady)
        self.inner_frame.pack(fill="both", expand=True)

    @property
    def body(self) -> tk.Frame:
        """Returns the inner frame where child widgets should be packed/gridded."""
        return self.inner_frame


class ModernProgressBar(tk.Canvas):
    """
    A custom canvas-based progress bar supporting smooth progress rendering,
    rounded ends, and custom color states.
    """

    def __init__(
        self,
        parent,
        width: int = 300,
        height: int = 12,
        bg_color: str = "#1E293B",
        fill_color: str = COLOR_PRIMARY,
        **kwargs,
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent["bg"] if "bg" in parent.keys() else COLOR_BG,
            highlightthickness=0,
            **kwargs,
        )
        self.bar_width = width
        self.bar_height = height
        self.track_bg = bg_color
        self.fill_color = fill_color
        self.progress = 1.0  # 0.0 to 1.0
        self.bind("<Configure>", self._on_resize)
        self._draw()

    def _on_resize(self, event):
        self.bar_width = max(10, event.width)
        self.bar_height = max(6, event.height)
        self._draw()

    def set_progress(self, ratio: float, color: Optional[str] = None):
        """Set progress ratio between 0.0 and 1.0, with optional color override."""
        self.progress = max(0.0, min(1.0, ratio))
        if color:
            self.fill_color = color
        self._draw()

    def _draw(self):
        self.delete("all")
        r = self.bar_height // 2
        w = self.bar_width
        h = self.bar_height

        # Draw background track
        self.create_rectangle(0, 0, w, h, fill=self.track_bg, outline="")

        # Draw filled progress
        fill_w = int(w * self.progress)
        if fill_w > 0:
            self.create_rectangle(0, 0, fill_w, h, fill=self.fill_color, outline="")


class StatBadge(tk.Frame):
    """
    A compact live metric badge showing an icon/label, value, and unit.
    Ideal for the live test dashboard.
    """

    def __init__(
        self,
        parent,
        title: str,
        initial_value: str = "0",
        unit: str = "",
        accent_color: str = COLOR_PRIMARY,
        bg_color: str = COLOR_SURFACE,
        width: int = 130,
        **kwargs,
    ):
        super().__init__(
            parent,
            bg=COLOR_BORDER,
            padx=1,
            pady=1,
            **kwargs,
        )
        self.accent_color = accent_color
        self.inner = tk.Frame(self, bg=bg_color, padx=12, pady=8, width=width)
        self.inner.pack(fill="both", expand=True)

        self.title_label = tk.Label(
            self.inner,
            text=title.upper(),
            font=("Segoe UI", 8, "bold"),
            fg=COLOR_TEXT_SECONDARY,
            bg=bg_color,
        )
        self.title_label.pack(anchor="w")

        val_frame = tk.Frame(self.inner, bg=bg_color)
        val_frame.pack(anchor="w", pady=(2, 0))

        self.value_label = tk.Label(
            val_frame,
            text=initial_value,
            font=("Segoe UI", 16, "bold"),
            fg=accent_color,
            bg=bg_color,
        )
        self.value_label.pack(side="left")

        if unit:
            self.unit_label = tk.Label(
                val_frame,
                text=f" {unit}",
                font=("Segoe UI", 10),
                fg=COLOR_TEXT_MUTED,
                bg=bg_color,
            )
            self.unit_label.pack(side="left", pady=(4, 0))

    def update_value(self, value: str, color: Optional[str] = None):
        """Update displayed stat value and optionally change the color."""
        self.value_label.config(text=value)
        if color:
            self.value_label.config(fg=color)

