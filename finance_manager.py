import sqlite3
from datetime import datetime, timedelta
import random
import os

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_amount(amount):
    return amount > 0

def setup_database():
    conn = sqlite3.connect('finance_manager.db')
    conn.execute("PRAGMA foreign_keys = ON")  
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        category_id INTEGER NOT NULL,
        description TEXT,
        type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON transactions(date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category_id ON transactions(category_id)')

    conn.commit()
    conn.close()

def add_transaction(amount, date, category, description, type_):
    if not validate_date(date):
        print(f"Invalid date format: {date}. Please use YYYY-MM-DD.")
        return
    if not validate_amount(amount):
        print(f"Invalid amount: {amount}. Amount must be positive.")
        return

    conn = sqlite3.connect('finance_manager.db')
    conn.execute("PRAGMA foreign_keys = ON")  
    cursor = conn.cursor()

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
    ''', (amount, date, category_id, description, type_))

    conn.commit()
    conn.close()

def generate_random_transactions(n):
    categories = ['Salary', 'Rent', 'Groceries', 'Entertainment', 'Utilities', 'Dining Out', 'Health', 'Transport']
    descriptions = ['Monthly income', 'House rent', 'Grocery shopping', 'Movie night', 'Electricity bill', 'Dinner', 'Medical expenses', 'Bus fare']
    types = ['income', 'expense']

    start_date = datetime.now() - timedelta(days=365)  
    total_income = 0
    max_expenses = 0

    # Generate income first
    for _ in range(n // 4):
        amount = round(random.uniform(500, 2000), 2)  
        date = (start_date + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        category = 'Salary'
        description = 'Monthly salary'
        type_ = 'income'
        
        add_transaction(amount, date, category, description, type_)
        total_income += amount

    
    max_expenses = total_income * 0.8  

    for _ in range(n // 4):
        amount = round(random.uniform(10, 500), 2)  
        date = (start_date + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        category = random.choice(categories)
        description = random.choice(descriptions)
        type_ = 'expense'
        
        if max_expenses >= amount:
            add_transaction(amount, date, category, description, type_)
            max_expenses -= amount
        else:
            print(f"Skipped expense of {amount}. Exceeds allowed expenses limit.")

setup_database()
generate_random_transactions(100)
