import psycopg2
import deliveryDB
import invoiceDB
import itemsDB
import orderDB
import vendorsDB
import datetime

def create_database():
    """Creates the database and necessary tables."""
    with psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    ) as conn:
        itemsDB.create_tables(conn)
        vendorsDB.create_tables(conn)
        orderDB.create_tables(conn)
        deliveryDB.create_table(conn)
        invoiceDB.create_table(conn)


def add_item(item_data):
    """Adds a new item to the inventory database.

    Args:
        item_data: A dictionary containing item information like name, description, quantity, price, and reorder point.

    Raises:
        Exception: If an error occurs while adding the item.
    """
    with psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    ) as conn:
        try:
            itemsDB.add_item(conn, item_data)
            conn.execute(
                "INSERT INTO item_price_history (item_id, new_price, change_date) VALUES (?, ?, ?)",
                (item_data["id"], item_data["price"], datetime.datetime.now()),
            )
            conn.commit()
        except Exception as e:
            raise Exception(f"Error adding item: {e}")


def add_vendor(vendor_data):
    """Adds a new vendor to the inventory database.

    Args:
        vendor_data: A dictionary containing vendor information like name, address, phone number, etc.

    Raises:
        Exception: If an error occurs while adding the vendor.
    """
    with psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    ) as conn:
        try:
            vendorsDB.add_vendor(conn, vendor_data)
            conn.commit()
        except Exception as e:
            raise Exception(f"Error adding vendor: {e}")


def place_order(order_data):
    """Places a new order.

    Args:
        order_data: A dictionary containing order information like items, vendor, order date, etc.

    Raises:
        Exception: If an error occurs while placing the order.
    """
    with psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    ) as conn:
        try:
            orderDB.place_order(conn, order_data)
            conn.commit()
        except Exception as e:
            raise Exception(f"Error placing order: {e}")


def record_delivery(delivery_data):
    """Records a new delivery.

    Args:
        delivery_data: A dictionary containing delivery information like delivery date, order ID, etc.

    Raises:
        Exception: If an error occurs while recording the delivery.
    """
    with psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    ) as conn:
        try:
            deliveryDB.record_delivery(conn, delivery_data)
            conn.commit()
        except Exception as e:
            raise Exception(f"Error recording delivery: {e}")


def generate_invoice(order_id):
    """Generates an invoice for the specified order.

    Args:
        order_id: The ID of the order.

    Raises:
        Exception: If an error occurs while generating the invoice.
    """
    with psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    ) as conn:
        try:
            invoiceDB.generate_invoice(conn, order_id)
            conn.commit()
        except Exception as e:
            raise Exception(f"Error generating invoice: {e}")


# ... other functions for different functionalities

if __name__ == "__main__":
    create_database()
    # Example usage:
    # ...
