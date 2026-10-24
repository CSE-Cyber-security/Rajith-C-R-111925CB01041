"""
Simple Calculator
Weekly Mini Project - 04

A menu-driven console calculator supporting addition, subtraction,
multiplication, division, modulus, and power, with input validation
and a persistent calculation history.

Run:
    python src/calculator.py

Data is persisted to ../data/history.json (relative to this file), so
the history survives between runs.
"""

import json
import os

# ---------------------------------------------------------------------------
# Configuration / constants
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "history.json")

LINE = "=" * 41
DASH = "-" * 41

# menu choice -> (internal operator symbol, display symbol, operation name)
OPERATIONS = {
    "1": ("+", "+", "Add"),
    "2": ("-", "-", "Subtract"),
    "3": ("*", "*", "Multiply"),
    "4": ("/", "/", "Divide"),
    "5": ("%", "%", "Modulus"),
    "6": ("**", "^", "Power"),
}


# ---------------------------------------------------------------------------
# Arithmetic
# ---------------------------------------------------------------------------

def compute(symbol, a, b):
    if symbol == "+":
        return a + b
    if symbol == "-":
        return a - b
    if symbol == "*":
        return a * b
    if symbol == "/":
        if b == 0:
            raise ZeroDivisionError("division")
        return a / b
    if symbol == "%":
        if b == 0:
            raise ZeroDivisionError("modulus")
        return a % b
    if symbol == "**":
        return a ** b
    raise ValueError(f"Unknown operator: {symbol}")


def format_num(x):
    """Show whole-number floats (like 5.0) as 5, keep real decimals as-is."""
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return str(x)


# ---------------------------------------------------------------------------
# Input helpers (all validate and re-prompt on bad input)
# ---------------------------------------------------------------------------

def parse_number(raw):
    try:
        return int(raw)
    except ValueError:
        pass
    return float(raw)  # raises ValueError if still not a valid number


def prompt_number(label):
    while True:
        raw = input(f"{label}: ").strip()
        if not raw:
            print("  Error: This field cannot be empty.")
            continue
        try:
            return parse_number(raw)
        except ValueError:
            print(f"  Error: '{raw}' is not a valid number.")


# ---------------------------------------------------------------------------
# History tracking
# ---------------------------------------------------------------------------

class CalculationHistory:
    def __init__(self):
        self.entries = []
        self.load()

    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    self.entries = json.load(f)
            except (json.JSONDecodeError, OSError):
                self.entries = []

    def save(self):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump(self.entries, f, indent=2)

    def next_id(self):
        max_num = 0
        for entry in self.entries:
            suffix = entry["Entry ID"][1:]
            if suffix.isdigit():
                max_num = max(max_num, int(suffix))
        return f"C{max_num + 1:03d}"

    def add(self, expression, result):
        entry = {
            "Entry ID": self.next_id(),
            "Expression": expression,
            "Result": format_num(result),
        }
        self.entries.append(entry)
        self.save()
        return entry

    def display_all(self):
        print("\n" + LINE)
        print(" CALCULATION HISTORY")
        print(LINE)
        if not self.entries:
            print("No calculations yet.")
            print(LINE)
            return
        for i, e in enumerate(self.entries):
            print(f"Entry ID    : {e['Entry ID']}")
            print(f"Expression  : {e['Expression']} = {e['Result']}")
            if i != len(self.entries) - 1:
                print(DASH)
        print(LINE)
        print(f"Total Calculations : {len(self.entries)}")
        print(LINE)


# ---------------------------------------------------------------------------
# Menu / program flow
# ---------------------------------------------------------------------------

def do_operation(history, symbol, display_symbol, name):
    print(f"\n--- {name} ---")
    a = prompt_number("Enter first number")
    b = prompt_number("Enter second number")
    try:
        result = compute(symbol, a, b)
    except ZeroDivisionError:
        action = "divide" if symbol == "/" else "compute modulus"
        print(f"  Error: Cannot {action} by zero.")
        return

    expression = f"{format_num(a)} {display_symbol} {format_num(b)}"
    entry = history.add(expression, result)

    print()
    print(LINE)
    print(" CALCULATION RESULT")
    print(LINE)
    print(f"Entry ID    : {entry['Entry ID']}")
    print(f"Expression  : {expression} = {entry['Result']}")
    print(LINE)


def print_menu():
    print("\n" + LINE)
    print(" SIMPLE CALCULATOR")
    print(LINE)
    print("1. Add        (+)")
    print("2. Subtract   (-)")
    print("3. Multiply   (*)")
    print("4. Divide     (/)")
    print("5. Modulus    (%)")
    print("6. Power      (^)")
    print("7. View History")
    print("8. Exit")
    print(LINE)


def main():
    history = CalculationHistory()
    while True:
        print_menu()
        choice = input("Enter your choice (1-8): ").strip()
        if choice in OPERATIONS:
            symbol, display_symbol, name = OPERATIONS[choice]
            do_operation(history, symbol, display_symbol, name)
        elif choice == "7":
            history.display_all()
        elif choice == "8":
            print("\nExiting Simple Calculator. Goodbye!")
            break
        else:
            print("  Error: Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
