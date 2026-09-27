"""
Factorial Calculator and History Tracker
Weekly Mini Project - 02

A menu-driven console application that computes the factorial of a
number using iterative and/or recursive methods, and keeps a searchable,
editable history of every calculation performed.

Run:
    python src/factorial_calculator.py

Data is persisted to ../data/history.json (relative to this file), so
the history survives between runs.
"""

import json
import os
import sys

# ---------------------------------------------------------------------------
# Configuration / constants
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "history.json")

MAX_N_ITERATIVE = 10000   # keeps results fast to compute and reasonable to store
MAX_N_RECURSIVE = 900     # stays safely under Python's default recursion limit

# Python 3.11+ refuses to convert integers with more than 4300 digits to a
# string by default (a DoS guard). 10000! has ~35,660 digits, so raise that
# ceiling well above anything MAX_N_ITERATIVE can produce.
try:
    sys.set_int_max_str_digits(200000)
except AttributeError:
    pass  # Python < 3.11 has no such limit

METHODS = {"1": "Iterative", "2": "Recursive", "3": "Both (Verified)"}

LINE = "=" * 41
DASH = "-" * 41


# ---------------------------------------------------------------------------
# Factorial implementations
# ---------------------------------------------------------------------------

def iterative_factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def recursive_factorial(n):
    if n in (0, 1):
        return 1
    return n * recursive_factorial(n - 1)


def compute_recursive_safely(n):
    """Temporarily raise the recursion limit just enough for this call,
    then restore it, so a legitimate calculation doesn't get killed by
    Python's default limit and we don't leave the limit changed globally."""
    old_limit = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(max(old_limit, n + 150))
        return recursive_factorial(n)
    finally:
        sys.setrecursionlimit(old_limit)


# ---------------------------------------------------------------------------
# Input helpers (all validate and re-prompt on bad input)
# ---------------------------------------------------------------------------

def prompt_number():
    while True:
        value = input(f"Enter a non-negative integer (n) to compute n! [0-{MAX_N_ITERATIVE}]: ").strip()
        if not value:
            print("  Error: This field cannot be empty.")
            continue
        try:
            n = int(value)
        except ValueError:
            print(f"  Error: '{value}' is not a valid integer.")
            continue
        if n < 0:
            print("  Error: Factorial is not defined for negative numbers.")
            continue
        if n > MAX_N_ITERATIVE:
            print(f"  Error: Please enter a number no greater than {MAX_N_ITERATIVE}.")
            continue
        return n


def prompt_method(n):
    while True:
        choice = input("Method (1=Iterative, 2=Recursive, 3=Both/Verify): ").strip()
        if choice not in METHODS:
            print("  Error: Please enter 1, 2, or 3.")
            continue
        if choice in ("2", "3") and n > MAX_N_RECURSIVE:
            print(f"  Error: Recursive method supports n up to {MAX_N_RECURSIVE} "
                  f"(Python recursion limits). Choose Iterative (1) instead.")
            continue
        return choice


def prompt_nonempty(label):
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print("  Error: This field cannot be empty.")


def prompt_yes_no(label):
    while True:
        value = input(f"{label} (y/n): ").strip().lower()
        if value in ("y", "n"):
            return value == "y"
        print("  Error: Please enter 'y' or 'n'.")


# ---------------------------------------------------------------------------
# Core history-tracking class
# ---------------------------------------------------------------------------

