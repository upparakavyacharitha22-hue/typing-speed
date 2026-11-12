"""
high_scores.py - Session High Score and Test History Manager.
Tracks user tests, calculates session bests (Best WPM, Best Accuracy),
average speed, and maintains an ordered record of attempts during the session.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional


class SessionManager:
    """Manages typing test records and high scores for the current session."""

    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.best_wpm: int = 0
        self.best_accuracy: float = 0.0
        self.total_tests: int = 0

    def add_result(self, stats: Dict[str, Any], paragraph_title: str = "") -> Dict[str, Any]:
        """
        Record a newly completed test attempt and evaluate if it's a new session high score.
        """
        self.total_tests += 1
        net_wpm = stats.get("net_wpm", 0)
        accuracy = stats.get("accuracy", 0.0)

        is_new_high_wpm = (net_wpm > self.best_wpm)
        is_new_high_acc = (accuracy > self.best_accuracy)

        if is_new_high_wpm:
            self.best_wpm = net_wpm
        if is_new_high_acc:
            self.best_accuracy = accuracy

        record = {
            "test_number": self.total_tests,
            "timestamp": datetime.now().strftime("%I:%M:%S %p"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "paragraph_title": paragraph_title,
            "net_wpm": net_wpm,
            "gross_wpm": stats.get("gross_wpm", 0),
            "accuracy": accuracy,
            "mistakes": stats.get("mistakes", 0),
            "correct_chars": stats.get("correct_chars", 0),
            "total_chars": stats.get("total_chars", 0),
            "standard_words": stats.get("standard_words", 0),
            "elapsed_seconds": stats.get("elapsed_seconds", 60),
            "tier_name": stats.get("tier_name", "Beginner"),
            "tier_badge_color": stats.get("tier_badge_color", "#F59E0B"),
            "is_new_high_wpm": is_new_high_wpm,
        }

        self.history.append(record)
        return record

    def get_best_wpm(self) -> int:
        """Return the highest WPM recorded in this session."""
        return self.best_wpm

    def get_best_accuracy(self) -> float:
        """Return the highest accuracy percentage recorded in this session."""
        return self.best_accuracy

    def get_total_tests(self) -> int:
        """Return total number of tests completed."""
        return self.total_tests

    def get_average_wpm(self) -> float:
        """Calculate average WPM across all tests in this session."""
        if not self.history:
            return 0.0
        total_wpm = sum(r["net_wpm"] for r in self.history)
        return round(total_wpm / len(self.history), 1)

    def get_history(self) -> List[Dict[str, Any]]:
        """Return a copy of all completed test records in chronological order."""
        return list(self.history)

    def get_recent_results(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Return the most recent N test results in reverse chronological order."""
        return list(reversed(self.history))[:limit]

    def reset_session(self) -> None:
        """Reset all session high scores and history."""
        self.history.clear()
        self.best_wpm = 0
        self.best_accuracy = 0.0
        self.total_tests = 0

