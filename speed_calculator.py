"""
speed_calculator.py - Typing Speed, Accuracy, and Metric Calculations.
Implements the standard 5-character-per-word typing formula, error detection,
speed tier categorization, and motivational feedback generation.
"""

from typing import Dict, Any, Tuple


AVERAGE_BENCHMARK_WPM = 40

SPEED_TIERS = [
    {
        "max_wpm": 19,
        "name": "Beginner",
        "badge_color": "#F59E0B",   # Amber
        "description": "Starting your typing journey",
        "icon": "🌱",
    },
    {
        "max_wpm": 39,
        "name": "Improving",
        "badge_color": "#38BDF8",   # Sky Blue
        "description": "Building momentum and muscle memory",
        "icon": "⚡",
    },
    {
        "max_wpm": 59,
        "name": "Average",
        "badge_color": "#6366F1",   # Indigo / Purple
        "description": "Meets or matches the global benchmark standard",
        "icon": "🎯",
    },
    {
        "max_wpm": 79,
        "name": "Fast",
        "badge_color": "#10B981",   # Emerald Green
        "description": "Highly productive and fluent touch typist",
        "icon": "🚀",
    },
    {
        "max_wpm": 9999,
        "name": "Excellent",
        "badge_color": "#8B5CF6",   # Vibrant Purple / Violet
        "description": "Elite tier speed among top competitive typists",
        "icon": "🏆",
    },
]


def get_speed_tier(wpm: int) -> Dict[str, Any]:
    """
    Classify typing speed into standard recognized performance tiers:
    - Below 20 WPM: Beginner
    - 20–39 WPM: Improving
    - 40–59 WPM: Average
    - 60–79 WPM: Fast
    - 80+ WPM: Excellent
    """
    for tier in SPEED_TIERS:
        if wpm <= tier["max_wpm"]:
            return tier
    return SPEED_TIERS[-1]


def calculate_stats(
    target_text: str,
    typed_text: str,
    elapsed_seconds: float,
) -> Dict[str, Any]:
    """
    Calculate comprehensive typing metrics:
    - Net Words Per Minute (WPM) using standard 5 characters = 1 word
    - Gross Words Per Minute (Gross WPM)
    - Total characters typed
    - Correct characters
    - Incorrect characters (mistakes)
    - Accuracy percentage
    - Total words typed (standard 5-char and space-split count)
    - Benchmark comparison
    """
    total_chars = len(typed_text)
    target_len = len(target_text)

    # Compare character by character
    compare_len = min(total_chars, target_len)
    correct_chars = 0
    mistakes = 0

    for i in range(compare_len):
        if typed_text[i] == target_text[i]:
            correct_chars += 1
        else:
            mistakes += 1

    # Excess characters typed beyond the target text length count as mistakes
    if total_chars > target_len:
        mistakes += (total_chars - target_len)

    # Accuracy percentage: (correct characters / total characters typed) * 100
    if total_chars > 0:
        accuracy = round((correct_chars / total_chars) * 100.0, 1)
    else:
        accuracy = 0.0

    # Avoid zero division and negative values
    elapsed_safe = max(elapsed_seconds, 1.0)
    elapsed_minutes = elapsed_safe / 60.0

    # Standard WPM calculation:
    # 1 standard word = 5 characters (including spaces and punctuation)
    # Net WPM = (Correct Characters / 5) / Time in Minutes
    # Gross WPM = (Total Characters Typed / 5) / Time in Minutes
    if total_chars > 0 and elapsed_seconds > 0:
        gross_wpm = int(round((total_chars / 5.0) / elapsed_minutes))
        net_wpm = int(round((correct_chars / 5.0) / elapsed_minutes))
        net_wpm = max(0, net_wpm)
    else:
        gross_wpm = 0
        net_wpm = 0

    # Total words typed: standard (chars/5) and actual space-separated words
    standard_words = round(total_chars / 5.0, 1)
    actual_words = len(typed_text.strip().split()) if typed_text.strip() else 0

    # Benchmark difference comparison against 40 WPM
    diff_from_benchmark = net_wpm - AVERAGE_BENCHMARK_WPM
    if diff_from_benchmark > 0:
        benchmark_comparison = f"+{diff_from_benchmark} WPM above average benchmark (40 WPM)"
    elif diff_from_benchmark == 0:
        benchmark_comparison = "Exactly matching the global average benchmark (40 WPM)"
    else:
        benchmark_comparison = f"{abs(diff_from_benchmark)} WPM below average benchmark (40 WPM)"

    tier_info = get_speed_tier(net_wpm)
    motivational_message = get_motivational_message(net_wpm, accuracy, mistakes)

    return {
        "net_wpm": net_wpm,
        "gross_wpm": gross_wpm,
        "total_chars": total_chars,
        "correct_chars": correct_chars,
        "mistakes": mistakes,
        "accuracy": accuracy,
        "standard_words": standard_words,
        "actual_words": actual_words,
        "elapsed_seconds": round(elapsed_seconds, 1),
        "tier_name": tier_info["name"],
        "tier_badge_color": tier_info["badge_color"],
        "tier_icon": tier_info["icon"],
        "tier_description": tier_info["description"],
        "benchmark_comparison": benchmark_comparison,
        "diff_from_benchmark": diff_from_benchmark,
        "motivational_message": motivational_message,
    }


def get_motivational_message(wpm: int, accuracy: float, mistakes: int) -> str:
    """
    Generate contextual, encouraging feedback based on performance and accuracy.
    """
    if wpm >= 80:
        if accuracy >= 95.0:
            return "Incredible typing mastery! Your speed and near-flawless precision put you in the elite top 5% of typists worldwide."
        return "Blazing fast speed! With just a little more focus on reducing typos, you will be unstoppable."

    elif wpm >= 60:
        if accuracy >= 95.0:
            return "Fantastic performance! You type significantly faster than average with superb accuracy. Keep it up!"
        return "Impressive pace! Slow down just slightly on tricky words to boost your accuracy above 95%."

    elif wpm >= 40:
        if accuracy >= 95.0:
            return "Great job! You have surpassed the global average of 40 WPM with excellent precision. Fast tier is within reach!"
        return "Well done! You have reached the average benchmark. Regular practice sessions will quickly push you into the 60+ WPM tier."

    elif wpm >= 20:
        if accuracy >= 90.0:
            return "Solid progress! Your accuracy is strong. As your fingers build muscle memory, your speed will naturally climb."
        return "Good effort! Remember that accuracy builds speed. Focus on typing smoothly without rushing, and the speed will follow."

    else:
        if accuracy >= 85.0:
            return "Good start! You are building careful typing habits. Keep practicing daily for 10 minutes to rapidly increase your speed."
        return "Every great typist started right here. Take your time, position your hands comfortably, and practice one paragraph at a time!"

