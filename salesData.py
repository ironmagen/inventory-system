import csv
import psycopg2

def record_sales_from_csv(csv_file, db_name, db_user, db_password, db_host):
    """
    Records sales data from a CSV file and updates inventory quantities.

    Args:
        csv_file: Path to the CSV file containing sales data.
        db_name: Name of the PostgreSQL database.
        db_user: Username for the PostgreSQL database.
        db_password: Password for the PostgreSQL database.
        db_host: Hostname or IP address of the PostgreSQL database server.
    """

    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host
    )
    cursor = conn.cursor()

    # Create prepared statements
    insert_sale = cursor.prepare(
        "INSERT INTO sales (date, category) VALUES (?, ?)"
    )
    insert_sales_item = cursor.prepare(
        "INSERT INTO sales_items (sale_id, item_id, quantity, recipe_id) VALUES (?, ?, ?, ?)"
    )
    update_item_quantity = cursor.prepare(
        "UPDATE items SET quantity = quantity - ? WHERE item_id = ?"
    )

    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sale_date = row['date']
            category = row['category']
            item_id = row['item_id']
            quantity = int(row['quantity'])
            recipe_id = row.get('recipe_id')

            # Insert sale record
            cursor.execute(insert_sale, (sale_date, category))
            sale_id = cursor.lastrowid

            # Insert sale item
            cursor.execute(insert_sales_item, (sale_id, item_id, quantity, recipe_id))

            # Update inventory quantity
            if recipe_id:
                # Retrieve recipe ingredients
                cursor.execute(
                    "SELECT ingredient_id, quantity FROM recipe_ingredients WHERE recipe_id = ?",
                    (recipe_id,),
                )
                ingredients = cursor.fetchall()

                # Calculate inventory consumption
                for ingredient_id, recipe_quantity in ingredients:
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
    cursor.close()
    conn.close()

if __name__ == "__main__":
    # Replace with your database credentials and CSV file path
    db_name = "your_database_name"
    db_user = "your_username"
    db_password = "your_password"
    db_host = "your_host"
    csv_file = "sales_data.csv"

    record_sales_from_csv(csv_file, db_name, db_user, db_password, db_host)