class FactorialHistory:
    def __init__(self):
        self.entries = []
        self.load()

    # ---------------- Persistence ----------------
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

    # ---------------- Lookup ----------------
    def find_by_id(self, entry_id):
        for entry in self.entries:
            if entry["Entry ID"].lower() == entry_id.lower():
                return entry
        return None

    def next_id(self):
        max_num = 0
        for entry in self.entries:
            suffix = entry["Entry ID"][1:]
            if suffix.isdigit():
                max_num = max(max_num, int(suffix))
        return f"F{max_num + 1:03d}"

    # ---------------- Calculate (Add) ----------------
    def calculate(self):
        print("\n--- Calculate Factorial ---")
        n = prompt_number()
        choice = prompt_method(n)
        method = METHODS[choice]

        if choice == "1":
            result = iterative_factorial(n)
        elif choice == "2":
            result = compute_recursive_safely(n)
        else:
            iter_result = iterative_factorial(n)
            rec_result = compute_recursive_safely(n)
            if iter_result != rec_result:
                print("  Error: Iterative and recursive results did not match. Aborting.")
                return
            result = iter_result

        label = input("Optional label/note (press Enter to skip): ").strip()

        entry = {
            "Entry ID": self.next_id(),
            "Number": n,
            "Method": method,
            "Result": str(result),
            "Digits": len(str(result)),
            "Label": label if label else "(none)",
        }
        self.entries.append(entry)
        self.save()

        print()
        self.print_result_block(entry)

    # ---------------- Search ----------------
    def search(self):
        print("\n--- Search History ---")
        if not self.entries:
            print("  No history yet.")
            return
        print("Search by: 1) Entry ID  2) Number (n)  3) Method")
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            key = prompt_nonempty("Enter Entry ID")
            results = [e for e in self.entries if e["Entry ID"].lower() == key.lower()]
        elif choice == "2":
            key = prompt_nonempty("Enter Number (n)")
            try:
                key_n = int(key)
                results = [e for e in self.entries if e["Number"] == key_n]
            except ValueError:
                print("  Error: Not a valid integer.")
                return
        elif choice == "3":
            key = input("Enter Method (Iterative/Recursive/Both): ").strip().lower()
            results = [e for e in self.entries if key in e["Method"].lower()]
        else:
            print("  Error: Invalid option.")
            return

        if not results:
            print("  No matching entries found.")
        else:
            print(f"\n  {len(results)} matching entr{'y' if len(results) == 1 else 'ies'} found:")
            self.print_entries(results)

    # ---------------- Update label ----------------
    def update_label(self):
        print("\n--- Update Entry Label ---")
        entry_id = prompt_nonempty("Enter Entry ID to update")
        entry = self.find_by_id(entry_id)
        if not entry:
            print(f"  Error: No entry found with ID '{entry_id}'.")
            return
        print(f"Current label: {entry['Label']}")
        new_label = input("New label (press Enter to keep current): ").strip()
        if new_label:
            entry["Label"] = new_label
            self.save()
            print(f"  Entry '{entry_id}' updated successfully.")
        else:
            print("  No change made.")

    # ---------------- Delete ----------------
    def delete(self):
        print("\n--- Delete Entry ---")
        entry_id = prompt_nonempty("Enter Entry ID to delete")
        entry = self.find_by_id(entry_id)
        if not entry:
            print(f"  Error: No entry found with ID '{entry_id}'.")
            return
        if prompt_yes_no(f"Delete '{entry_id}' (n={entry['Number']}, {entry['Method']})?"):
            self.entries.remove(entry)
            self.save()
            print(f"  Entry '{entry_id}' deleted successfully.")
        else:
            print("  Deletion cancelled.")

    # ---------------- Display ----------------
    def print_result_block(self, entry):
        print(LINE)
        print(" FACTORIAL CALCULATION RESULT")
        print(LINE)
        self.print_entries([entry])
        print(LINE)

    def print_entries(self, entries):
        for i, e in enumerate(entries):
            print(f"Entry ID     : {e['Entry ID']}")
            print(f"Number (n)   : {e['Number']}")
            print(f"Method       : {e['Method']}")
            print(f"Result       : {e['Result']}")
            print(f"Digits       : {e['Digits']}")
            print(f"Label        : {e['Label']}")
            if i != len(entries) - 1:
                print(DASH)

    def display_all(self):
        print("\n" + LINE)
        print(" FACTORIAL CALCULATION HISTORY")
        print(LINE)
        if not self.entries:
            print("No history to display.")
            print(LINE)
            return
        self.print_entries(self.entries)
        print(LINE)
        total = len(self.entries)
        largest = max(e["Number"] for e in self.entries)
        most_digits_entry = max(self.entries, key=lambda e: e["Digits"])
        print(f"Total Calculations   : {total}")
        print(f"Largest n Computed   : {largest}")
        print(f"Most Digits          : {most_digits_entry['Digits']} (Entry {most_digits_entry['Entry ID']})")
        print(LINE)

    # ---------------- Statistics ----------------
    def statistics(self):
        print(LINE)
        print(" FACTORIAL STATISTICS SUMMARY")
        print(LINE)
        if not self.entries:
            print("No history to summarize.")
            print(LINE)
            return

        total = len(self.entries)
        largest = max(e["Number"] for e in self.entries)
        smallest = min(e["Number"] for e in self.entries)
        most_digits_entry = max(self.entries, key=lambda e: e["Digits"])
        avg_digits = sum(e["Digits"] for e in self.entries) / total
        iterative_count = sum(1 for e in self.entries if e["Method"] == "Iterative")
        recursive_count = sum(1 for e in self.entries if e["Method"] == "Recursive")
        both_count = sum(1 for e in self.entries if e["Method"] == "Both (Verified)")

        print(f"Total Calculations   : {total}")
        print(f"Largest n Computed   : {largest}")
        print(f"Smallest n Computed  : {smallest}")
        print(f"Most Digits          : {most_digits_entry['Digits']} "
              f"(Entry {most_digits_entry['Entry ID']}, n={most_digits_entry['Number']})")
        print(f"Iterative Used       : {iterative_count}")
        print(f"Recursive Used       : {recursive_count}")
        print(f"Both (Verified)      : {both_count}")
        print(f"Average Digits       : {avg_digits:.1f}")
        print(LINE)


# ---------------------------------------------------------------------------
# Menu / program flow
# ---------------------------------------------------------------------------

def print_menu():
    print("\n" + LINE)
    print(" FACTORIAL CALCULATOR & HISTORY TRACKER")
    print(LINE)
    print("1. Calculate Factorial")
    print("2. Search History")
    print("3. Update Entry Label")
    print("4. Delete Entry")
    print("5. Display All History")
    print("6. Statistics Summary")
    print("7. Exit")
    print(LINE)


def main():
    history = FactorialHistory()
    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()
        if choice == "1":
            history.calculate()
        elif choice == "2":
            history.search()
        elif choice == "3":
            history.update_label()
        elif choice == "4":
            history.delete()
        elif choice == "5":
            history.display_all()
        elif choice == "6":
            print()
            history.statistics()
        elif choice == "7":
            print("\nExiting Factorial Calculator. Goodbye!")
            break
        else:
            print("  Error: Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
