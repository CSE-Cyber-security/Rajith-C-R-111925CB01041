# Test Cases — Factorial Calculator & History Tracker

Manual test cases used to verify `src/factorial_calculator.py`. Each was
run against the program via its interactive menu; screenshots of the
corresponding sessions are in `../screenshots/`.

| # | Test Case | Steps / Input | Expected Result | Actual Result |
|---|-----------|----------------|------------------|----------------|
| TC-01 | Calculate factorial (Iterative) | Menu → `1`, enter `12`, method `1` | Computes 12! = 479001600 correctly, saves as a new history entry | ✅ Pass — see `screenshots/01-calculate-factorial.png` |
| TC-02 | Calculate factorial (Recursive) | Menu → `1`, enter `10`, method `2` | Computes 10! = 3628800 via the recursive implementation | ✅ Pass |
| TC-03 | Calculate factorial (Both / Verified) | Menu → `1`, enter `20`, method `3` | Iterative and recursive results are computed and compared; matching result is stored as "Both (Verified)" | ✅ Pass |
| TC-04 | Reject negative number | Menu → `1`, enter `-5` | "Factorial is not defined for negative numbers." shown; re-prompts | ✅ Pass — see `screenshots/07-input-validation.png` |
| TC-05 | Reject non-integer input | Menu → `1`, enter `abc` | "'abc' is not a valid integer." shown; re-prompts | ✅ Pass |
| TC-06 | Reject number above the supported cap | Menu → `1`, enter `999999` | "Please enter a number no greater than 10000." shown; re-prompts | ✅ Pass |
| TC-07 | Reject invalid method choice | At the method prompt, enter `9` | "Please enter 1, 2, or 3." shown; re-prompts | ✅ Pass |
| TC-08 | Reject recursive method for large n | Enter `n = 5000`, then choose method `2` (Recursive) | "Recursive method supports n up to 900 ..." shown; forces Iterative or Both is unavailable until a smaller n is used next time | ✅ Pass |
| TC-09 | Display all history | Menu → `5` | All stored entries print in the required format, followed by Total Calculations / Largest n / Most Digits | ✅ Pass — see `screenshots/02-display-history.png` |
| TC-10 | Search by Number (n) | Menu → `2` → `2`, enter `20` | Returns the single matching entry (F003, n=20) | ✅ Pass — see `screenshots/03-search-history.png` |
| TC-11 | Search by Entry ID | Menu → `2` → `1`, enter `F002` | Returns the single matching entry | ✅ Pass |
| TC-12 | Search by Method | Menu → `2` → `3`, enter `Recursive` | Returns all entries computed with the Recursive method | ✅ Pass |
| TC-13 | Search with no match | Menu → `2` → `1`, enter a non-existent Entry ID (e.g. `F999`) | "No matching entries found." shown; no crash | ✅ Pass |
| TC-14 | Update an entry's label | Menu → `3`, enter `F001`, enter new label `Homework Q1` | Label is updated and persisted; other fields unchanged | ✅ Pass — see `screenshots/04-update-label.png` |
| TC-15 | Update label — blank keeps current | Menu → `3`, enter a valid Entry ID, press Enter at the new-label prompt | "No change made." shown; label remains as-is | ✅ Pass |
| TC-16 | Update a non-existent entry | Menu → `3`, enter an Entry ID that doesn't exist | "No entry found with ID ..." shown; no crash | ✅ Pass |
| TC-17 | Delete an entry (confirmed) | Menu → `4`, enter `F004`, confirm `y` | Entry is removed from history and from `data/history.json`; summary counts update | ✅ Pass — see `screenshots/05-delete-entry.png` |
| TC-18 | Delete an entry (cancelled) | Menu → `4`, enter a valid Entry ID, respond `n` | "Deletion cancelled." shown; entry remains | ✅ Pass |
| TC-19 | Statistics summary | Menu → `6` | Detailed breakdown prints: Total, Largest/Smallest n, Most Digits, counts per method, Average Digits | ✅ Pass — see `screenshots/06-statistics-summary.png` |
| TC-20 | Very large factorial (digit-limit safety) | Calculate `n = 5000` with method Iterative | Result (16,326 digits) is computed and stored without hitting Python's int-to-string conversion limit | ✅ Pass (fixed by raising `sys.set_int_max_str_digits`) |
| TC-21 | Data persistence across runs | Add/update/delete an entry, exit, relaunch | History reflects the same state as when the program was last closed (loaded from `data/history.json`) | ✅ Pass |
| TC-22 | Display with empty history | Delete every entry, then choose Display All | "No history to display." shown instead of an error | ✅ Pass |
| TC-23 | Invalid main menu choice | At the main menu, enter `9` | "Invalid choice. Please enter a number between 1 and 7." shown; menu re-displays | ✅ Pass |

## Known boundary values

- `0! = 1` and `1! = 1` are both handled explicitly by the recursive
  base case and computed correctly by the iterative loop (which never
  enters its multiplication range for n < 2).
- `MAX_N_ITERATIVE = 10000` — the practical ceiling for this tool; well
  above this, factorial results become extremely large strings that
  are impractical to store or display in a console tool.
- `MAX_N_RECURSIVE = 900` — kept safely under Python's default
  recursion limit (1000) so a legitimate large recursive calculation
  can't crash the interpreter.

## How these were run

Each scenario was driven through a pseudo-terminal so that typed input
is echoed exactly as it would appear in a real terminal session, then
captured as a screenshot. To reproduce any of the above by hand:

```bash
cd Week-02-Factorial-Calculator
python3 src/factorial_calculator.py
```

and follow the steps in the "Steps / Input" column.
