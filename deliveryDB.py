import psycopg2

# Create a database connection
def create_connection(db_name, user, password, host, port):
    """Create a database connection to a PostgreSQL database."""
    conn = psycopg2.connect(
        dbname=db_name, user=user, password=password, host=host, port=port
    )
    return conn

# Create the deliveries table
def create_table(conn):
    """Create a table in the database."""
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deliveries (
        delivery_id SERIAL PRIMARY KEY,
        delivery_date DATE NOT NULL,
        order_id INTEGER REFERENCES orders(order_id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    cursor.close()

def record_delivery(conn, delivery_data):
    """Records a new delivery in the database.

    Args:
        conn: The database connection.
        delivery_data: A dictionary containing delivery information like delivery date, order ID, etc.
    """
    cursor = conn.cursor()

    delivery_date = delivery_data['delivery_date']
    order_id = delivery_data['order_id']

    # Check if order exists and is not already delivered
    cursor.execute("SELECT * FROM orders WHERE order_id = ? AND status != 'delivered'", (order_id,))
    order = cursor.fetchone()
    if not order:
        raise ValueError(f"Order with ID {order_id} not found or already delivered")

    # Insert delivery record
    cursor.execute("INSERT INTO deliveries (delivery_date, order_id) VALUES (?, ?)", (delivery_date, order_id))

    # ... rest of your logic with appropriate PostgreSQL syntax

    conn.commit()
    cursor.close()

if __name__ == '__main__':
    conn = create_connection("your_database_name", "your_username", "your_password", "your_host", "your_port")
    create_table(conn)
    conn.close()
