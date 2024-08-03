import sqlite3
import os


def initialize_database(dbsq_path):

    os.makedirs(os.path.dirname(dbsq_path), exist_ok=True)

    conn = sqlite3.connect(dbsq_path)
    cursor = conn.cursor()

    # Items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        item_type TEXT NOT NULL,
        description TEXT,
        weight REAL,
        quantity INTEGER DEFAULT 1
    )
    ''')

    # We can add more tables here?

    conn.commit()
    conn.close()

    print(f"Database initialized at {dbsq_path}")


if __name__ == "__main__":
    # We can run this script directly to initialize the database
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'inventory.sqlite')
    initialize_database(db_path)
