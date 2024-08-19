# itemsDB.py

import sqlite3

# Create a database connection
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = sqlite3.connect(db_file)
    return conn


# Create the tables
def create_tables(conn):
    """ create tables in the database """
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        quantity INTEGER NOT NULL DEFAULT 0,
        quantity_unit TEXT,
        price REAL NOT NULL,
        reorder_point INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS item_categories (
        item_id INTEGER,
        category_id INTEGER,
        FOREIGN KEY (item_id) REFERENCES items(item_id),
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    )
    ''')

    conn.commit()
    cursor.close()


if __name__ == '__main__':
    conn = create_connection('inventory.db')
    create_tables(conn)
    conn.close()
