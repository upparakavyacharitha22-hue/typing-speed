"""
main.py - TypeMaster: Typing Speed & Accuracy Test Desktop Application.
Built with Python 3 and Tkinter.

A complete, modern desktop application designed to measure and improve typing speed
and accuracy with real-time feedback, interactive benchmarks, high-score tracking,
and detailed performance analytics.
"""

import os
import sys
import time
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any

from paragraphs import get_random_paragraph, SAMPLE_PARAGRAPHS
from speed_calculator import (
    calculate_stats,
    AVERAGE_BENCHMARK_WPM,
    SPEED_TIERS,
)
from high_scores import SessionManager
from ui_components import (
    COLOR_BG,
    COLOR_SURFACE,
    COLOR_SURFACE_LIGHT,
    COLOR_BORDER,
    COLOR_PRIMARY,
    COLOR_PRIMARY_HOVER,
    COLOR_SECONDARY,
    COLOR_SECONDARY_HOVER,
    COLOR_SUCCESS,
    COLOR_WARNING,
    COLOR_DANGER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED,
    COLOR_INPUT_BG,
    COLOR_ACCENT_PURPLE,
    ModernButton,
    CardFrame,
    ModernProgressBar,
    StatBadge,
)


TEST_DURATION_SECONDS = 60


