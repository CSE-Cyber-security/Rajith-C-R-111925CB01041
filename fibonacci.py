"""
Fibonacci Series Generator
GitHub Task - Week 03

Prints the first n terms of the Fibonacci sequence
(0, 1, 1, 2, 3, 5, 8, 13, ...) for a user-supplied n.

Run:
    python src/fibonacci.py
"""


def generate_fibonacci(n):
    """Return a list containing the first n Fibonacci numbers."""
    series = []
    a, b = 0, 1
    for _ in range(n):
        series.append(a)
        a, b = b, a + b
    return series


def prompt_terms():
    """Prompt for a non-negative integer number of terms, re-prompting
    on empty input, non-integer input, or a negative number."""
    while True:
        value = input("Enter the number of terms: ").strip()
        if not value:
            print("  Error: This field cannot be empty.")
            continue
        try:
            n = int(value)
        except ValueError:
            print(f"  Error: '{value}' is not a valid integer.")
            continue
        if n < 0:
            print("  Error: Number of terms cannot be negative.")
            continue
        return n


def prompt_yes_no(label):
    while True:
        value = input(f"{label} (y/n): ").strip().lower()
        if value in ("y", "n"):
            return value == "y"
        print("  Error: Please enter 'y' or 'n'.")


def main():
    while True:
        n = prompt_terms()
        series = generate_fibonacci(n)
        print("Fibonacci Series:")
        print(" ".join(str(term) for term in series))
        print()
        if not prompt_yes_no("Calculate again?"):
            print("Goodbye!")
            break
        print()


if __name__ == "__main__":
    main()
