# Week 02 — Factorial Calculator & History Tracker

A menu-driven Python console application that computes the factorial
of a number using iterative and/or recursive methods, validates every
input, and keeps a searchable, editable history of past calculations.

## Problem Statement

Compute the factorial of a number entered by the user. The tool should
support both common approaches to the problem — an iterative loop and
a recursive function — let the user pick (or verify both agree), and
avoid crashing on invalid input such as negative numbers, non-numeric
text, or numbers too large to handle sensibly. Beyond a single
calculation, the tool keeps a running history so previous results can
be looked up, labeled, and managed rather than lost after each run.

## Features

- **Calculate** n! using an iterative loop, a recursive function, or
  both at once (with automatic cross-verification)
- **Search** history by Entry ID, Number (n), or Method used
- **Update** the label/note on any past calculation
- **Delete** a history entry, with a confirmation prompt
- **Display** the full calculation history in a clean report format
- **Statistics Summary** — largest/smallest n computed, most digits
  produced, counts per method, and average result length
- **Input validation** on every field: rejects negative numbers,
  non-integers, numbers above the supported cap, and invalid menu or
  method choices, always re-prompting instead of crashing
- **Persistence** — history is saved to `data/history.json` after
  every change and reloaded automatically the next time the program
  runs

## How Factorial Is Computed

| Method | Implementation | Practical limit |
|---|---|---|
| Iterative | A `for` loop multiplying `1 × 2 × 3 × ... × n` | n ≤ 10,000 |
| Recursive | `n! = n × (n-1)!` with base case `0! = 1! = 1` | n ≤ 900 (stays under Python's recursion limit) |
| Both (Verified) | Runs both implementations and confirms they agree before saving | n ≤ 900 |

Numbers above 900 can still be computed — just with the Iterative
method, since deep recursion in Python risks hitting the interpreter's
call-stack limit. The program also raises Python's integer-to-string
conversion ceiling at startup, since 10,000! has about 35,660 digits —
well past the 4,300-digit default introduced in Python 3.11.

## Data Model

Each history entry has the following fields:

| Field | Notes |
|---|---|
| Entry ID | Auto-generated, e.g. `F001`, `F002`, ... |
| Number | The `n` that was computed |
| Method | `Iterative`, `Recursive`, or `Both (Verified)` |
| Result | The factorial result, stored as a string (can be very large) |
| Digits | Length of the result, for quick comparison |
| Label | Optional free-text note the user can add or edit |

## Repository Structure

```
Week-02-Factorial-Calculator/
├── src/
│   └── factorial_calculator.py   # Main program
├── data/
│   └── history.json              # Persisted history (seeded with 4 sample entries)
├── tests/
│   └── test_cases.md             # Manual test cases and results
├── screenshots/
│   ├── 01-calculate-factorial.png
│   ├── 02-display-history.png
│   ├── 03-search-history.png
│   ├── 04-update-label.png
│   ├── 05-delete-entry.png
│   ├── 06-statistics-summary.png
│   └── 07-input-validation.png
└── README.md
```

## How to Run

Requires Python 3.7+ (standard library only — no external
dependencies; Python 3.11+ recommended so the built-in integer-string
limit is raised automatically, though the program is compatible with
earlier versions too).

```bash
cd Week-02-Factorial-Calculator
python3 src/factorial_calculator.py
```

You'll land on the main menu right away — there's no separate
"bulk load" step for this project, since a factorial history builds up
naturally one calculation at a time.

### Sample Session

```
=========================================
 FACTORIAL CALCULATOR & HISTORY TRACKER
=========================================
1. Calculate Factorial
2. Search History
3. Update Entry Label
4. Delete Entry
5. Display All History
6. Statistics Summary
7. Exit
=========================================
Enter your choice (1-7): 1

--- Calculate Factorial ---
Enter a non-negative integer (n) to compute n! [0-10000]: 12
Method (1=Iterative, 2=Recursive, 3=Both/Verify): 1
Optional label/note (press Enter to skip): Practice problem

=========================================
 FACTORIAL CALCULATION RESULT
=========================================
Entry ID     : F005
Number (n)   : 12
Method       : Iterative
Result       : 479001600
Digits       : 9
Label        : Practice problem
=========================================
```

## Design Notes

- **Validation loops**: the number field rejects blanks, non-integers,
  negatives, and anything above the supported cap; the method field
  rejects anything outside 1–3 and blocks Recursive/Both when `n` is
  too large for safe recursion — all with a clear re-prompt rather
  than a crash.
- **Auto-generated IDs**: unlike a manually-curated inventory, a
  calculation history is naturally sequential, so Entry IDs (`F001`,
  `F002`, ...) are generated automatically rather than typed in.
- **Verification mode**: choosing "Both" doesn't just run two
  algorithms for fun — it actively cross-checks their results and
  aborts the save if they ever disagreed, which would indicate a bug.

## Testing

See [`tests/test_cases.md`](tests/test_cases.md) for the full list of
manual test cases (calculating, searching, updating, deleting,
validation failures, and edge cases like very large factorials) with
expected vs. actual results. Corresponding screenshots are in
[`screenshots/`](screenshots/).
