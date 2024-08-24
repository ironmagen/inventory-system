import sqlite3


def record_sales(sales_data):
    """
    Records sales data and updates inventory quantities.

    Args:
      sales_data: A list of dictionaries, each containing 'date', 'category', 'sales_items' (list of dictionaries with 'item_id', 'quantity', and 'recipe_id' (optional)).
    """

    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Create prepared statements
    insert_sales_item = cursor.prepare(
        "INSERT INTO sales_items (sale_id, item_id, quantity, recipe_id) VALUES (?, ?, ?, ?)"
    )
    update_item_quantity = cursor.prepare(
        "UPDATE items SET quantity = quantity - ? WHERE item_id = ?"
    )

    for sale in sales_data:
        sale_date = sale["date"]
        category = sale["category"]
        sales_items = sale["sales_items"]

        # Insert sale record (optional)
        # ... logic to insert sale record into a sales table

        for sales_item in sales_items:
            item_id = sales_item["item_id"]
            quantity = sales_item["quantity"]
            recipe_id = sales_item.get("recipe_id")

            # Update sales item quantity (if applicable)
            # ... logic to update sales item quantity (e.g., in sales_items table)

            if recipe_id:
                # Retrieve recipe ingredients
                cursor.execute(
                    "SELECT ingredient_id, quantity FROM recipe_ingredients WHERE recipe_id = ?",
                    (recipe_id,),
                )
                ingredients = cursor.fetchall()

                # Calculate inventory consumption
                for ingredient in ingredients:
                    ingredient_id, recipe_quantity = ingredient
                    ingredient_consumption = recipe_quantity * quantity
                    cursor.execute(
                        "UPDATE items SET quantity = quantity - ? WHERE item_id = ?",
                        (ingredient_consumption, ingredient_id),
                    )
            else:
                # Handle direct item consumption
                cursor.execute(
                    "UPDATE items SET quantity = quantity - ? WHERE item_id = ?",
                    (quantity, item_id),
                )

    conn.commit()
    conn.close()
