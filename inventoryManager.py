from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import os
import itemsDB
import vendorsDB
import orderDB
import deliveryDB
import invoiceDB
import datetime
from flaskConfig import POSTGRES_CONNECTION_STRING, UPLOAD_FOLDER, ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Extracted functions

def get_form_data():
    return {
        'name': request.form['name'],
        'description': request.form['description'],
        'price': float(request.form['price']),
        'quantity': int(request.form['quantity']),
        'reorder_point': int(request.form['reorder_point'])
    }

def execute_db_query(query, params):
    conn = psycopg2.connect(POSTGRES_CONNECTION_STRING)
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()

def handle_error(e):
    return str(e), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
           POSTGRES_CONNECTION_STRING 
        )
        conn.autocommit = True
        return conn
    except psycopg2.Error as e:
        error_message = f"Database connection error: {e.pgerror}"
        return render_template('error.html', error_message=error_message), 500

# Create database and tables (if not already created)
def create_database():
    try:
        conn = get_db_connection()
        itemsDB.create_tables(conn)
        vendorsDB.create_tables(conn)
        orderDB.create_tables(conn)
        deliveryDB.create_table(conn)
        invoiceDB.create_table(conn)
        conn.close()
    except psycopg2.Error as e:
        error_message = f"Database creation error: {e.pgerror}"
        return render_template('error.html', error_message=error_message), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items')
def items():
    conn = psycopg2.connect(POSTGRES_CONNECTION_STRING)
    cur = conn.cursor()
    cur.execute("SELECT * FROM items")
    items = cur.fetchall()
    conn.close()
    return render_template('items.html', items=items)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        try:
            item_data = get_form_data()
            execute_db_query("INSERT INTO items (name, description, price, quantity, reorder_point) VALUES (%s, %s, %s, %s, %s)", 
                             (item_data['name'], item_data['description'], item_data['price'], item_data['quantity'], item_data['reorder_point']))
            flash('Item added successfully', 'success')
            return redirect(url_for('items'))
        except Exception as e:
            return handle_error(e)
    return render_template('add_item.html')

@app.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if request.method == 'POST':
        try:
            item_data = get_form_data()
            execute_db_query("UPDATE items SET name=%s, description=%s, price=%s, quantity=%s, reorder_point=%s WHERE id=%s", 
                             (item_data['name'], item_data['description'], item_data['price'], item_data['quantity'], item_data['reorder_point'], item_id))
            flash('Item updated successfully', 'success')
            return redirect(url_for('items'))
        except Exception as e:
            return handle_error(e)
    conn = psycopg2.connect(POSTGRES_CONNECTION_STRING)
    cur = conn.cursor()
    cur.execute("SELECT * FROM items WHERE id=%s", (item_id,))
    item = cur.fetchone()
    conn.close()
    return render_template('edit_item.html', item=item)

@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    try:
        execute_db_query("DELETE FROM items WHERE id=%s", (item_id,))
        flash('Item deleted successfully', 'success')
        return redirect(url_for('items'))
    except Exception as e:
        return handle_error(e)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            flash('File uploaded successfully', 'success')
            return redirect(url_for('items'))
        else:
            flash('Invalid file type', 'error')
            return redirect(request.url)
    return render_template('upload.html')


# Vendor routes
@app.route('/vendors')
def vendors():
    try:
        conn = get_db_connection()
        vendors = vendorsDB.get_all_vendors(conn)
        conn.close()
        return render_template('vendors.html', vendors=vendors)
    except psycopg2.Error as e:
        error_message = f"Database error: {e.pgerror}"
        return render_template('error.html', error_message=error_message), 500

@app.route('/add_vendor', methods=['POST'])
def add_vendor():
    try:
        vendor_data = {
            'name': request.form['name'],
            'address': request.form['address'],
            'phone': request.form['phone'],
            'email': request.form['email']
        }
        conn = get_db_connection()
        vendorsDB.add_vendor(conn, vendor_data)
        conn.close()
        return redirect(url_for('vendors'))
    except KeyError as e:
        return "Missing form data: " + str(e), 400
    except psycopg2.Error as e:
        error_message = f"Database error: {e.pgerror}"
        return render_template('error.html', error_message=error_message), 500

# Order routes
@app.route('/orders')
def orders():
    try:
        conn = get_db_connection()
        orders = orderDB.get_all_orders(conn)
        conn.close()
        return render_template('orders.html', orders=orders)
    except psycopg2.Error as e:
        error_message = f"Database error: {e.pgerror}"
        return render_template('error.html', error_message=error_message), 500

@app.route('/add_order', methods=['POST'])
def add_order():
    try:
        order_data = {
            'order_date': datetime.datetime.now(),
            'vendor_id': request.form['vendor_id'],
            'items': request.form.getlist('items')
        }
        conn = get_db_connection()
        orderDB.place_order(conn, order_data)
        conn.close()
        return redirect(url_for('orders'))
    except KeyError as e:
        return "Missing form data: " + str(e), 400
    except psycopg2.Error as e:
        error_message = f"Database error: {e.pgerror}"
        return render_template('error.html', error_message=error_message), 500

 #Delivery routes
@app.route('/deliveries')
def deliveries():
    try:
        conn = get_db_connection()
        deliveries = deliveryDB.get_all_deliveries(conn)
        conn.close()
        return render_template('deliveries.html', deliveries=deliveries)
    except psycopg2.Error as e:
        error_message = f"Database error: {e.pgerror}"
        return render_template('error.html', error_message=error_message), 500

@app.route('/add_delivery', methods=['POST'])
def add_delivery():
    try:
        delivery_data = {
            'delivery_date': datetime.datetime.now(),
            'order_id': request.form['order_id']
        }
        conn = get_db_connection()
        deliveryDB.record_delivery(conn, delivery_data)
        conn.close()
        return redirect(url_for('deliveries'))
    except KeyError as e:
        return "Missing form data: " + str(e), 400
    except psycopg2.Error as e:
        error_message = f"Database error: {e.pgerror}"
        return render_template('error.html', error_message=error_message), 500

# Invoice routes
@app.route('/invoices')
def invoices():
    try:
        conn = get_db_connection()
        invoices = invoiceDB.get_all_invoices(conn)
        conn.close()
        return render_template('invoices.html', invoices=invoices)
    except psycopg2.Error as e:
        error_message = f"Database error: {e.pgerror}"
        return render_template('error.html', error_message=error_message), 500

@app.route('/generate_invoice/<int:order_id>')
def generate_invoice(order_id):
    try:
        conn = get_db_connection()
        invoiceDB.generate_invoice(conn, order_id)
        conn.close()
        return redirect(url_for('invoices'))
    except psycopg2.Error as e:
        error_message = f"Database error: {e.pgerror}"
        return render_template('error.html', error_message=error_message), 500

# Run the Flask app
if __name__ == '__main__':
    create_database()
    app.run(debug=True)
