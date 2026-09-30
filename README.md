# Student Tracker

A simple, feature-packed Python application for tracking students, managing subject grades, computing averages and letter grades, viewing class statistics, and saving/loading data via JSON files.

## Features

- **Student Management:** Add, view, search, and remove students with unique IDs.
- **Grade Tracking:** Add, update, and remove numerical grades (0–100) per subject.
- **Grade Calculations:** Automatically compute average grades and letter grade equivalents (A, B, C, D, F).
- **Class Analytics:** View total student count, overall class average grade, and top/lowest performers.
- **Data Persistence:** Save tracker data to and load from JSON files.
- **Interactive CLI:** Easy-to-use menu-driven terminal interface.

## Project Structure

```
.
├── main.py                     # Command-line interface entry point
├── student_tracker/
│   ├── __init__.py             # Package initializer
│   ├── student.py              # Student class implementation
│   └── tracker.py              # StudentTracker management class implementation
└── tests/
    └── test_tracker.py         # Comprehensive unit tests using pytest
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- `pytest` (for running unit tests)

### Running the Application

To launch the interactive CLI menu:

```bash
python3 main.py
```

### Running Tests

To run the unit test suite:

```bash
PYTHONPATH=. pytest
```

## Example Usage

1. Launch `python3 main.py`.
2. Choose Option `1` to add a student (e.g., ID: `101`, Name: `Alice`).
3. Choose Option `6` to add subject grades (e.g., `Math`: `95`, `Science`: `88`).
4. Choose Option `3` to view Alice's details and average grade.
5. Choose Option `8` to view class statistics.
6. Choose Option `9` to save student data to a JSON file (e.g., `students.json`).
