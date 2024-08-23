import sqlite3

import deliveryDB
import invoiceDB
import itemsDB
import orderDB
import vendorsDB


def create_database():
    """Creates the database and necessary tables."""
    conn = sqlite3.connect("inventory.db")
    itemsDB.create_tables(conn)
    vendorsDB.create_tables(conn)
    orderDB.create_tables(conn)
    deliveryDB.create_table(conn)
    invoiceDB.create_table(conn)
    conn.close()


def add_item(item_data):
    """Adds a new item to the inventory database.

    Args:
      item_data: A dictionary containing item information like name, description, quantity, price, and reorder point.
    """
    cursor = conn.cursor()
    conn = sqlite3.connect("inventory.db")
    itemsDB.add_item(conn, item_data)
    cursor.execute(
       
        "INSERT INTO item_price_history (item_id, new_price, change_date) VALUES (?, ?, ?)",
        (item_data['id'], item_data['price'], datetime.datetime.now())
        
    )
    
    conn.commit()
    conn.close()


def add_vendor(vendor_data):
    """Adds a new vendor to the inventory database.

    Args:
      vendor_data: A dictionary containing vendor information like name, address, phone number, etc.
    """
    conn = sqlite3.connect("inventory.db")
    vendorsDB.add_vendor(conn, vendor_data)
    conn.close()


def place_order(order_data):
    """Places a new order.

    Args:
      order_data: A dictionary containing order information like items, vendor, order date, etc.
    """
    conn = sqlite3.connect("inventory.db")
    orderDB.place_order(conn, order_data)
    conn.close()


def record_delivery(delivery_data):
    """Records a new delivery.

    Args:
      delivery_data: A dictionary containing delivery information like delivery date, order ID, etc.
    """
    conn = sqlite3.connect("inventory.db")
    deliveryDB.record_delivery(conn, delivery_data)
    conn.close()


def generate_invoice(order_id):
    """Generates an invoice for the specified order.

    Args:
      order_id: The ID of the order.
    """
    conn = sqlite3.connect("inventory.db")
    invoiceDB.generate_invoice(conn, order_id)
    conn.close()


# ... other functions for different functionalities

if __name__ == "__main__":
    create_database()
    # Example usage:
    # ...
