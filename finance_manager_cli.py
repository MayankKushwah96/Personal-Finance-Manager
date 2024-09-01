import argparse
import sqlite3
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable

def validate_transaction(amount, date, category, description, type):
    if amount <= 0:
        raise ValueError("Amount must be a positive number.")
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")
    if not category.strip():
        raise ValueError("Category must not be empty.")
    if not description.strip():
        raise ValueError("Description must not be empty.")
    if type not in ['income', 'expense']:
        raise ValueError("Type must be either 'income' or 'expense'.")

def add_transaction(args=None):
    conn = sqlite3.connect('finance_manager.db')
    cursor = conn.cursor()

    print("\n-----------------------")
    print(" Add a New Transaction ")
    print("-----------------------\n")

    if not args:
    
        amount = float(input("Enter the transaction amount: "))
        date = input("Enter the transaction date (YYYY-MM-DD): ")
        category = input("Enter the transaction category: ")
        description = input("Enter the transaction description: ")
        type = input("Enter the transaction type (income/expense): ")
    else:
        amount = args.amount
        date = args.date
        category = args.category
        description = args.description
        type = args.type

    try:
        validate_transaction(amount, date, category, description, type)
    except ValueError as e:
        print(f"Validation Error: {e}")
        conn.close()
        return

    cursor.execute('SELECT SUM(amount) FROM transactions WHERE type = "income"')
    total_income = cursor.fetchone()[0] or 0

    cursor.execute('SELECT SUM(amount) FROM transactions WHERE type = "expense"')
    total_expenses = cursor.fetchone()[0] or 0

    if type == 'expense' and (total_expenses + amount) > total_income:
        print("Error: Adding this expense would exceed your total income. Please adjust the amount or add more income first.")
    else:
        cursor.execute('SELECT id FROM categories WHERE name = ?', (category,))
        category_row = cursor.fetchone()
        if category_row is None:
            cursor.execute('INSERT INTO categories (name) VALUES (?)', (category,))
            category_id = cursor.lastrowid
        else:
            category_id = category_row[0]

        cursor.execute('''
        INSERT INTO transactions (amount, date, category_id, description, type)
        VALUES (?, ?, ?, ?, ?)
        ''', (amount, date, category_id, description, type))

        conn.commit()
        print(f"Transaction added: {amount} on {date} for {category}")

    conn.close()

def view_transactions(args):
    conn = sqlite3.connect('finance_manager.db')
    cursor = conn.cursor()

    query = '''
    SELECT transactions.id, transactions.amount, transactions.date, categories.name, transactions.description, transactions.type 
    FROM transactions 
    INNER JOIN categories ON transactions.category_id = categories.id 
    WHERE 1=1
    '''
    params = []

    if hasattr(args, 'category') and args.category:
        query += ' AND categories.name = ?'
        params.append(args.category)

    if hasattr(args, 'date') and args.date:
        query += ' AND transactions.date = ?'
        params.append(args.date)

    if hasattr(args, 'type') and args.type:
        query += ' AND transactions.type = ?'
        params.append(args.type)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["ID", "Amount", "Date", "Category", "Description", "Type"]
    
    for row in rows:
        table.add_row(row)
    
    print(table)

    conn.close()


def load_transactions_to_dataframe():
    conn = sqlite3.connect('finance_manager.db')
    query = '''
    SELECT t.amount, t.date, c.name as category, t.description, t.type
    FROM transactions t
    JOIN categories c ON t.category_id = c.id
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def calculate_financial_summary():
    df = load_transactions_to_dataframe()
    total_income = df[df['type'] == 'income']['amount'].sum()
    total_expense = df[df['type'] == 'expense']['amount'].sum()
    net_savings = total_income - total_expense
    print()
    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expense}")
    print(f"Net Savings: {net_savings}")

def generate_financial_report():
    df = load_transactions_to_dataframe()
    
    income_expense = df.groupby('type')['amount'].sum()
    income_expense.plot(kind='bar', title='Income vs. Expenses')
    plt.ylabel('Amount')
    plt.show()
    
    category_spending = df.groupby('category')['amount'].sum()
    category_spending.plot(kind='pie', autopct='%1.1f%%', title='Spending by Category')
    plt.show()

def generate_report(args=None):
    calculate_financial_summary()
    generate_financial_report()

def interactive_menu():
    while True:
        print("--------------------------")
        print(" Personal Finance Manager ")
        print("--------------------------\n")

        print("1. Add a new transaction")
        print("2. View transactions")
        print("3. Generate a financial report")
        print("4. Exit")
        print()
        choice = input("Choose an option: ")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions(argparse.Namespace())
        elif choice == '3':
            generate_report()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

def main():
    parser = argparse.ArgumentParser(description="Personal Finance Manager CLI")
    
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    
    add_parser = subparsers.add_parser("add_transaction", help="Add a new transaction")
    add_parser.add_argument("amount", type=float, help="Amount of the transaction")
    add_parser.add_argument("date", type=str, help="Date of the transaction (YYYY-MM-DD)")
    add_parser.add_argument("category", type=str, help="Category of the transaction")
    add_parser.add_argument("description", type=str, help="Description of the transaction")
    add_parser.add_argument("type", type=str, choices=["income", "expense"], help="Type of the transaction")
    add_parser.set_defaults(func=add_transaction)
    
    view_parser = subparsers.add_parser("view_transactions", help="View transactions")
    view_parser.add_argument("--category", type=str, help="Filter by category")
    view_parser.add_argument("--date", type=str, help="Filter by date (YYYY-MM-DD)")
    view_parser.add_argument("--type", type=str, choices=["income", "expense"], help="Filter by type")
    view_parser.set_defaults(func=view_transactions)
    
    report_parser = subparsers.add_parser("generate_report", help="Generate a financial report")
    report_parser.set_defaults(func=generate_report)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        interactive_menu()  
    else:
        args.func(args)

if __name__ == "__main__":
    main()
