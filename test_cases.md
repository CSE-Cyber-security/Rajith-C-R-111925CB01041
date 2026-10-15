# Test Cases — Fibonacci Series Generator

Manual test cases used to verify `src/fibonacci.py`. Each was run
against the program interactively; screenshots of the corresponding
sessions are in `../screenshots/`.

| # | Test Case | Input | Expected Output | Actual Result |
|---|-----------|-------|------------------|----------------|
| TC-01 | Assignment sample (n=7) | `7` | `Fibonacci Series:` then `0 1 1 2 3 5 8` | ✅ Pass — matches the assignment's sample output exactly, see `screenshots/01-valid-input.png` |
| TC-02 | Single term (n=1) | `1` | `0` | ✅ Pass — see `screenshots/02-boundary-values.png` |
| TC-03 | Zero terms (n=0) | `0` | An empty series line (no numbers printed) | ✅ Pass — see `screenshots/02-boundary-values.png` |
| TC-04 | Two terms (n=2) | `2` | `0 1` | ✅ Pass |
| TC-05 | Larger n (n=15) | `15` | `0 1 1 2 3 5 8 13 21 34 55 89 144 233 377` | ✅ Pass |
| TC-06 | Reject empty input | *(press Enter with nothing typed)* | `Error: This field cannot be empty.`, then re-prompts | ✅ Pass — see `screenshots/03-input-validation.png` |
| TC-07 | Reject non-integer input | `abc` | `Error: 'abc' is not a valid integer.`, then re-prompts | ✅ Pass |
| TC-08 | Reject negative input | `-5` | `Error: Number of terms cannot be negative.`, then re-prompts | ✅ Pass |
| TC-09 | Run again (loop) | `7`, then `y`, then `3` | Program accepts a second run without restarting; produces `0 1 1` | ✅ Pass |
| TC-10 | Exit cleanly | `7`, then `n` | Prints `Goodbye!` and the program terminates | ✅ Pass |
| TC-11 | Invalid y/n response | At the "Calculate again?" prompt, enter `maybe` | `Error: Please enter 'y' or 'n'.`, then re-prompts | ✅ Pass |

## Correctness check

The sequence is defined as `F(0) = 0`, `F(1) = 1`,
`F(k) = F(k-1) + F(k-2)` for `k ≥ 2`. For n = 7 the first seven terms
are `0, 1, 1, 2, 3, 5, 8` — matching the assignment's expected output
exactly.

## How to run these by hand

```bash
cd Week-03-Fibonacci-Series
python3 src/fibonacci.py
```

and follow the "Input" column above.
