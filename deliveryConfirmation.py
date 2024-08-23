import sqlite3

def record_delivery(delivery_data):
  conn = sqlite3.connect('inventory.db')
  cursor = conn.cursor()

  # Retrieve ordered quantities
  cursor.execute('SELECT item_id, quantity FROM order_items WHERE order_id = ?', (delivery_data['order_id'],))
  order_items = cursor.fetchall()
  order_item_map = {item[0]: item[1] for item in order_items}

  # Update item quantities
  for item in delivery_data['items']:
    item_id = item['item_id']
    delivered_quantity = item['quantity']

    if item_id in order_item_map:
      ordered_quantity = order_item_map[item_id]
      if delivered_quantity > ordered_quantity:
        raise ValueError(f"Delivered quantity exceeds ordered quantity for item {item_id}")

      cursor.execute('UPDATE items SET quantity = quantity + ? WHERE item_id = ?', (delivered_quantity, item_id))

  # Update order status (if all items delivered)
  cursor.execute('SELECT COUNT(*) FROM order_items WHERE order_id = ? AND fulfilled = 0', (delivery_data['order_id'],))
  unfulfilled_items = cursor.fetchone()[0]

  if unfulfilled_items == 0:
    cursor.execute('UPDATE orders SET status = "delivered" WHERE order_id = ?', (delivery_data['order_id'],))

  conn.commit()
  conn.close()

