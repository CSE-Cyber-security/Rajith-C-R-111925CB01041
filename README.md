# Week 03 — Fibonacci Series Generator

A Python console program that prints the first `n` terms of the
Fibonacci series.

## Question

Write a Python program to print the Fibonacci series for n terms.

## Sample I/O

**Input:**
```
Enter the number of terms: 7
```

**Output:**
```
Fibonacci Series:
0 1 1 2 3 5 8
```

## Features

- Prints the first `n` Fibonacci numbers, space-separated, exactly
  matching the required output format
- **Input validation**: rejects empty input, non-integer input, and
  negative numbers, re-prompting each time rather than crashing
- **Run again** option so you can generate another series without
  restarting the program

## Repository Structure

```
Week-03-Fibonacci-Series/
├── src/
│   └── fibonacci.py        # Main program
├── tests/
│   └── test_cases.md       # Manual test cases and results
├── screenshots/
│   ├── 01-valid-input.png
│   ├── 02-boundary-values.png
│   └── 03-input-validation.png
└── README.md
```

## How to Run

Requires Python 3 (standard library only — no external dependencies).

```bash
cd Week-03-Fibonacci-Series
python3 src/fibonacci.py
```

## How It Works

The series is built iteratively, starting from `a, b = 0, 1`. On each
of the `n` iterations the current value of `a` is recorded, then
`a, b` are advanced to `b, a + b` — the classic constant-space way to
generate Fibonacci numbers without recomputing earlier terms.

```python
def generate_fibonacci(n):
    series = []
    a, b = 0, 1
    for _ in range(n):
        series.append(a)
        a, b = b, a + b
    return series
```

## Testing

See [`tests/test_cases.md`](tests/test_cases.md) for the full list of
test cases (the assignment's sample, boundary values like n=0 and
n=1, and validation failures) with expected vs. actual results.
Corresponding screenshots are in [`screenshots/`](screenshots/).
