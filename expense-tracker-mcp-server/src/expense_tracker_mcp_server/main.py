import csv
from pathlib import Path
from datetime import datetime
from fastmcp import FastMCP

mcp = FastMCP("Expense Tracker")

# Store expenses inside the project
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

EXPENSE_FILE = DATA_DIR / "expenses.csv"


def initialize_csv():
    """Create the CSV file with headers if it doesn't exist."""
    if not EXPENSE_FILE.exists():
        with open(EXPENSE_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "date",
                "amount",
                "category",
                "description"
            ])


@mcp.tool()
def add_expense(
    amount: float,
    category: str,
    description: str = ""
) -> str:
    """
    Add a new expense.

    Example:
    User says: "I spent 500 rupees on food"

    amount = 500
    category = food
    """

    initialize_csv()

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(EXPENSE_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            date,
            amount,
            category.lower(),
            description
        ])

    return f"Expense added: ₹{amount} for {category}"


@mcp.tool()
def list_expenses(category: str = "") -> list[dict]:
    """
    Return saved expenses.

    If category is provided, return only expenses
    from that category.
    """

    initialize_csv()

    expenses = []

    with open(EXPENSE_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:

            if category:
                if row["category"].lower() != category.lower():
                    continue

            expenses.append(row)

    return expenses


@mcp.tool()
def get_total_expenses(category: str = "") -> dict:
    """
    Calculate total spending.

    Optionally filter by category.
    """

    initialize_csv()

    total = 0
    count = 0

    with open(EXPENSE_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:

            if category:
                if row["category"].lower() != category.lower():
                    continue

            total += float(row["amount"])
            count += 1

    return {
        "category": category if category else "all",
        "total": round(total, 2),
        "number_of_expenses": count
    }


@mcp.tool()
def export_expenses_csv(
    filename: str = "expense_report.csv"
) -> str:
    """
    Export all expenses into a separate CSV file.
    """

    initialize_csv()

    export_path = DATA_DIR / filename

    with open(EXPENSE_FILE, "r", encoding="utf-8") as source:
        content = source.read()

    with open(export_path, "w", encoding="utf-8") as destination:
        destination.write(content)

    return f"CSV exported successfully to: {export_path}"


if __name__ == "__main__":
    mcp.run()