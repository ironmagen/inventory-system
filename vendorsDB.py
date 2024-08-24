import psycopg2


# Create a database connection
def create_connection(db_file):
    """Creates a database connection to a PostgreSQL database"""
    conn = psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    return conn


# Create the vendors table
def create_vendor_table(conn):
    """Creates the vendors table in the database."""
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendors (
        vendor_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        address TEXT,
        phone_number TEXT,
        email TEXT,
        payment_terms TEXT,
        credit_limit NUMERIC(10, 2),  # Adjust precision as needed
        tax_id TEXT
    )
    """)

    conn.commit()
    cursor.close()


if __name__ == "__main__":
    conn = create_connection("inventory.db")
    create_vendor_table(conn)
    conn.close()
