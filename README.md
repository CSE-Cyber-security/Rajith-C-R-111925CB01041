# Week 04 — Simple Calculator

A menu-driven Python console calculator supporting addition,
subtraction, multiplication, division, modulus, and power, with input
validation and a persistent calculation history.

## Problem Statement

Build a simple calculator that lets a user perform basic arithmetic
operations on two numbers. The tool should handle invalid input (such
as non-numeric values or dividing by zero) without crashing, and keep
a record of past calculations so the user can look back at what
they've computed.

## Features

- **Six operations**: Add, Subtract, Multiply, Divide, Modulus, Power
- **Input validation**: rejects empty input and non-numeric values,
  always re-prompting instead of crashing
- **Safe division/modulus**: dividing or taking the modulus by zero
  shows a clear error and returns to the menu rather than crashing
- **Clean number display**: whole-number results like `10 / 2` show as
  `5`, not `5.0`
- **Calculation history** — every result is saved with an
  auto-generated Entry ID and can be reviewed with "View History"
- **Persistence** — history is saved to `data/history.json` after
  every calculation and reloaded automatically the next time the
  program runs

## Repository Structure

```
Week-04-Simple-Calculator/
├── src/
│   └── calculator.py           # Main program
├── data/
│   └── history.json            # Persisted history (seeded with 4 sample entries)
├── tests/
│   └── test_cases.md           # Manual test cases and results
├── screenshots/
│   ├── 01-basic-operations.png
│   ├── 02-divide-modulus-power.png
│   ├── 03-view-history.png
│   └── 04-error-handling.png
└── README.md
```

## How to Run

Requires Python 3 (standard library only — no external dependencies).

```bash
cd Week-04-Simple-Calculator
python3 src/calculator.py
```

### Sample Session

```
=========================================
 SIMPLE CALCULATOR
=========================================
1. Add        (+)
2. Subtract   (-)
3. Multiply   (*)
4. Divide     (/)
5. Modulus    (%)
6. Power      (^)
7. View History
8. Exit
=========================================
Enter your choice (1-8): 1

--- Add ---
Enter first number: 10
Enter second number: 5

=========================================
 CALCULATION RESULT
=========================================
Entry ID    : C001
Expression  : 10 + 5 = 15
=========================================
```

## Design Notes

- **Number parsing**: input is tried as an `int` first, then a
  `float`, so `5` stays a clean integer while `5.5` is handled
  correctly — any value that's neither is rejected with a clear error.
- **Division/modulus by zero**: caught as a `ZeroDivisionError` and
  turned into a friendly message instead of letting Python's own
  traceback reach the user.
- **Auto-generated Entry IDs** (`C001`, `C002`, ...): since a
  calculation history is naturally sequential, IDs are generated
  automatically rather than typed in.

## Testing

See [`tests/test_cases.md`](tests/test_cases.md) for the full list of
manual test cases (each operation, division/modulus by zero, invalid
input, and history behavior) with expected vs. actual results.
Corresponding screenshots are in [`screenshots/`](screenshots/).