class TypeMasterApp(tk.Tk):
    """
    Main Application Window and Controller for TypeMaster.
    Manages view transitions between Home, Typing Test, Results, and Session History.
    """

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("TypeMaster – Typing Speed Test")
        self.geometry("1040x720")
        self.minsize(860, 620)
        self.configure(bg=COLOR_BG)

        # Set application icon if available
        self._setup_icon()

        # Session State
        self.session_manager = SessionManager()

        # Active Test State
        self.current_paragraph: Optional[Dict[str, str]] = None
        self.test_running: bool = False
        self.test_started: bool = False
        self.start_time: float = 0.0
        self.elapsed_time: float = 0.0
        self.timer_after_id: Optional[str] = None
        self.last_stats: Optional[Dict[str, Any]] = None

        # Container for swappable screens (Home, Test, Results, History)
        self.container = tk.Frame(self, bg=COLOR_BG)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Start with Home view
        self.show_home()

    def _setup_icon(self):
        """Configure application icon safely from assets folder if available."""
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
        if os.path.exists(icon_path):
            try:
                self.app_icon = tk.PhotoImage(file=icon_path)
                self.iconphoto(True, self.app_icon)
            except Exception:
                pass

    def _clear_container(self):
        """Remove all active widgets from the central container."""
        if self.timer_after_id:
            try:
                self.after_cancel(self.timer_after_id)
            except Exception:
                pass
            self.timer_after_id = None

        for widget in self.container.winfo_children():
            widget.destroy()

    # ========================================================================
    # SCREEN 1: HOME DASHBOARD
    # ========================================================================
    def show_home(self):
        """Render the TypeMaster Home Dashboard."""
        self._clear_container()

        # Main scrollable or centered canvas/frame
        home_frame = tk.Frame(self.container, bg=COLOR_BG)
        home_frame.pack(fill="both", expand=True, padx=30, pady=24)

        # --- Top Header Bar ---
        header_frame = tk.Frame(home_frame, bg=COLOR_BG)
        header_frame.pack(fill="x", pady=(0, 20))

        # Title & Logo Badge
        title_box = tk.Frame(header_frame, bg=COLOR_BG)
        title_box.pack(side="left")

        logo_label = tk.Label(
            title_box,
            text="⚡",
            font=("Segoe UI", 26),
            fg=COLOR_SECONDARY,
            bg=COLOR_BG,
        )
        logo_label.pack(side="left", padx=(0, 10))

        title_text_box = tk.Frame(title_box, bg=COLOR_BG)
        title_text_box.pack(side="left")

        app_title = tk.Label(
            title_text_box,
            text="TypeMaster",
            font=("Segoe UI", 26, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_BG,
        )
        app_title.pack(anchor="w")

        app_subtitle = tk.Label(
            title_text_box,
            text="Interactive Desktop Typing Speed & Accuracy Benchmark",
            font=("Segoe UI", 11),
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_BG,
        )
        app_subtitle.pack(anchor="w")

        # Top Right Actions: Session History button
        history_btn = ModernButton(
            header_frame,
            text=f"📊 Session History ({self.session_manager.get_total_tests()})",
            command=self.show_history,
            bg_color=COLOR_SURFACE,
            hover_color=COLOR_SURFACE_LIGHT,
            active_color=COLOR_BORDER,
            text_color=COLOR_TEXT_PRIMARY,
            font_tuple=("Segoe UI", 10, "bold"),
            padx=14,
            pady=8,
        )
        history_btn.pack(side="right")

        # --- Hero Welcome & Start Card ---
        hero_card = CardFrame(home_frame, bg=COLOR_SURFACE, padx=24, pady=22)
        hero_card.pack(fill="x", pady=(0, 20))

        welcome_heading = tk.Label(
            hero_card.body,
            text="Ready to test your keyboard speed?",
            font=("Segoe UI", 18, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_SURFACE,
        )
        welcome_heading.pack(anchor="w")

        welcome_desc = tk.Label(
            hero_card.body,
            text=(
                "TypeMaster presents you with engaging real-world paragraphs to evaluate your typing speed in "
                "Words Per Minute (WPM), accuracy percentage, and keystroke mistakes. Take multiple tests "
                "to track your muscle memory and build speed over time."
            ),
            font=("Segoe UI", 11),
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_SURFACE,
            wraplength=850,
            justify="left",
        )
        welcome_desc.pack(anchor="w", pady=(8, 16))

        # Start button in Hero
        hero_btn_row = tk.Frame(hero_card.body, bg=COLOR_SURFACE)
        hero_btn_row.pack(anchor="w")

        start_btn = ModernButton(
            hero_btn_row,
            text="🚀  Start Typing Test (60s)",
            command=self.start_new_test,
            bg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color="#FFFFFF",
            font_tuple=("Segoe UI", 13, "bold"),
            padx=28,
            pady=12,
        )
        start_btn.pack(side="left", padx=(0, 14))

        quick_tip = tk.Label(
            hero_btn_row,
            text="⏱️  The 60-second timer begins automatically on your first keypress.",
            font=("Segoe UI", 10, "italic"),
            fg=COLOR_SECONDARY,
            bg=COLOR_SURFACE,
        )
        quick_tip.pack(side="left", pady=(8, 0))

        # --- Grid: How it Works & Benchmark Information ---
        info_grid = tk.Frame(home_frame, bg=COLOR_BG)
        info_grid.pack(fill="both", expand=True)
        info_grid.grid_columnconfigure(0, weight=1, uniform="info_col")
        info_grid.grid_columnconfigure(1, weight=1, uniform="info_col")
        info_grid.grid_columnconfigure(2, weight=1, uniform="info_col")

        # Column 1: Test Instructions
        instructions_card = CardFrame(info_grid, bg=COLOR_SURFACE, padx=18, pady=18)
        instructions_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        inst_title = tk.Label(
            instructions_card.body,
            text="📖  How The Test Works",
            font=("Segoe UI", 13, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_SURFACE,
        )
        inst_title.pack(anchor="w", pady=(0, 10))

        steps = [
            ("1", "A random paragraph is chosen from 12 diverse subjects."),
            ("2", "Click the input area and type the displayed text."),
            ("3", "The 60s timer starts on your very first keystroke."),
            ("4", "Real-time colors highlight correct and incorrect letters."),
            ("5", "Get a detailed results breakdown when time expires."),
        ]
        for num, step_text in steps:
            step_row = tk.Frame(instructions_card.body, bg=COLOR_SURFACE)
            step_row.pack(fill="x", pady=3)

            pill = tk.Label(
                step_row,
                text=num,
                font=("Segoe UI", 9, "bold"),
                fg=COLOR_PRIMARY,
                bg=COLOR_SURFACE_LIGHT,
                width=3,
                pady=1,
            )
            pill.pack(side="left", padx=(0, 8))

            step_lbl = tk.Label(
                step_row,
                text=step_text,
                font=("Segoe UI", 9),
                fg=COLOR_TEXT_SECONDARY,
                bg=COLOR_SURFACE,
                wraplength=210,
                justify="left",
            )
            step_lbl.pack(side="left")

        # Column 2: Speed Benchmark (40 WPM benchmark requirement)
        benchmark_card = CardFrame(info_grid, bg=COLOR_SURFACE, padx=18, pady=18)
        benchmark_card.grid(row=0, column=1, sticky="nsew", padx=5)

        bench_title = tk.Label(
            benchmark_card.body,
            text="🎯  Typing Speed Benchmark",
            font=("Segoe UI", 13, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_SURFACE,
        )
        bench_title.pack(anchor="w", pady=(0, 8))

        bench_highlight = tk.Frame(benchmark_card.body, bg=COLOR_SURFACE_LIGHT, padx=12, pady=8)
        bench_highlight.pack(fill="x", pady=(0, 10))

        bench_num = tk.Label(
            bench_highlight,
            text="40 WPM",
            font=("Segoe UI", 18, "bold"),
            fg=COLOR_SECONDARY,
            bg=COLOR_SURFACE_LIGHT,
        )
        bench_num.pack(anchor="w")

        bench_num_sub = tk.Label(
            bench_highlight,
            text="Global Average Benchmark for Computer Users",
            font=("Segoe UI", 9),
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_SURFACE_LIGHT,
        )
        bench_num_sub.pack(anchor="w")

        tiers_info = [
            ("Below 20 WPM", "Beginner", "#F59E0B"),
            ("20–39 WPM", "Improving", "#38BDF8"),
            ("40–59 WPM", "Average", "#6366F1"),
            ("60–79 WPM", "Fast", "#10B981"),
            ("80+ WPM", "Excellent", "#8B5CF6"),
        ]
        for wpm_range, tier_lbl, color in tiers_info:
            t_row = tk.Frame(benchmark_card.body, bg=COLOR_SURFACE)
            t_row.pack(fill="x", pady=2)

            t_badge = tk.Label(
                t_row,
                text=tier_lbl,
                font=("Segoe UI", 8, "bold"),
                fg=color,
                bg=COLOR_SURFACE_LIGHT,
                width=9,
            )
            t_badge.pack(side="left", padx=(0, 8))

            t_desc = tk.Label(
                t_row,
                text=wpm_range,
                font=("Segoe UI", 9),
                fg=COLOR_TEXT_SECONDARY,
                bg=COLOR_SURFACE,
            )
            t_desc.pack(side="left")

        # Column 3: Session High Scores & Records
        records_card = CardFrame(info_grid, bg=COLOR_SURFACE, padx=18, pady=18)
        records_card.grid(row=0, column=2, sticky="nsew", padx=(10, 0))

        rec_title = tk.Label(
            records_card.body,
            text="🏆  Session High Scores",
            font=("Segoe UI", 13, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_SURFACE,
        )
        rec_title.pack(anchor="w", pady=(0, 10))

        best_wpm = self.session_manager.get_best_wpm()
        best_acc = self.session_manager.get_best_accuracy()
        total_tests = self.session_manager.get_total_tests()
        avg_wpm = self.session_manager.get_average_wpm()

        rec_stat_frame = tk.Frame(records_card.body, bg=COLOR_SURFACE)
        rec_stat_frame.pack(fill="both", expand=True)

        rec_items = [
            ("BEST SPEED", f"{best_wpm} WPM", COLOR_SUCCESS),
            ("BEST ACCURACY", f"{best_acc}%", COLOR_SECONDARY),
            ("TOTAL TESTS", f"{total_tests}", COLOR_TEXT_PRIMARY),
            ("SESSION AVERAGE", f"{avg_wpm} WPM", COLOR_PRIMARY),
        ]

        for label_text, val_text, val_color in rec_items:
            item_box = tk.Frame(rec_stat_frame, bg=COLOR_SURFACE_LIGHT, padx=10, pady=6)
            item_box.pack(fill="x", pady=3)

            lbl = tk.Label(
                item_box,
                text=label_text,
                font=("Segoe UI", 8, "bold"),
                fg=COLOR_TEXT_SECONDARY,
                bg=COLOR_SURFACE_LIGHT,
            )
            lbl.pack(side="left")

            val = tk.Label(
                item_box,
                text=val_text,
                font=("Segoe UI", 11, "bold"),
                fg=val_color,
                bg=COLOR_SURFACE_LIGHT,
            )
            val.pack(side="right")

    # ========================================================================
    # SCREEN 2: TYPING TEST
    # ========================================================================
    def start_new_test(self):
        """Pick a new random paragraph and navigate to the Typing Test Screen."""
        # Avoid picking the same paragraph consecutively
        current_id = self.current_paragraph["id"] if self.current_paragraph else None
        self.current_paragraph = get_random_paragraph(exclude_id=current_id)

        self.test_running = False
        self.test_started = False
        self.start_time = 0.0
        self.elapsed_time = 0.0
        if self.timer_after_id:
            try:
                self.after_cancel(self.timer_after_id)
            except Exception:
                pass
            self.timer_after_id = None

        self.show_test()

    def show_test(self):
        """Render the Typing Test Screen."""
        self._clear_container()

        test_frame = tk.Frame(self.container, bg=COLOR_BG)
        test_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # --- Top Navigation & Controls Row ---
        top_bar = tk.Frame(test_frame, bg=COLOR_BG)
        top_bar.pack(fill="x", pady=(0, 14))

        home_btn = ModernButton(
            top_bar,
            text="← Home Dashboard",
            command=self._confirm_exit_to_home,
            bg_color=COLOR_SURFACE,
            hover_color=COLOR_SURFACE_LIGHT,
            text_color=COLOR_TEXT_PRIMARY,
            font_tuple=("Segoe UI", 9, "bold"),
            padx=12,
            pady=6,
        )
        home_btn.pack(side="left", padx=(0, 10))

        restart_btn = ModernButton(
            top_bar,
            text="🔄 Restart Test",
            command=self.restart_test,
            bg_color=COLOR_SURFACE,
            hover_color=COLOR_SURFACE_LIGHT,
            text_color=COLOR_TEXT_PRIMARY,
            font_tuple=("Segoe UI", 9, "bold"),
            padx=12,
            pady=6,
        )
        restart_btn.pack(side="left")

        # Paragraph topic pill on the right
        topic_frame = tk.Frame(top_bar, bg=COLOR_SURFACE_LIGHT, padx=12, pady=4)
        topic_frame.pack(side="right")

        topic_label = tk.Label(
            topic_frame,
            text=f"Topic: {self.current_paragraph.get('topic', 'General')} • {self.current_paragraph.get('title', '')}",
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_SECONDARY,
            bg=COLOR_SURFACE_LIGHT,
        )
        topic_label.pack()

        # --- Live Dashboard Stat Badges ---
        stat_bar = tk.Frame(test_frame, bg=COLOR_BG)
        stat_bar.pack(fill="x", pady=(0, 10))
        stat_bar.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="stat_badge")

        self.badge_timer = StatBadge(
            stat_bar,
            title="Time Remaining",
            initial_value=f"{TEST_DURATION_SECONDS}s",
            accent_color=COLOR_SECONDARY,
        )
        self.badge_timer.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.badge_wpm = StatBadge(
            stat_bar,
            title="Live Speed",
            initial_value="0",
            unit="WPM",
            accent_color=COLOR_PRIMARY,
        )
        self.badge_wpm.grid(row=0, column=1, sticky="ew", padx=3)

        self.badge_accuracy = StatBadge(
            stat_bar,
            title="Accuracy",
            initial_value="100%",
            accent_color=COLOR_SUCCESS,
        )
        self.badge_accuracy.grid(row=0, column=2, sticky="ew", padx=3)

        self.badge_mistakes = StatBadge(
            stat_bar,
            title="Mistakes",
            initial_value="0",
            accent_color=COLOR_DANGER,
        )
        self.badge_mistakes.grid(row=0, column=3, sticky="ew", padx=(6, 0))

        # --- Progress Bar ---
        self.progress_bar = ModernProgressBar(
            test_frame,
            height=6,
            fill_color=COLOR_SECONDARY,
            bg_color=COLOR_SURFACE,
        )
        self.progress_bar.pack(fill="x", pady=(4, 16))
        self.progress_bar.set_progress(1.0)

        # --- Display Target Paragraph (Sample Text) ---
        sample_card = CardFrame(test_frame, bg=COLOR_SURFACE, padx=18, pady=16)
        sample_card.pack(fill="both", expand=True, pady=(0, 14))

        sample_header = tk.Frame(sample_card.body, bg=COLOR_SURFACE)
        sample_header.pack(fill="x", pady=(0, 8))

        sample_title = tk.Label(
            sample_header,
            text="TEXT TO TYPE:",
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_SURFACE,
        )
        sample_title.pack(side="left")

        self.status_hint = tk.Label(
            sample_header,
            text="● Click the input area below and start typing. The 60-second timer begins on first keypress.",
            font=("Segoe UI", 9, "italic"),
            fg=COLOR_SECONDARY,
            bg=COLOR_SURFACE,
        )
        self.status_hint.pack(side="right")

        # Monospace Text Box for Target Paragraph
        self.sample_text_box = tk.Text(
            sample_card.body,
            wrap="word",
            font=("Consolas", 14),
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT_PRIMARY,
            insertbackground=COLOR_TEXT_PRIMARY,
            relief="flat",
            bd=0,
            padx=8,
            pady=8,
            height=5,
        )
        self.sample_text_box.pack(fill="both", expand=True)

        # Configure highlighting tags for sample text
        self.sample_text_box.tag_configure("correct", foreground=COLOR_SUCCESS)
        self.sample_text_box.tag_configure("wrong", foreground=COLOR_DANGER, underline=True)
        self.sample_text_box.tag_configure("current", background=COLOR_PRIMARY, foreground="#FFFFFF")
        self.sample_text_box.tag_configure("untyped", foreground=COLOR_TEXT_SECONDARY)

        # Populate sample text
        self.sample_text_box.insert("1.0", self.current_paragraph["text"])
        self.sample_text_box.tag_add("untyped", "1.0", "end")
        self.sample_text_box.config(state="disabled")

        # --- User Typing Input Area ---
        input_card = CardFrame(test_frame, bg=COLOR_INPUT_BG, border_color=COLOR_PRIMARY, padx=14, pady=12)
        input_card.pack(fill="x", pady=(0, 10))

        self.input_text = tk.Text(
            input_card.body,
            wrap="word",
            font=("Consolas", 14),
            bg=COLOR_INPUT_BG,
            fg=COLOR_TEXT_PRIMARY,
            insertbackground=COLOR_SECONDARY,
            relief="flat",
            bd=0,
            height=4,
            undo=True,
        )
        self.input_text.pack(fill="both", expand=True)
        self.input_text.focus_set()

        # Configure real-time input tags (highlighting errors in red inside input area as well)
        self.input_text.tag_configure("input_wrong", foreground=COLOR_DANGER, background="#3B1212")
        self.input_text.tag_configure("input_correct", foreground=COLOR_TEXT_PRIMARY)

        # Input box placeholder behavior
        self.placeholder_text = "Click here and start typing... (Timer begins automatically on your first keypress)"
        self._show_placeholder()

        # Event Bindings for typing detection & real-time checking
        self.input_text.bind("<FocusIn>", self._on_input_focus_in)
        self.input_text.bind("<FocusOut>", self._on_input_focus_out)
        self.input_text.bind("<KeyPress>", self._on_key_press)
        self.input_text.bind("<KeyRelease>", self._on_key_release)
        self.input_text.bind("<Tab>", lambda e: "break")  # Prevent accidental focus loss

    def _show_placeholder(self):
        """Insert placeholder text if input area is empty."""
        if not self.test_started:
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", self.placeholder_text)
            self.input_text.tag_add("placeholder", "1.0", "end")
            self.input_text.tag_config("placeholder", foreground=COLOR_TEXT_MUTED)

    def _on_input_focus_in(self, event=None):
        """Clear placeholder text when user clicks into the input field."""
        if not self.test_started:
            current_content = self.input_text.get("1.0", "end-1c")
            if current_content == self.placeholder_text:
                self.input_text.delete("1.0", "end")

    def _on_input_focus_out(self, event=None):
        """Restore placeholder text if the user unfocuses before starting."""
        if not self.test_started:
            content = self.input_text.get("1.0", "end-1c").strip()
            if not content:
                self._show_placeholder()

    def _on_key_press(self, event):
        """Detect the very first character key to start the timer."""
        # Ignore modifier keys and standalone navigation keys for starting the timer
        ignored_keys = {
            "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R",
            "Caps_Lock", "Tab", "Escape", "Num_Lock", "Scroll_Lock", "Pause",
            "Left", "Right", "Up", "Down", "Home", "End", "Page_Up", "Page_Down",
            "Insert", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
        }

        if event.keysym in ignored_keys:
            return

        # If test hasn't started yet, initialize test and start timer loop
        if not self.test_started and not self.test_running:
            # If placeholder is still present, clear it
            if self.input_text.get("1.0", "end-1c") == self.placeholder_text:
                self.input_text.delete("1.0", "end")

            self.test_started = True
            self.test_running = True
            self.start_time = time.time()
            self.status_hint.config(
                text="● Test in progress! Keep typing until the 60s timer expires.",
                fg=COLOR_SUCCESS,
            )
            # Begin the Tkinter after() countdown loop
            self.update_timer()

    def _on_key_release(self, event):
        """Perform real-time comparison, character highlighting, and live stats update."""
        if not self.test_running:
            return

        typed_text = self.input_text.get("1.0", "end-1c")
        target_text = self.current_paragraph["text"]

        # 1. Update Real-time Highlighting on Target Paragraph and User Input
        self._update_target_text_highlighting(target_text, typed_text)
        self._update_input_text_highlighting(target_text, typed_text)

        # 2. Compute Live Stats
        elapsed = max(0.1, time.time() - self.start_time)
        stats = calculate_stats(target_text, typed_text, elapsed)

        # 3. Update Live Badges
        self.badge_wpm.update_value(str(stats["net_wpm"]))
        self.badge_accuracy.update_value(f"{stats['accuracy']}%")
        self.badge_mistakes.update_value(str(stats["mistakes"]))

        # 4. Check early completion (if user completes entire paragraph before 60s)
        if len(typed_text) >= len(target_text):
            self.finish_test()

    def _update_target_text_highlighting(self, target_text: str, typed_text: str):
        """
        Dynamically applies color tags to the sample text widget:
        - Correct characters: Green
        - Incorrect characters: Red with underline
        - Next character: Cursor highlight
        - Remaining characters: Muted gray
        """
        self.sample_text_box.config(state="normal")
        self.sample_text_box.tag_remove("correct", "1.0", "end")
        self.sample_text_box.tag_remove("wrong", "1.0", "end")
        self.sample_text_box.tag_remove("current", "1.0", "end")
        self.sample_text_box.tag_remove("untyped", "1.0", "end")

        typed_len = len(typed_text)
        target_len = len(target_text)

        # Mark compared characters
        compare_limit = min(typed_len, target_len)
        for i in range(compare_limit):
            start_index = f"1.0 + {i} chars"
            end_index = f"1.0 + {i + 1} chars"
            if typed_text[i] == target_text[i]:
                self.sample_text_box.tag_add("correct", start_index, end_index)
            else:
                self.sample_text_box.tag_add("wrong", start_index, end_index)

        # Highlight current character to type
        if typed_len < target_len:
            cur_start = f"1.0 + {typed_len} chars"
            cur_end = f"1.0 + {typed_len + 1} chars"
            self.sample_text_box.tag_add("current", cur_start, cur_end)

            # Untyped remaining characters
            if typed_len + 1 < target_len:
                rem_start = f"1.0 + {typed_len + 1} chars"
                self.sample_text_box.tag_add("untyped", rem_start, "end")

        self.sample_text_box.config(state="disabled")

    def _update_input_text_highlighting(self, target_text: str, typed_text: str):
        """
        Dynamically applies color tags to the user's input box:
        - Highlights incorrect characters in red with a subtle dark-red background.
        - Keeps correct characters in clean white.
        """
        self.input_text.tag_remove("input_wrong", "1.0", "end")
        self.input_text.tag_remove("input_correct", "1.0", "end")

        typed_len = len(typed_text)
        target_len = len(target_text)

        compare_limit = min(typed_len, target_len)
        for i in range(compare_limit):
            start_index = f"1.0 + {i} chars"
            end_index = f"1.0 + {i + 1} chars"
            if typed_text[i] == target_text[i]:
                self.input_text.tag_add("input_correct", start_index, end_index)
            else:
                self.input_text.tag_add("input_wrong", start_index, end_index)

        # Characters typed beyond the target text are highlighted as wrong
        if typed_len > target_len:
            self.input_text.tag_add("input_wrong", f"1.0 + {target_len} chars", "end")

    def update_timer(self):
        """
        Countdown timer method called every 100ms via Tkinter's after() method.
        Prevents GUI freezing while providing smooth countdown.
        """
        if not self.test_running:
            return

        now = time.time()
        elapsed = now - self.start_time
        remaining = max(0, TEST_DURATION_SECONDS - int(elapsed))

        # Update countdown badge
        if remaining <= 10:
            self.badge_timer.update_value(f"{remaining}s", color=COLOR_DANGER)
            self.progress_bar.set_progress(remaining / TEST_DURATION_SECONDS, color=COLOR_DANGER)
        elif remaining <= 20:
            self.badge_timer.update_value(f"{remaining}s", color=COLOR_WARNING)
            self.progress_bar.set_progress(remaining / TEST_DURATION_SECONDS, color=COLOR_WARNING)
        else:
            self.badge_timer.update_value(f"{remaining}s", color=COLOR_SECONDARY)
            self.progress_bar.set_progress(remaining / TEST_DURATION_SECONDS, color=COLOR_SECONDARY)

        # Check if 60 seconds are completed
        if remaining <= 0:
            self.finish_test()
            return

        # Schedule next update tick in 100 milliseconds
        self.timer_after_id = self.after(100, self.update_timer)

    def finish_test(self):
        """
        Stops the test, disables input to prevent further typing,
        calculates final metrics, records session high score, and opens Results screen.
        """
        if not self.test_running and not self.test_started:
            return

        self.test_running = False
        if self.timer_after_id:
            try:
                self.after_cancel(self.timer_after_id)
            except Exception:
                pass
            self.timer_after_id = None

        # Calculate actual elapsed time (capped at 60s)
        actual_elapsed = min(TEST_DURATION_SECONDS, time.time() - self.start_time)
        if actual_elapsed <= 0.1:
            actual_elapsed = 60.0

        # Lock input box so user cannot type anymore
        self.input_text.config(state="disabled")

        # Collect final text typed
        typed_text = self.input_text.get("1.0", "end-1c")
        if typed_text == self.placeholder_text:
            typed_text = ""

        target_text = self.current_paragraph["text"]

        # Calculate final comprehensive stats
        final_stats = calculate_stats(target_text, typed_text, actual_elapsed)
        self.last_stats = final_stats

        # Record attempt into session history
        para_title = self.current_paragraph.get("title", "Practice Paragraph")
        record = self.session_manager.add_result(final_stats, paragraph_title=para_title)
        final_stats["is_new_high_score"] = record.get("is_new_high_wpm", False)

        # Navigate to Results Dashboard
        self.show_results(final_stats)

    def restart_test(self):
        """Reset the test state and select a new sample paragraph."""
        if self.timer_after_id:
            try:
                self.after_cancel(self.timer_after_id)
            except Exception:
                pass
            self.timer_after_id = None

        self.start_new_test()

    def _confirm_exit_to_home(self):
        """Confirm return to home if test is actively in progress."""
        if self.test_running:
            should_leave = messagebox.askyesno(
                "Cancel Test",
                "A typing test is currently active. Are you sure you want to exit to the Home Dashboard?",
            )
            if not should_leave:
                return

        if self.timer_after_id:
            try:
                self.after_cancel(self.timer_after_id)
            except Exception:
                pass
            self.timer_after_id = None
        self.test_running = False
        self.test_started = False
        self.show_home()

    # ========================================================================
    # SCREEN 3: RESULTS DASHBOARD
    # ========================================================================
    def show_results(self, stats: Dict[str, Any]):
        """Render the Results Dashboard with comprehensive metrics and speed tiers."""
        self._clear_container()

        results_frame = tk.Frame(self.container, bg=COLOR_BG)
        results_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Header Title
        res_header = tk.Frame(results_frame, bg=COLOR_BG)
        res_header.pack(fill="x", pady=(0, 14))

        title_lbl = tk.Label(
            res_header,
            text="🎉  Typing Test Completed!",
            font=("Segoe UI", 22, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_BG,
        )
        title_lbl.pack(side="left")

        # High Score Badge if achieved
        if stats.get("is_new_high_score", False):
            hs_badge = tk.Label(
                res_header,
                text="⭐ NEW SESSION HIGH SCORE!",
                font=("Segoe UI", 10, "bold"),
                fg="#FBBF24",
                bg="#78350F",
                padx=12,
                pady=4,
            )
            hs_badge.pack(side="right")

        # --- Hero Speed Summary Card ---
        hero_card = CardFrame(results_frame, bg=COLOR_SURFACE, padx=24, pady=18)
        hero_card.pack(fill="x", pady=(0, 16))

        hero_grid = tk.Frame(hero_card.body, bg=COLOR_SURFACE)
        hero_grid.pack(fill="x")
        hero_grid.grid_columnconfigure(0, weight=1)
        hero_grid.grid_columnconfigure(1, weight=2)

        # Left Column: Large WPM Score & Tier
        score_box = tk.Frame(hero_grid, bg=COLOR_SURFACE)
        score_box.grid(row=0, column=0, sticky="w")

        wpm_val_lbl = tk.Label(
            score_box,
            text=f"{stats['net_wpm']} WPM",
            font=("Segoe UI", 36, "bold"),
            fg=stats["tier_badge_color"],
            bg=COLOR_SURFACE,
        )
        wpm_val_lbl.pack(anchor="w")

        tier_tag = tk.Label(
            score_box,
            text=f"{stats['tier_icon']}  Level: {stats['tier_name'].upper()}",
            font=("Segoe UI", 12, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=stats["tier_badge_color"],
            padx=12,
            pady=3,
        )
        tier_tag.pack(anchor="w", pady=(4, 0))

        # Right Column: Benchmark comparison & Motivational feedback
        feedback_box = tk.Frame(hero_grid, bg=COLOR_SURFACE)
        feedback_box.grid(row=0, column=1, sticky="nsew", padx=(20, 0))

        bench_lbl = tk.Label(
            feedback_box,
            text=f"Benchmark Check: {stats['benchmark_comparison']}",
            font=("Segoe UI", 11, "bold"),
            fg=COLOR_SECONDARY,
            bg=COLOR_SURFACE,
        )
        bench_lbl.pack(anchor="w")

        motive_msg = tk.Label(
            feedback_box,
            text=stats["motivational_message"],
            font=("Segoe UI", 11),
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_SURFACE,
            wraplength=520,
            justify="left",
        )
        motive_msg.pack(anchor="w", pady=(6, 0))

        # --- Detailed 6-Metric Grid ---
        metrics_grid = tk.Frame(results_frame, bg=COLOR_BG)
        metrics_grid.pack(fill="x", pady=(0, 16))
        for col_idx in range(6):
            metrics_grid.grid_columnconfigure(col_idx, weight=1, uniform="res_metric")

        metric_cards = [
            ("ACCURACY", f"{stats['accuracy']}%", COLOR_SUCCESS),
            ("MISTAKES", f"{stats['mistakes']}", COLOR_DANGER),
            ("CORRECT CHARS", f"{stats['correct_chars']}", COLOR_PRIMARY),
            ("TOTAL CHARS", f"{stats['total_chars']}", COLOR_TEXT_PRIMARY),
            ("WORDS TYPED", f"{stats['standard_words']}", COLOR_SECONDARY),
            ("TIME TAKEN", f"{stats['elapsed_seconds']}s", COLOR_TEXT_SECONDARY),
        ]

        for i, (m_title, m_val, m_color) in enumerate(metric_cards):
            card = CardFrame(metrics_grid, bg=COLOR_SURFACE, padx=12, pady=10)
            card.grid(row=0, column=i, sticky="ew", padx=3)

            lbl_t = tk.Label(
                card.body,
                text=m_title,
                font=("Segoe UI", 8, "bold"),
                fg=COLOR_TEXT_SECONDARY,
                bg=COLOR_SURFACE,
            )
            lbl_t.pack(anchor="w")

            lbl_v = tk.Label(
                card.body,
                text=m_val,
                font=("Segoe UI", 15, "bold"),
                fg=m_color,
                bg=COLOR_SURFACE,
            )
            lbl_v.pack(anchor="w", pady=(3, 0))

        # --- Performance Tier Reference Table ---
        ref_card = CardFrame(results_frame, bg=COLOR_SURFACE, padx=16, pady=12)
        ref_card.pack(fill="x", pady=(0, 18))

        ref_title = tk.Label(
            ref_card.body,
            text="Speed Tier Classifications:",
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_SURFACE,
        )
        ref_title.pack(anchor="w", pady=(0, 6))

        ref_row = tk.Frame(ref_card.body, bg=COLOR_SURFACE)
        ref_row.pack(fill="x")
        ref_row.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="tier_col")

        tiers_display = [
            ("Below 20 WPM", "Beginner", "#F59E0B"),
            ("20–39 WPM", "Improving", "#38BDF8"),
            ("40–59 WPM", "Average", "#6366F1"),
            ("60–79 WPM", "Fast", "#10B981"),
            ("80+ WPM", "Excellent", "#8B5CF6"),
        ]

        for idx, (range_txt, name_txt, col_txt) in enumerate(tiers_display):
            is_active = (name_txt == stats["tier_name"])
            t_bg = COLOR_SURFACE_LIGHT if not is_active else col_txt
            t_fg = COLOR_TEXT_PRIMARY if is_active else col_txt

            t_box = tk.Frame(ref_row, bg=t_bg, padx=8, pady=5)
            t_box.grid(row=0, column=idx, sticky="ew", padx=3)

            name_l = tk.Label(
                t_box,
                text=name_txt + ("  ✓" if is_active else ""),
                font=("Segoe UI", 9, "bold"),
                fg=t_fg,
                bg=t_bg,
            )
            name_l.pack()

            rng_l = tk.Label(
                t_box,
                text=range_txt,
                font=("Segoe UI", 8),
                fg="#FFFFFF" if is_active else COLOR_TEXT_SECONDARY,
                bg=t_bg,
            )
            rng_l.pack()

        # --- Action Buttons (Try Again, History, Home) ---
        btn_bar = tk.Frame(results_frame, bg=COLOR_BG)
        btn_bar.pack(fill="x")

        try_again_btn = ModernButton(
            btn_bar,
            text="🔄  Try Again (New Paragraph)",
            command=self.start_new_test,
            bg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            font_tuple=("Segoe UI", 11, "bold"),
            padx=20,
            pady=10,
        )
        try_again_btn.pack(side="left", padx=(0, 12))

        history_btn = ModernButton(
            btn_bar,
            text="📊  Session History",
            command=self.show_history,
            bg_color=COLOR_SURFACE,
            hover_color=COLOR_SURFACE_LIGHT,
            font_tuple=("Segoe UI", 11, "bold"),
            padx=18,
            pady=10,
        )
        history_btn.pack(side="left", padx=(0, 12))

        home_btn = ModernButton(
            btn_bar,
            text="🏠  Home Dashboard",
            command=self.show_home,
            bg_color=COLOR_SURFACE,
            hover_color=COLOR_SURFACE_LIGHT,
            font_tuple=("Segoe UI", 11, "bold"),
            padx=18,
            pady=10,
        )
        home_btn.pack(side="left")

    # ========================================================================
    # SCREEN 4: SESSION HISTORY & HIGH SCORES
    # ========================================================================
    def show_history(self):
        """Render the Session High Scores and Past Tests History table."""
        self._clear_container()

        hist_frame = tk.Frame(self.container, bg=COLOR_BG)
        hist_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Header Row
        header_row = tk.Frame(hist_frame, bg=COLOR_BG)
        header_row.pack(fill="x", pady=(0, 14))

        title_lbl = tk.Label(
            header_row,
            text="📊  Session Performance History",
            font=("Segoe UI", 20, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_BG,
        )
        title_lbl.pack(side="left")

        back_btn = ModernButton(
            header_row,
            text="← Back to Dashboard",
            command=self.show_home,
            bg_color=COLOR_SURFACE,
            hover_color=COLOR_SURFACE_LIGHT,
            font_tuple=("Segoe UI", 9, "bold"),
            padx=14,
            pady=6,
        )
        back_btn.pack(side="right")

        # Top Summary Cards Row
        summary_grid = tk.Frame(hist_frame, bg=COLOR_BG)
        summary_grid.pack(fill="x", pady=(0, 16))
        summary_grid.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="sum_col")

        best_wpm = self.session_manager.get_best_wpm()
        best_acc = self.session_manager.get_best_accuracy()
        total_tests = self.session_manager.get_total_tests()
        avg_wpm = self.session_manager.get_average_wpm()

        summary_data = [
            ("SESSION BEST SPEED", f"{best_wpm} WPM", COLOR_SUCCESS),
            ("SESSION BEST ACCURACY", f"{best_acc}%", COLOR_SECONDARY),
            ("TESTS COMPLETED", f"{total_tests}", COLOR_TEXT_PRIMARY),
            ("SESSION AVERAGE SPEED", f"{avg_wpm} WPM", COLOR_PRIMARY),
        ]

        for i, (label_txt, val_txt, val_col) in enumerate(summary_data):
            c = CardFrame(summary_grid, bg=COLOR_SURFACE, padx=14, pady=10)
            c.grid(row=0, column=i, sticky="ew", padx=3)

            l1 = tk.Label(
                c.body,
                text=label_txt,
                font=("Segoe UI", 8, "bold"),
                fg=COLOR_TEXT_SECONDARY,
                bg=COLOR_SURFACE,
            )
            l1.pack(anchor="w")

            l2 = tk.Label(
                c.body,
                text=val_txt,
                font=("Segoe UI", 16, "bold"),
                fg=val_col,
                bg=COLOR_SURFACE,
            )
            l2.pack(anchor="w", pady=(2, 0))

        # History Table Container
        table_card = CardFrame(hist_frame, bg=COLOR_SURFACE, padx=14, pady=14)
        table_card.pack(fill="both", expand=True, pady=(0, 14))

        history_list = self.session_manager.get_history()

        if not history_list:
            no_data_label = tk.Label(
                table_card.body,
                text="No typing tests completed yet in this session.\nClick 'Start Typing Test' on the home dashboard to record your first score!",
                font=("Segoe UI", 12),
                fg=COLOR_TEXT_SECONDARY,
                bg=COLOR_SURFACE,
                pady=40,
            )
            no_data_label.pack()
        else:
            # Custom styled treeview table
            style = ttk.Style()
            style.theme_use("clam")
            style.configure(
                "History.Treeview",
                background=COLOR_SURFACE,
                foreground=COLOR_TEXT_PRIMARY,
                fieldbackground=COLOR_SURFACE,
                rowheight=32,
                font=("Segoe UI", 10),
            )
            style.configure(
                "History.Treeview.Heading",
                background=COLOR_SURFACE_LIGHT,
                foreground=COLOR_TEXT_PRIMARY,
                font=("Segoe UI", 10, "bold"),
            )
            style.map("History.Treeview", background=[("selected", COLOR_PRIMARY)])

            columns = ("test_no", "time", "wpm", "accuracy", "mistakes", "chars", "tier")
            tree = ttk.Treeview(
                table_card.body,
                columns=columns,
                show="headings",
                style="History.Treeview",
                selectmode="browse",
            )

            tree.heading("test_no", text="Test #")
            tree.heading("time", text="Timestamp")
            tree.heading("wpm", text="Speed (WPM)")
            tree.heading("accuracy", text="Accuracy")
            tree.heading("mistakes", text="Mistakes")
            tree.heading("chars", text="Characters")
            tree.heading("tier", text="Tier Level")

            tree.column("test_no", width=60, anchor="center")
            tree.column("time", width=120, anchor="center")
            tree.column("wpm", width=100, anchor="center")
            tree.column("accuracy", width=100, anchor="center")
            tree.column("mistakes", width=80, anchor="center")
            tree.column("chars", width=100, anchor="center")
            tree.column("tier", width=120, anchor="center")

            # Add vertical scrollbar
            scroll = ttk.Scrollbar(table_card.body, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scroll.set)

            tree.pack(side="left", fill="both", expand=True)
            scroll.pack(side="right", fill="y")

            # Insert history items in reverse chronological order
            for item in reversed(history_list):
                tree.insert(
                    "",
                    "end",
                    values=(
                        f"#{item['test_number']}",
                        item["timestamp"],
                        f"{item['net_wpm']} WPM" + (" ⭐" if item.get("is_new_high_wpm") else ""),
                        f"{item['accuracy']}%",
                        f"{item['mistakes']}",
                        f"{item['correct_chars']} / {item['total_chars']}",
                        item["tier_name"],
                    ),
                )

        # Bottom Action Buttons
        bot_bar = tk.Frame(hist_frame, bg=COLOR_BG)
        bot_bar.pack(fill="x")

        start_new_btn = ModernButton(
            bot_bar,
            text="🚀  Take Another Test",
            command=self.start_new_test,
            bg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            font_tuple=("Segoe UI", 10, "bold"),
            padx=16,
            pady=8,
        )
        start_new_btn.pack(side="left", padx=(0, 10))

        if history_list:
            clear_btn = ModernButton(
                bot_bar,
                text="🗑️  Reset Session Records",
                command=self._confirm_reset_session,
                bg_color=COLOR_SURFACE,
                hover_color=COLOR_DANGER,
                font_tuple=("Segoe UI", 10, "bold"),
                padx=14,
                pady=8,
            )
            clear_btn.pack(side="left")

    def _confirm_reset_session(self):
        """Confirm and clear session records."""
        confirmed = messagebox.askyesno(
            "Reset Session",
            "Are you sure you want to clear all high scores and test history for this session?",
        )
        if confirmed:
            self.session_manager.reset_session()
            self.show_history()


def main():
    """Application entry point."""
    try:
        app = TypeMasterApp()
        app.mainloop()
    except Exception as e:
        print(f"Error starting TypeMaster: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
