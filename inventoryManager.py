from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import itemsDB
import vendorsDB
import orderDB
import deliveryDB
import invoiceDB
import datetime
from flaskConfig import POSTGRES_CONNECTION_STRING, SECRET_KEY, DEBUG


app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG

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

# Item routes
@app.route('/items')
def items():
    try:
        conn = get_db_connection()
        items = itemsDB.get_all_items(conn)
        conn.close()
        return render_template('items.html', items=items)
    except psycopg2.Error as e:
        error_message = f"Database error: {e.pgerror}"
        return render_template('error.html', error_message=error_message), 500

@app.route('/add_item', methods=['POST'])
def add_item():
    try:
        item_data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'price': float(request.form['price']),
            'quantity': int(request.form['quantity']),
            'reorder_point': int(request.form['reorder_point'])
        }
        conn = get_db_connection()
        itemsDB.add_item(conn, item_data)
        conn.close()
        return redirect(url_for('items'))
    except KeyError as e:
        return "Missing form data: " + str(e), 400
    except ValueError as e:
        return "Invalid form data: " + str(e), 400
    except psycopg2.Error as e:
        error_message = f"Database error: {e.pgerror}"
        return render_template('error.html', error_message=error_message), 500

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
