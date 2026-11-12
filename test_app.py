"""
test_app.py - Automated Unit & Integration Tests for TypeMaster.
Tests paragraph selection, speed calculations, timer behavior,
GUI transitions, typing events, and session history tracking.
"""

import time
import unittest
import tkinter as tk

from paragraphs import get_all_paragraphs, get_random_paragraph
from speed_calculator import (
    calculate_stats,
    get_speed_tier,
    get_motivational_message,
    AVERAGE_BENCHMARK_WPM,
)
from high_scores import SessionManager
from main import TypeMasterApp, TEST_DURATION_SECONDS


class TestTypingLogic(unittest.TestCase):
    """Test standard typing calculation formulas and business logic."""

    def test_sample_paragraphs_count(self):
        paragraphs = get_all_paragraphs()
        self.assertGreaterEqual(len(paragraphs), 10, "Must have at least 10 sample paragraphs")
        for p in paragraphs:
            self.assertTrue(len(p["text"]) > 100, f"Paragraph {p['id']} text is too short")
            self.assertTrue(p["title"], "Paragraph must have a title")
            self.assertTrue(p["topic"], "Paragraph must have a topic")

    def test_random_paragraph_selection(self):
        p1 = get_random_paragraph()
        self.assertIsNotNone(p1)
        p2 = get_random_paragraph(exclude_id=p1["id"])
        self.assertNotEqual(p1["id"], p2["id"], "Should exclude the previous paragraph")

    def test_standard_wpm_calculation(self):
        # 250 correct characters in 60 seconds (1 minute):
        # (250 / 5) / 1.0 = 50 WPM
        target = "a" * 300
        typed = "a" * 250
        stats = calculate_stats(target, typed, 60.0)

        self.assertEqual(stats["total_chars"], 250)
        self.assertEqual(stats["correct_chars"], 250)
        self.assertEqual(stats["mistakes"], 0)
        self.assertEqual(stats["accuracy"], 100.0)
        self.assertEqual(stats["net_wpm"], 50)
        self.assertEqual(stats["gross_wpm"], 50)
        self.assertEqual(stats["tier_name"], "Average")

    def test_mistakes_and_accuracy(self):
        target = "Hello World"
        typed = "Hello Warld!"  # 1 mistake ('a' instead of 'o'), 1 extra char ('!')
        stats = calculate_stats(target, typed, 60.0)

        self.assertEqual(stats["total_chars"], 12)
        self.assertEqual(stats["correct_chars"], 10)
        self.assertEqual(stats["mistakes"], 2)
        # Accuracy = (10 / 12) * 100 = 83.3%
        self.assertAlmostEqual(stats["accuracy"], 83.3, places=1)

    def test_speed_tiers(self):
        self.assertEqual(get_speed_tier(15)["name"], "Beginner")
        self.assertEqual(get_speed_tier(28)["name"], "Improving")
        self.assertEqual(get_speed_tier(45)["name"], "Average")
        self.assertEqual(get_speed_tier(72)["name"], "Fast")
        self.assertEqual(get_speed_tier(95)["name"], "Excellent")

    def test_session_manager(self):
        session = SessionManager()
        self.assertEqual(session.get_total_tests(), 0)
        self.assertEqual(session.get_best_wpm(), 0)

        stats1 = {"net_wpm": 35, "accuracy": 92.0, "mistakes": 3, "correct_chars": 175, "total_chars": 180}
        rec1 = session.add_result(stats1, "Test 1")
        self.assertEqual(session.get_total_tests(), 1)
        self.assertEqual(session.get_best_wpm(), 35)
        self.assertTrue(rec1["is_new_high_wpm"])

        stats2 = {"net_wpm": 60, "accuracy": 98.0, "mistakes": 1, "correct_chars": 300, "total_chars": 305}
        rec2 = session.add_result(stats2, "Test 2")
        self.assertEqual(session.get_total_tests(), 2)
        self.assertEqual(session.get_best_wpm(), 60)
        self.assertEqual(session.get_average_wpm(), 47.5)

        session.reset_session()
        self.assertEqual(session.get_total_tests(), 0)
        self.assertEqual(session.get_best_wpm(), 0)


class TestTypeMasterGUI(unittest.TestCase):
    """Test Tkinter GUI workflows, screen transitions, and user events."""

    @classmethod
    def setUpClass(cls):
        cls.app = TypeMasterApp()
        cls.app.withdraw()  # Hide window during headless unit tests

    @classmethod
    def tearDownClass(cls):
        try:
            cls.app.destroy()
        except Exception:
            pass

    def test_01_home_screen(self):
        self.app.show_home()
        self.app.update()
        # Verify container has children
        children = self.app.container.winfo_children()
        self.assertGreater(len(children), 0, "Home screen must have active widgets")

    def test_02_start_test(self):
        self.app.start_new_test()
        self.app.update()

        self.assertIsNotNone(self.app.current_paragraph)
        self.assertFalse(self.app.test_running, "Test should not be running before typing starts")
        self.assertFalse(self.app.test_started, "Test should not be started before typing")

        # Verify sample text is loaded
        sample_content = self.app.sample_text_box.get("1.0", "end-1c")
        self.assertEqual(sample_content, self.app.current_paragraph["text"])

        # Verify timer badge displays 60s
        self.assertEqual(self.app.badge_timer.value_label.cget("text"), f"{TEST_DURATION_SECONDS}s")

    def test_03_typing_and_timer_trigger(self):
        # Simulate typing event
        class DummyEvent:
            keysym = "a"
            char = "a"

        self.app.input_text.insert("1.0", "Artificial")
        self.app._on_key_press(DummyEvent())
        self.app.update()

        self.assertTrue(self.app.test_started, "Test must be marked started on first keypress")
        self.assertTrue(self.app.test_running, "Test must be marked running on first keypress")
        self.assertGreater(self.app.start_time, 0.0)

        # Simulate key release for live metrics
        self.app._on_key_release(DummyEvent())
        self.app.update()

        # Verify live stat badges updated
        wpm_text = self.app.badge_wpm.value_label.cget("text")
        self.assertTrue(wpm_text.isdigit(), "WPM badge should display numeric value")

        # Test input text highlighting
        ranges_correct = self.app.input_text.tag_ranges("input_correct")
        ranges_wrong = self.app.input_text.tag_ranges("input_wrong")
        self.assertTrue(len(ranges_correct) > 0 or len(ranges_wrong) > 0, "Input tags should be applied")

    def test_04_finish_test_and_results(self):
        # Verify input was active before finishing
        self.assertEqual(str(self.app.input_text.cget("state")), "normal")

        # Call finish_test which disables typing and transitions to Results Dashboard
        self.app.finish_test()
        self.app.update()

        # Check test state is no longer running
        self.assertFalse(self.app.test_running)

        # Verify results screen is rendered and stats recorded
        self.assertIsNotNone(self.app.last_stats)
        self.assertEqual(self.app.session_manager.get_total_tests(), 1)
        self.assertIn("net_wpm", self.app.last_stats)
        self.assertIn("accuracy", self.app.last_stats)
        self.assertIn("mistakes", self.app.last_stats)

    def test_05_session_history_screen(self):
        self.app.show_history()
        self.app.update()
        self.assertGreater(len(self.app.container.winfo_children()), 0)

    def test_06_restart_and_return_home(self):
        self.app.start_new_test()
        self.app.update()
        self.app.show_home()
        self.app.update()
        self.assertFalse(self.app.test_running)


if __name__ == "__main__":
    unittest.main()
