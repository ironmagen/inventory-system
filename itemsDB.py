import psycopg2


# Connection function
def create_connection(db_file):
    """Creates a database connection"""
    conn = psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    return conn


# Create the tables
def create_tables(conn):
    """Creates tables in the database"""
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        item_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        quantity INTEGER NOT NULL DEFAULT 0,
        quantity_unit TEXT,
        price DECIMAL(10, 2) NOT NULL,  # Adjust precision as needed
        reorder_point INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS item_categories (
        item_id INTEGER,
        category_id INTEGER,
        FOREIGN KEY (item_id) REFERENCES items(item_id),
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    )
    """)

    # table to explicitly track price history per item
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS item_price_history (
        id SERIAL PRIMARY KEY,
        item_id INTEGER,
        new_price DECIMAL,
        change_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (item_id) REFERENCES items(item_id)
    )
    ''')

    conn.commit()
    cursor.close()


if __name__ == "__main__":
    conn = create_connection("inventory.db")
    create_tables(conn)
    conn.close()
