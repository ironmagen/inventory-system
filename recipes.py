import csv
import psycopg2

def update_inventory(sales_data, db_name, db_user, db_password, db_host):
    """
    Updates inventory quantity based on sales data in a CSV file.

    Args:
        sales_data (str): Path to the CSV file containing sales data.
        db_name (str): Name of the PostgreSQL database.
        db_user (str): Username for the PostgreSQL database.
        db_password (str): Password for the PostgreSQL database.
        db_host (str): Hostname or IP address of the PostgreSQL database server.
    """
    # Connect to PostgreSQL database
    conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
    cur = conn.cursor()

    # Read sales data from CSV file
    with open(sales_data, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Get sale item information
            sale_item_id = row['sale_item_id']

            # Prompt user for quantity
            quantity = int(input(f"Enter quantity for sale item {sale_item_id}: "))

            # Query for ingredient volumes for the sale item
            cur.execute("""
                SELECT i.id AS ingredient_id, si.volume
                FROM sales_items si
                INNER JOIN ingredients i ON si.ingredient_id = i.id
                WHERE si.sale_item_id = %s
            """, (sale_item_id,))

            # Update inventory quantity for each ingredient
            for ingredient in cur.fetchall():
                ingredient_id = ingredient[0]
                ingredient_volume = int(ingredient[1]) * quantity

                # Update query
                cur.execute("""
                    UPDATE items
                    SET quantity = quantity - %s
                    WHERE id = %s
                """, (ingredient_volume, ingredient_id))

    # Commit changes and close connection
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    # Replace with your database credentials
    db_name = "inventory"
    db_user = "your_username"
    db_password = "your_password"
    db_host = "localhost"

    # Replace with the path to your CSV file
    sales_data = "sales_items.csv"

    update_inventory(sales_data, db_name, db_user, db_password, db_host)
    # print("Inventory quantities updated successfully!")
