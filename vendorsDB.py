import sqlite3

# Create a database connection
def create_connection(db_file):
  """ create a database connection to a SQLite database """
  conn = sqlite3.connect(db_file)
  return conn

# Create the vendors table
def create_tables(conn):
  """ create a table in the database """
  cursor = conn.cursor()

  cursor.execute('''
  CREATE TABLE IF NOT EXISTS vendors (
      vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      address TEXT,
      phone_number TEXT,
      email TEXT,
      payment_terms TEXT,
      credit_limit REAL,
      tax_id TEXT
  )
  ''')

  conn.commit()
  cursor.close()


if __name__ == '__main__':
  conn = create_connection('inventory.db')
  create_tables(conn)
  conn.close()