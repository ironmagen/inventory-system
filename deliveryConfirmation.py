import psycopg2

def record_delivery(delivery_data, db_name, user, password, host, port):
    """Records a delivery, updating inventory and order status.

    Args:
        delivery_data (dict): A dictionary containing the following keys:
            - order_id (int): The ID of the order being delivered.
            - items (list): A list of dictionaries, each representing an item in the delivery.
                - item_id (int): The ID of the item.
                - quantity (int): The quantity of the item being delivered.
                - confirmed_quantity (int, optional): The confirmed quantity of the item being delivered (default: None).
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

    # Retrieve ordered quantities
    cursor.execute(
        "SELECT item_id, quantity FROM order_items WHERE order_id = ?",
        (delivery_data["order_id"],),
    )
    order_items = cursor.fetchall()
    order_item_map = {item[0]: item[1] for item in order_items}

    # Update item quantities
    for item in delivery_data["items"]:
        item_id = item["item_id"]
        delivered_quantity = item["quantity"]
        confirmed_quantity = item.get("confirmed_quantity", None)

        if item_id in order_item_map:
            ordered_quantity = order_item_map[item_id]
            if confirmed_quantity is None:
                confirmed_quantity = delivered_quantity

            if confirmed_quantity > ordered_quantity:
                raise ValueError(
                    f"Delivered quantity exceeds ordered quantity for item {item_id}"
                )

            cursor.execute(
                "UPDATE items SET quantity = quantity + ? WHERE item_id = ?",
                (delivered_quantity, item_id),
            )

    # Update order status (if all items delivered)
    cursor.execute(
        "SELECT COUNT(*) FROM order_items WHERE order_id = ? AND fulfilled = 0",
        (delivery_data["order_id"],),
    )
    unfulfilled_items = cursor.fetchone()[0]

    if unfulfilled_items == 0:
        cursor.execute(
            'UPDATE orders SET status = "delivered" WHERE order_id = ?',
            (delivery_data["order_id"],),
        )

    conn.commit()
    conn.close()
