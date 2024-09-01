import sqlite3

def delete_table_data():
    conn = sqlite3.connect('finance_manager.db')
    cursor = conn.cursor()

    # Delete all data from tables
    cursor.execute('DELETE FROM transactions')
    cursor.execute('DELETE FROM categories')

    conn.commit()
    conn.close()
    print("All data from tables has been deleted.")

if __name__ == "__main__":
    delete_table_data()
