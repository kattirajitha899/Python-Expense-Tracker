

# Personal Expense Tracker

## Project Description
A Python application that helps users record, view, and delete expenses and calculate total spending.

## Features
- Add expenses with name, amount, category, and date
- View all saved expenses
- Delete expenses by ID
- Calculate total expenses
- Store data in an SQLite database
- Validate user input and log database errors

## Technologies Used
- Python
- SQLite
- Logging module

## Requirements
- Python 3.10 or later
- No external Python packages required

## Installation and Setup
1. Install Python.
2. Download or clone this repository.
3. Open the project folder in a terminal.
4. Run the application:

   `python main.py`

## Database Schema
The `expenses` table contains:
- `id`: Unique expense ID
- `title`: Expense name
- `amount`: Expense amount
- `category`: Expense category
- `expense_date`: Date of the expense

The database file `expenses.db` is created automatically when the application runs.

## Logging
Database errors are recorded in `expense_tracker.log`.

## Future Improvements
- Edit existing expenses
- Filter expenses by category and date
- Export expenses to CSV
- Add a graphical user interface
