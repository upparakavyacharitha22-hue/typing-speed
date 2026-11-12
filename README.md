# ⚡ TypeMaster – Modern Desktop Typing Speed Test

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/GUI-Tkinter%208.6-indigo.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-brightgreen.svg)]()

> An interactive, modern, and feature-rich desktop typing test application built using **Python** and **Tkinter**. Designed to measure, benchmark, and improve your typing speed (WPM), accuracy, and keyboard fluency through timed tests and real-time visual feedback.

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Key Features](#-key-features)
3. [Design System & UI Theme](#-design-system--ui-theme)
4. [File Structure](#-file-structure)
5. [Prerequisites & Installation](#-prerequisites--installation)
6. [How to Run the Application](#-how-to-run-the-application)
7. [Typing Speed & Accuracy Formulas](#-typing-speed--accuracy-formulas)
8. [Performance Benchmark Tiers](#-performance-benchmark-tiers)
9. [Code Architecture & Explanation for Beginners](#-code-architecture--explanation-for-beginners)
10. [Running Automated Tests](#-running-automated-tests)
11. [Course Submission Checklist](#-course-submission-checklist)

---

## 🎯 Project Overview

In the modern digital workplace, typing speed and precision directly impact productivity. The global average typing speed is approximately **40 WPM (Words Per Minute)**. **TypeMaster** helps users benchmark their current speed, detect errors in real time, build muscle memory, and steadily progress towards the Fast (60–79 WPM) and Excellent (80+ WPM) tiers.

The application is built **100% using Python's Standard Library**, requiring **zero third-party dependencies**. It can be executed immediately on any Windows, macOS, or Linux computer running Python 3.8+.

---

## ✨ Key Features

### 1. 🏠 Home Dashboard
- **Clean Welcome Center**: Welcomes the user with a sleek header, application overview, and clear step-by-step instructions.
- **Speed Benchmark Display**: Prominently highlights the 40 WPM global average benchmark and outlines the 5 performance tiers.
- **Session High Score Summary**: Displays your session's best WPM, highest accuracy, total tests taken, and session average speed.
- **One-Click Start**: Vibrant "Start Typing Test" button to begin immediately.

### 2. ⌨️ Typing Test Screen
- **Curated Paragraph Pool**: Features 12 diverse, engaging sample paragraphs covering Science, AI, Space, Nature, Cybersecurity, and Habit Building.
- **Random Paragraph Selection**: Automatically picks a new paragraph for each test, ensuring tests never feel repetitive.
- **Automatic Timer Start**: The 60-second countdown timer initiates **only on your first keystroke** (ignoring modifier keys like Shift and Ctrl).
- **Dual Real-time Mistake Highlighting**:
  - In the sample text box: Correct characters are colored **green**, incorrect characters are underlined in **red**, and the upcoming character is highlighted with a cursor tag.
  - In the user's typing box: Mismatched characters are dynamically tagged in **red with a subtle dark background**.
- **Live Stats Dashboard**: Real-time display of Time Remaining (60s countdown), Live WPM, Live Accuracy (%), and Live Mistakes count.
- **Smooth Canvas Progress Bar**: Visual countdown bar that changes color from cyan/blue to warning amber and danger red as time runs low.
- **Full Test Controls**: Allows restarting the test at any moment with a single click.

### 3. 📊 Results Dashboard
- **Speed Calculation**: Computes Net WPM and Gross WPM using the international standard **5-characters-per-word** formula.
- **Comprehensive Metrics Grid**:
  - Final Net Speed (WPM)
  - Accuracy Percentage (%)
  - Number of Mistakes
  - Correct Characters typed
  - Total Characters typed
  - Words Typed (standard 5-character words and actual words)
  - Elapsed Time
- **Performance Tier Categorization**: Automatically categorizes your speed into **Beginner**, **Improving**, **Average**, **Fast**, or **Excellent**.
- **Benchmark Comparison**: Shows your exact difference compared to the 40 WPM average (e.g. `+14 WPM above average benchmark`).
- **Personalized Motivational Messages**: Context-aware feedback based on both your speed tier and typing accuracy.
- **Navigation Controls**: "Try Again" (starts a fresh test with a new paragraph), "Session History", and "Home Dashboard" buttons.

### 4. 🏆 Session High Scores & History
- Records every test attempt during the session with timestamps, WPM, accuracy, errors, character counts, and tier badges.
- Highlights new session bests with special trophy badges.
- Dedicated **Session Performance History** view featuring a clean tabular display with scrolling and session reset capabilities.

---

## 🎨 Design System & UI Theme

TypeMaster is designed with a modern, high-contrast dark theme inspired by modern developer tools:

| Element | Color Hex | Preview / Purpose |
| :--- | :--- | :--- |
| **Main Background** | `#0B0F19` | Deep Dark Slate / Navy |
| **Card Surface** | `#1E293B` | Modern elevated container |
| **Primary Accent** | `#6366F1` | Vibrant Indigo / Purple |
| **Secondary Accent** | `#38BDF8` | Electric Sky Blue |
| **Success Color** | `#10B981` | Emerald Green (Correct keystrokes & high scores) |
| **Danger / Error** | `#EF4444` | Coral Red (Mistakes & low time warning) |
| **Warning Color** | `#F59E0B` | Warm Amber |
| **Primary Text** | `#FFFFFF` | Bright White for maximum readability |
| **Muted Text** | `#94A3B8` | Slate Grey for labels and descriptions |

---

## 📂 File Structure

```text
TypeMaster/
│
├── main.py              # Main application entry point, GUI controllers & views
├── speed_calculator.py  # WPM, accuracy, character comparisons, and tiers
├── paragraphs.py        # Curated library of 12 test paragraphs & selection logic
├── high_scores.py       # Session high score & test history manager
├── ui_components.py     # Reusable custom Tkinter widgets (cards, buttons, progress bar)
├── test_app.py          # Automated unit & integration tests
├── requirements.txt     # Environment requirements (pure standard library)
├── README.md            # Complete project documentation & guide
└── assets/
    └── icon.png         # Application window icon
```

---

## ⚙️ Prerequisites & Installation

### Requirements
- **Operating System**: Windows 10/11, macOS, or Linux.
- **Python**: Version **3.8 or higher** (Python 3.10+ recommended).
- **Tkinter**: Bundled by default with official Python installers on Windows and macOS.

> [!NOTE]
> On Ubuntu/Debian Linux, if Tkinter is missing, install it using:
> ```bash
> sudo apt-get update && sudo apt-get install python3-tk
> ```

---

## 🚀 How to Run the Application

### 1. Open Terminal / Command Prompt
Navigate to the project directory:
```bash
cd "c:\Users\Kavya\OneDrive\Desktop\typing speed testing apllication"
```

### 2. Run the Main Script
```bash
python main.py
```
*(On macOS/Linux, use `python3 main.py` if `python` points to Python 2).*

### 3. Running from VS Code or PyCharm
1. Open the folder in **VS Code** or **PyCharm**.
2. Select your installed Python 3 interpreter.
3. Open `main.py`.
4. Click the **Run** button or press `F5` / `Ctrl+F5`.

---

## 📐 Typing Speed & Accuracy Formulas

TypeMaster adheres to the **international typing certification standard**:

### 1. Standard Word Definition
A "word" in typing certification is standardized to **5 keystrokes / characters** (including letters, spaces, and punctuation). This ensures fair measurement regardless of whether paragraphs contain short or long words.

$$\text{Standard Words} = \frac{\text{Total Characters Typed}}{5}$$

### 2. Elapsed Time in Minutes
$$\text{Elapsed Minutes} = \frac{\text{Elapsed Seconds}}{60.0}$$

### 3. Words Per Minute (WPM)
- **Gross WPM** (Raw typing speed):
  $$\text{Gross WPM} = \frac{\text{Total Characters} / 5}{\text{Elapsed Minutes}}$$

- **Net WPM** (Standard productive speed based on correct characters):
  $$\text{Net WPM} = \max\left(0, \frac{\text{Correct Characters} / 5}{\text{Elapsed Minutes}}\right)$$

### 4. Accuracy Percentage
$$\text{Accuracy (\%)} = \left(\frac{\text{Correct Characters Typed}}{\text{Total Characters Typed}}\right) \times 100$$

### 5. Mistakes / Errors
$$\text{Mistakes} = \sum (\text{Mismatched Characters}) + (\text{Characters Typed Beyond Target Length})$$

---

## 🏅 Performance Benchmark Tiers

TypeMaster categorizes every completed test into one of five recognized performance levels:

| Tier | Speed Range | Badge Color | Description |
| :---: | :---: | :---: | :--- |
| **🌱 Beginner** | Below 20 WPM | Amber (`#F59E0B`) | Developing initial finger placement and keyboard familiarity. |
| **⚡ Improving** | 20 – 39 WPM | Sky Blue (`#38BDF8`) | Building muscle memory and rhythm. |
| **🎯 Average** | 40 – 59 WPM | Indigo (`#6366F1`) | Meets the global typing speed benchmark for computer users. |
| **🚀 Fast** | 60 – 79 WPM | Emerald (`#10B981`) | Productive touch typist capable of rapid writing and coding. |
| **🏆 Excellent** | 80+ WPM | Violet (`#8B5CF6`) | Elite typing speed in the top 5% of typists worldwide. |

---

## 🔍 Code Architecture & Explanation for Beginners

For students and beginners reviewing this codebase, here is how each module works:

### 1. `main.py` – The Application Engine
- Inherits from `tk.Tk` to create the root application window.
- Implements a single-window view switcher (`show_home()`, `show_test()`, `show_results()`, `show_history()`) that cleanly swaps widget containers without creating messy multi-window popups.
- **Non-blocking Timer**: Instead of `time.sleep(1)` (which halts the GUI and causes Windows to report the application as "Not Responding"), TypeMaster uses Tkinter's native `self.after(100, self.update_timer)`. This schedules a lightweight check every 100 milliseconds while keeping the user interface completely responsive.
- **Automatic Timer Trigger**: Listens for `<KeyPress>`. When the user types their first alphanumeric key, the start timestamp `time.time()` is recorded and `update_timer()` begins counting down from 60 seconds.
- **Real-Time Text Tagging**: On every `<KeyRelease>`, Tkinter Text tags (`correct`, `wrong`, `current`, `untyped`) are dynamically recalculated and applied to both the sample paragraph and the user input box.

### 2. `speed_calculator.py` – The Analytics Engine
- Performs the character-by-character comparison between target and typed text.
- Applies the mathematical formulas for Net WPM, Gross WPM, accuracy %, and mistakes.
- Maps WPM scores to speed tiers and produces context-aware motivational feedback.

### 3. `paragraphs.py` – Content Repository
- Stores a clean collection of 12 sample texts.
- Provides `get_random_paragraph(exclude_id)` so the user gets varied topics on every test and never repeats the same text twice in a row.

### 4. `high_scores.py` – State & History Manager
- Maintains a clean list of test attempts across the session.
- Tracks `best_wpm`, `best_accuracy`, `total_tests`, and `average_wpm`.
- Provides an easy-to-use API to add results and clear session history.

### 5. `ui_components.py` – Modern Widget Library
- Contains custom reusable widgets:
  - `ModernButton`: A styled button with hover and active press state transitions (`<Enter>`, `<Leave>`, `<Button-1>`).
  - `CardFrame`: A bordered, dark-surface card container.
  - `ModernProgressBar`: A custom Canvas progress bar that dynamically recolors as time decreases.
  - `StatBadge`: A live metric display card for the live dashboard.

---

## 🧪 Running Automated Tests

TypeMaster includes an automated test suite (`test_app.py`) verifying all business logic and GUI events.

To run the unit and integration tests:
```bash
python test_app.py
```

Expected output:
```text
............
----------------------------------------------------------------------
Ran 12 tests in 1.691s

OK
```

### What is tested:
- Paragraph count, lengths, and random selection logic.
- Standard 5-character-per-word WPM formulas.
- Character mistake detection and accuracy percentage calculations.
- Speed tier categorization thresholds.
- Session manager best score tracking and resets.
- GUI initialization, screen navigation, keypress timer triggers, live tagging, and test completion.

---

## 🎓 Course Submission Checklist

| Requirement | Status | Implementation Details |
| :--- | :---: | :--- |
| **Tkinter Desktop GUI** | ✅ | Native responsive Tkinter GUI with custom dark theme |
| **Sample Paragraphs** | ✅ | 12 diverse paragraphs across science, tech, and literature |
| **Random Selection** | ✅ | Implemented via `paragraphs.get_random_paragraph()` |
| **Auto-Start on Typing** | ✅ | Starts 60s timer on first valid keypress |
| **Countdown Timer** | ✅ | 60-second non-blocking timer using `after(100)` |
| **Restart Test** | ✅ | Instant restart button on test screen and results screen |
| **WPM Calculation** | ✅ | Standard 5-chars-per-word formula |
| **Accuracy Calculation** | ✅ | `(correct / total) * 100` |
| **Mistake Detection** | ✅ | Character-by-character comparison |
| **Results Screen** | ✅ | Detailed dashboard with all 6 required metrics |
| **Speed Tiers** | ✅ | Beginner, Improving, Average, Fast, Excellent |
| **Benchmark (40 WPM)** | ✅ | Explanations and live comparison against 40 WPM |
| **Mistake Highlighting** | ✅ | Visual red highlighting in both sample text and input |
| **Session High Scores** | ✅ | Session manager tracking best WPM, accuracy, and history |
| **Beginner Friendly Code** | ✅ | Clean modular architecture with docstrings and comments |

---

## 📜 License

This project is created for educational and practical use. Feel free to use, modify, and submit this project for your academic coursework.

