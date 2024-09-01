# Personal Finance Manager CLI

## Description

The **Personal Finance Manager CLI** is a command-line tool that helps users manage their personal finances efficiently. Users can add transactions, view transaction history, and generate financial reports directly from the terminal. The application is built using Python and SQLite, with a focus on ease of use, flexibility, and interactivity.

## Features

- **Add New Transactions**: Add income or expense transactions with details like amount, date, category, and description.
- **View Transactions**: View all transactions, filtered by category, date, or type (income/expense).
- **Generate Financial Reports**: Create summary reports based on your financial data.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/MayankKushwah96/Personal-Finance-Manager.git
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   ```
   
3. **Activate Virtual Environment**
   ```bash
   venv\Scripts\activate
   ```
   
4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the Application:**
   ```bash
   python finance_manager_cli.py
    ```
   This will present you with a menu to choose from:
   - Add a new transaction
   - View transactions
   - Generate a financial report
   - Exit

## Command-Line Mode
You can also use the CLI directly with specific commands:

**Add a Transaction**
```bash
python finance_manager_cli.py add_transaction <amount> <date> <category> <description> <type>
```

**Example:**
```bash
python finance_manager_cli.py add_transaction 100.0 2024-09-01 Groceries "Weekly grocery shopping" expense
```

**View Transactions**
```bash
python finance_manager_cli.py view_transactions [--category <category>] [--date <YYYY-MM-DD>] [--type <income|expense>]
```

**Example:**
```bash
python finance_manager_cli.py view_transactions --category Groceries --type expense
```
**Generate a Financial Report**
```bash
python finance_manager_cli.py generate_report
```

This command will display a summary of your financial status and generate visual reports.

## Database
The transactions and categories are stored in an SQLite database named finance_manager.db. The database will be created automatically when you add your first transaction.

## Dependencies

- **argparse:** Used for parsing command-line options and arguments.
- **pandas:** Data manipulation and analysis library.
- **prettytable:** Library for displaying tabular data in the terminal.
- **matplotlib:** Library for creating static, animated, and interactive visualizations.
