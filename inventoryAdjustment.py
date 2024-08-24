import psycopg2

def create_audit_log_table(conn):
    """Creates the inventory_adjustments table for auditing purposes."""
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory_adjustments (
        adjustment_id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id INTEGER,  # Foreign key to users table (if applicable)
        item_id INTEGER REFERENCES items(item_id),
        previous_quantity INTEGER,
        new_quantity INTEGER,
        quantity_difference INTEGER,
        reason TEXT,
        category_id INTEGER,  # Foreign key to categories table (optional)
        vendor_id INTEGER  # Foreign key to vendors table (optional)
    )
    """)

    conn.commit()
    cursor.close()

def create_category_totals_table(conn):
    """Creates the category_totals table for tracking category quantities."""
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS category_totals (
        category_id INTEGER PRIMARY KEY REFERENCES categories(category_id),
        total_quantity INTEGER
    )
    """)

    conn.commit()
    cursor.close()

def create_vendor_totals_table(conn):
    """Creates the vendor_totals table for tracking vendor quantities."""
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendor_totals (
        vendor_id INTEGER PRIMARY KEY REFERENCES vendors(vendor_id),
        total_quantity INTEGER
    )
    """)

    conn.commit()
    cursor.close()

def adjustInventory(adjustments, userId=None):
    """Adjusts inventory quantities based on user input.

    Args:
        adjustments: A list of dictionaries, each containing 'itemId', 'newQuantity', 'category' (optional), and 'vendor' (optional).
        userId: The ID of the user making the adjustment (optional).
    """

    conn = psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    cursor = conn.cursor()

    create_audit_log_table(conn)
    create_category_totals_table(conn)
    create_vendor_totals_table(conn)

    for adjustment in adjustments:
        itemId = adjustment["itemId"]
        newQuantity = adjustment["newQuantity"]
        category = adjustment.get("category")
        vendor = adjustment.get("vendor")

        # Retrieve current quantity
        cursor.execute("SELECT quantity FROM items WHERE item_id = ?", (itemId,))
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Item with ID {itemId} not found")
        currentQuantity = result[0]

        # Calculate difference
        quantityDifference = newQuantity - currentQuantity

        # Update item quantity
        cursor.execute(
            "UPDATE items SET quantity = ? WHERE item_id = ?", (newQuantity, itemId)
        )

        # Log adjustment
        cursor.execute(
            """
            INSERT INTO inventory_adjustments (user_id, item_id, previous_quantity, new_quantity, quantity_difference, category_id, vendor_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                userId,
                itemId,
                currentQuantity,
                newQuantity,
                quantityDifference,
                category,
                vendor,
            ),
        )

        # Update category and vendor totals
        if category:
            cursor.execute(
                "UPDATE category_totals SET total_quantity = total_quantity + ? WHERE category_id = ?",
                (quantityDifference, category),
            )
            cursor.execute(
                "INSERT OR IGNORE INTO category_totals (category_id, total_quantity) VALUES (?, ?)",
                (category, quantityDifference),
            )
        if vendor:
            cursor.execute(
                "UPDATE vendor_totals SET total_quantity = total_quantity + ? WHERE vendor_id = ?",
                (quantityDifference, vendor),
            )
            cursor.execute(
                "INSERT OR IGNORE INTO vendor_totals (vendor_id, total_quantity) VALUES (?, ?)",
                (vendor, quantityDifference),
            )

    conn.commit()
    conn.close()
