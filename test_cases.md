# Test Cases — Simple Calculator

Manual test cases used to verify `src/calculator.py`. Each was run
against the program via its interactive menu; screenshots of the
corresponding sessions are in `../screenshots/`.

| # | Test Case | Steps / Input | Expected Result | Actual Result |
|---|-----------|----------------|------------------|----------------|
| TC-01 | Addition | Menu → `1`, enter `10`, `5` | `10 + 5 = 15`, saved as C001 | ✅ Pass — see `screenshots/01-basic-operations.png` |
| TC-02 | Subtraction | Menu → `2`, enter `10`, `5` | `10 - 5 = 5` | ✅ Pass |
| TC-03 | Multiplication | Menu → `3`, enter `10`, `5` | `10 * 5 = 50` | ✅ Pass |
| TC-04 | Division | Menu → `4`, enter `10`, `4` | `10 / 4 = 2.5` | ✅ Pass — see `screenshots/02-divide-modulus-power.png` |
| TC-05 | Modulus | Menu → `5`, enter `10`, `3` | `10 % 3 = 1` | ✅ Pass |
| TC-06 | Power | Menu → `6`, enter `2`, `10` | `2 ^ 10 = 1024` | ✅ Pass |
| TC-07 | Division by zero | Menu → `4`, enter `10`, `0` | `Error: Cannot divide by zero.`; no crash, returns to menu | ✅ Pass — see `screenshots/04-error-handling.png` |
| TC-08 | Modulus by zero | Menu → `5`, enter `10`, `0` | `Error: Cannot compute modulus by zero.`; no crash | ✅ Pass |
| TC-09 | Non-numeric first operand | Enter `abc` at the first-number prompt | `Error: 'abc' is not a valid number.`; re-prompts | ✅ Pass |
| TC-10 | Non-numeric second operand | Enter `xyz` at the second-number prompt | `Error: 'xyz' is not a valid number.`; re-prompts | ✅ Pass |
| TC-11 | Empty operand | Press Enter with nothing typed at a number prompt | `Error: This field cannot be empty.`; re-prompts | ✅ Pass |
| TC-12 | Whole-number float display | Compute `10 / 2` | Displays `5`, not `5.0` | ✅ Pass |
| TC-13 | Decimal float display | Compute `15 / 4` | Displays `3.75` | ✅ Pass |
| TC-14 | View history | Menu → `7` with existing entries | All past calculations print in order, with a Total Calculations count | ✅ Pass — see `screenshots/03-view-history.png` |
| TC-15 | View history (empty) | Menu → `7` with no prior calculations | `No calculations yet.` shown instead of an error | ✅ Pass |
| TC-16 | Invalid menu choice | At the main menu, enter `99` | `Error: Invalid choice. Please enter a number between 1 and 8.` | ✅ Pass |
| TC-17 | Data persistence across runs | Perform a calculation, exit, relaunch | History reflects the same state as when the program was last closed (loaded from `data/history.json`) | ✅ Pass |
| TC-18 | Negative operands | Menu → `1`, enter `-7`, `-3` | `-7 + -3 = -10` | ✅ Pass |

## How these were run

Each scenario was driven through a pseudo-terminal so that typed input
is echoed exactly as it would appear in a real terminal session, then
captured as a screenshot. To reproduce any of the above by hand:

```bash
cd Week-04-Simple-Calculator
python3 src/calculator.py
```

and follow the steps in the "Steps / Input" column.
