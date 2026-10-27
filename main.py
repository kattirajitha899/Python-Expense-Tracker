
import sqlite3
import logging
from datetime import date

# Set up logging
logging.basicConfig(
    filename="expense_tracker.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DATABASE = "expenses.db"


def connect_db():
    """Connect to the expense database."""
    return sqlite3.connect(DATABASE)


def create_table():
    """Create the expenses table if it does not exist."""
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                expense_date TEXT NOT NULL
            )
        """)


def add_expense():
    """Add a new expense."""
    try:
        title = input("Enter expense name: ").strip()
        if not title:
            raise ValueError("Expense name cannot be empty.")

        amount = float(input("Enter amount (₹): "))
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        category = input("Enter category: ").strip()
        if not category:
            raise ValueError("Category cannot be empty.")

        with connect_db() as conn:
            conn.execute(
                """INSERT INTO expenses
                   (title, amount, category, expense_date)
                   VALUES (?, ?, ?, ?)""",
                (title, amount, category, date.today().isoformat())
            )
        print("Expense added successfully!")

    except ValueError as error:
        print("Invalid input:", error)
    except sqlite3.Error as error:
        logging.exception("Database error while adding expense")
        print("Could not save the expense:", error)


def view_expenses():
    """Display all expenses."""
    try:
        with connect_db() as conn:
            rows = conn.execute(
                """SELECT id, title, amount, category, expense_date
                   FROM expenses ORDER BY id DESC"""
            ).fetchall()

        if not rows:
            print("No expenses recorded yet.")
            return

        print("\nID | Name | Amount | Category | Date")
        print("-" * 55)
        for row in rows:
            print(
                f"{row[0]} | {row[1]} | ₹{row[2]:.2f} | "
                f"{row[3]} | {row[4]}"
            )

    except sqlite3.Error as error:
        logging.exception("Database error while viewing expenses")
        print("Could not retrieve expenses:", error)


def delete_expense():
    """Delete an expense using its ID."""
    try:
        expense_id = int(input("Enter expense ID to delete: "))

        with connect_db() as conn:
            cursor = conn.execute(
                "DELETE FROM expenses WHERE id = ?", (expense_id,)
            )

        if cursor.rowcount:
            print("Expense deleted successfully!")
        else:
            print("No expense found with that ID.")

    except ValueError:
        print("Please enter a valid whole-number ID.")
    except sqlite3.Error as error:
        logging.exception("Database error while deleting expense")
        print("Could not delete the expense:", error)


def show_total():
    """Calculate the total expenses."""
    try:
        with connect_db() as conn:
            result = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) FROM expenses"
            ).fetchone()

        print(f"Total expenses: ₹{result[0]:.2f}")

    except sqlite3.Error as error:
        logging.exception("Database error while calculating total")
        print("Could not calculate the total:", error)


def main():
    create_table()

    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Delete expense")
        print("4. Show total expenses")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            show_total()
        elif choice == "5":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Please enter 1 to 5.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExpense Tracker closed.")
