import psycopg2


def verify_delivery(order_id, delivered_items, db_name, user, password, host, port):
    """
    Verifies a delivery based on user input.

    Args:
        order_id: The ID of the order.
        delivered_items: A list of dictionaries, each containing 'item_id' and 'quantity'.
        db_name (str): PostgreSQL database name.
        user (str): Database username.
        password (str): Database password.
        host (str): Database host.
        port (int): Database port.
    """

    conn = psycopg2.connect(
        dbname=db_name, user=user, password=password, host=host, port=port
    )
    cursor = conn.cursor()

    # Retrieve order details
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()
    if not order:
        conn.close()
        raise ValueError("Order not found")

    # Retrieve ordered quantities
    cursor.execute(
        "SELECT item_id, quantity FROM order_items WHERE order_id = ?", (order_id,)
    )
    order_items = cursor.fetchall()
    order_item_map = {item[0]: item[1] for item in order_items}

    # Verify and update item quantities
    for delivered_item in delivered_items:
        item_id = delivered_item["item_id"]
        received_quantity = delivered_item["quantity"]

        if item_id not in order_item_map:
            raise ValueError(f"Item {item_id} not found in order {order_id}")

        ordered_quantity = order_item_map[item_id]
        if received_quantity != ordered_quantity:
            # Allow user to confirm quantity

            # Update item quantity
            cursor.execute(
                "UPDATE items SET quantity = quantity + ? WHERE item_id = ?",
                (received_quantity, item_id),
            )

    # Update order status (if all items delivered)
    # ... same logic as in deliverConfirmation.py

    conn.commit()
    conn.close()
