import sqlite3

# Create a database connection
def create_connection(db_file):
  """ create a database connection to a SQLite database """
  conn = sqlite3.connect(db_file)
  return conn

# Create the deliveries table
def create_table(conn):
  """ create a table in the database """
  cursor = conn.cursor()

  cursor.execute('''
  CREATE TABLE IF NOT EXISTS deliveries (
      vendor_id INTEGER REFERENCES vendors(vendor_id),
      delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
      delivery_date DATE NOT NULL,
      order_id INTEGER REFERENCES orders(order_id),
      FOREIGN KEY (order_id) REFERENCES orders(order_id)
  )
  ''')

  conn.commit()
  cursor.close()

def record_delivery(conn, delivery_data):
  """Records a new delivery in the database.

  Args:
    conn: The database connection.
    delivery_data: A dictionary containing delivery information like delivery date, order ID, etc.
  """
  cursor = conn.cursor()

  # Generate delivery ID
  cursor.execute("SELECT MAX(delivery_id) FROM deliveries")
  max_delivery_id = cursor.fetchone()[0]
  if max_delivery_id is None:
    delivery_id = 1
  else:
    delivery_id = max_delivery_id + 1

  delivery_date = delivery_data['delivery_date']
  order_id = delivery_data['order_id']

  # Check if order exists
  cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
  order = cursor.fetchone()
  if not order:
    raise ValueError(f"Order with ID {order_id} not found")

  # Insert delivery record
  cursor.execute("INSERT INTO deliveries (delivery_id, delivery_date, order_id) VALUES (?, ?, ?)", (delivery_id, delivery_date, order_id))

  # Update order status to 'delivered'
  cursor.execute("UPDATE orders SET status = 'delivered' WHERE order_id = ?", (order_id,))

  # Update item quantities based on delivered items
  delivered_items = delivery_data.get('delivered_items', [])
  for item in delivered_items:
    item_id = item['item_id']
    quantity = item['quantity']
    cursor.execute("UPDATE items SET quantity = quantity + ? WHERE item_id = ?", (quantity, item_id))

     # Verify item is in order
    cursor.execute("SELECT quantity FROM order_items WHERE order_id = ? AND item_id = ?", (order_id, item_id))
    order_item = cursor.fetchone()
    if not order_item or order_item[0] < quantity:
      raise ValueError(f"Invalid delivery quantity for item {item_id} in order {order_id}")

    # Update item quantity
    cursor.execute("UPDATE items SET quantity = quantity + ? WHERE item_id = ?", (quantity, item_id))

     # Check if all items in the order are delivered
  cursor.execute("SELECT COUNT(*) FROM order_items WHERE order_id = ?", (order_id,))
  total_items = cursor.fetchone()[0]
  cursor.execute("SELECT SUM(quantity) FROM order_items WHERE order_id = ?", (order_id,))
  total_delivered = cursor.fetchone()[0]
  if total_delivered == total_items:
    cursor.execute("UPDATE orders SET status = 'delivered' WHERE order_id = ?", (order_id,))

     # Insert initial delivery tracking record
  cursor.execute("INSERT INTO delivery_tracking (delivery_id, tracking_date, status) VALUES (?, ?, 'in_transit')", (delivery_id, delivery_date))

  # ... logic to update item quantities

  conn.commit()
  cursor.close()


if __name__ == '__main__':
  conn = create_connection('inventory.db')
  create_table(conn)
  conn.close()
