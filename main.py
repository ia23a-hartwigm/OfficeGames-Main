# Wir importieren zuerst das Flask-Objekt aus dem Package
from operator import itemgetter

import psycopg2 as psycopg2
from flask import Flask, request, render_template, url_for, redirect, session, flash, jsonify
from flask_session import Session
import json

import services.math_service as math_service

# mock data
languages = [
    {"name": "Python", "creator": "Guido van Rossum", "year": 1991},
    {"name": "JavaScript", "creator": "Brendan Eich", "year": 1995},
    {"name": "Java", "creator": "James Gosling", "year": 1995},
    {"name": "C#", "creator": "Microsoft", "year": 2000},
    {"name": "Ruby", "creator": "Yukihiro Matsumoto", "year": 1995},
]

# Definieren einer Variable, die die aktuelle Datei zum Zentrum
# der Anwendung macht.
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
"""
Festlegen einer Route für die Homepage. Der String in den Klammern
bildet das URL-Muster ab, unter dem der folgende Code ausgeführt
werden soll.
z.B.
* @app.route('/')    -> http://127.0.0.1:5000/
* @app.route('/abc') -> http://127.0.0.1:5000/abc
"""

db_config = "postgres://admin:pF0jxrVmWapytgfJw2t7EzzYIAbFbgbz@dpg-cn14gin109ks73ccr1c0-a.frankfurt-postgres.render.com/officegames_db"


def connect_to_database():
    # Connection string for PostgreSQL
    connection_string = "postgres://admin:pF0jxrVmWapytgfJw2t7EzzYIAbFbgbz@dpg-cn14gin109ks73ccr1c0-a.frankfurt-postgres.render.com/officegames_db"
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(connection_string)
    return conn


def create_cursor(conn):
    return conn.cursor()


def get_coworker(cursor):
    # Define the keys that will be used to create the dictionaries
    keys = ["coworkerid", "first_name", "last_name", "coworker_role", "description", "favorite_product"]

    # Query to fetch data from the coworker table
    query = "SELECT coworkerid, first_name, last_name, coworker_role, description, favorite_product FROM coworker"
    cursor.execute(query)

    # Fetch all rows from the query result
    results = cursor.fetchall()

    # Check if there are any results
    if results:
        # Convert the list of tuples into a list of dictionaries
        list_of_dicts = [dict(zip(keys, row)) for row in results]
        return list_of_dicts
    else:
        return None


def get_products_by_id(cursor, id):
    # Define the keys that will be used to create the dictionaries
    keys = ["productid", "name_product", "rating", "price", "is_sale", "sale", "description"]

    # Query to fetch data from the coworker table
    query = "SELECT productid, name_product, rating, price, is_sale, sale, description FROM product WHERE productid = %s"
    cursor.execute(query, str(id))

    # Fetch all rows from the query result
    results = cursor.fetchall()

    # Check if there are any results
    if results:
        # Convert the list of tuples into a list of dictionaries
        list_of_products = [dict(zip(keys, row)) for row in results]
        return list_of_products
    else:
        return None


def get_products(cursor):
    # Define the keys that will be used to create the dictionaries
    keys = ["productid", "name_product", "rating", "price", "is_sale", "sale", "description"]

    # Query to fetch data from the coworker table
    query = "SELECT productid, name_product, rating, price, is_sale, sale, description FROM product"
    cursor.execute(query)

    # Fetch all rows from the query result
    results = cursor.fetchall()

    # Check if there are any results
    if results:
        # Convert the list of tuples into a list of dictionaries
        list_of_products = [dict(zip(keys, row)) for row in results]
        return list_of_products
    else:
        return None


@app.route("/")
def home():
    app.logger.info("Rendering home page")
    return render_template("home.html", warenkorb=render_warenkorb())


@app.route("/about")
def about():
    connection = connect_to_database()
    cursor = create_cursor(connection)
    coworkers_info = get_coworker(cursor)
    cursor.close()
    connection.close()
    return render_template("about.html", coworkers=coworkers_info, warenkorb=render_warenkorb())


@app.route("/shop")
def shop():
    # Your list of dictionaries
    warenkorb_items = [
        {'productid': 5, 'quant': 1},
        {'productid': 5, 'quant': 1},
        {'productid': 1, 'quant': 1},
        {'productid': 1, 'quant': 1},
        {'productid': 2, 'quant': 1}
    ]
    connection = connect_to_database()
    cursor = create_cursor(connection)
    product_info = get_products(cursor)
    cursor.close()
    connection.close()
    print(session.get("warenkorb"))
    return render_template("shop.html", product_info=product_info, warenkorb=render_warenkorb())


@app.route("/blogs")
def blogs():
    app.logger.info("Rendering blog page")
    return render_template("blogs.html", warenkorb=render_warenkorb())


@app.route("/login")
def login() -> str:
    app.logger.info("Rendering shop page")
    return render_template("login.html", warenkorb=render_warenkorb())


@app.route("/warenkorb")
def warenkorb():
    app.logger.info("Rendering warenkorb page")
    return render_template("warenkorb.html", warenkorb=render_warenkorb())


@app.route("/contact")
def contact():
    app.logger.info("Rendering contact page")
    return render_template("contact.html", warenkorb=render_warenkorb())


@app.route("/agb")
def agb():
    app.logger.info("Rendering home page")
    return render_template("agb.html", warenkorb=render_warenkorb())


@app.route("/infos/<id>", methods=["GET"])
def infos(id):
    id = int(id)
    connection = connect_to_database()
    cursor = create_cursor(connection)
    product_info = get_products_by_id(cursor, id)
    cursor.close()
    connection.close()
    return render_template("infos.html", warenkorb=render_warenkorb(), infos=product_info)


@app.route("/review")
def review():
    app.logger.info("Rendering home page")
    return render_template("review.html", warenkorb=render_warenkorb())


@app.route("/q")
def read_session():
    # check if the users exist or not
    if not session.get("user"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    return jsonify(session.get("user"))


def kasse_fillin(cursor):
    # Define the keys that will be used to create the dictionaries
    keys = ["first_name", "last_name", "company_name", "country", "street", "plz", "city", "tel", "email"]

    # Query to fetch data from the coworker table
    query = (
        "SELECT (first_name, last_name, company_name, country, street, plz, city, tel, email) FROM customers WHERE customerid = %s")
    cursor.execute(query, session.get("user"))

    # Fetch all rows from the query result
    results = cursor.fetchall()

    # Check if there are any results
    if results:
        # Convert the list of tuples into a list of dictionaries
        list_of_products = [dict(zip(keys, row)) for row in results]
        return list_of_products
    else:
        return None


@app.route("/kasse")
def kasse():
    return render_template("kasse.html", warenkorb=render_warenkorb())
    '''    connection = connect_to_database()
    cursor = create_cursor(connection)
    
    product_info = kasse_fillin(cursor)
    
    cursor.close()
    connection.close()
    , product_info=product_info'''


@app.route("/new_user", methods=["POST"])
def new_user():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        company = request.form["company"]
        street = request.form["street"]
        plz = request.form["plz"]
        city = request.form["city"]
        country = request.form["country"]
        email = request.form["email"]
        tel = request.form["tel"]
        pw = request.form["password"]
        pw2 = request.form["password2"]
        agree = request.form["tos"]

        if agree == True:
            if pw == pw2:
                conn = connect_to_database()
                cursor = conn.cursor()
                max_id = get_max_id_customer()
                query = "INSERT INTO customers (customersid, first_name, last_name, company_name, country, street, plz, city, tel, email, password) VALUES %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
                cursor.execute(query, (max_id, first_name, last_name, company, country, street, plz, city, tel, email, pw))
                conn.commit()
            else:
                return "pw nicht übeinstimmend"

        else:
            return "need to accept the agreement"   

@app.route('/warenkorb/add/<id>', methods=['GET'])
def productpage(id):
    if session.get("user"):
        cursor = None
        conn = None
        try:
            # Since `id` is already an argument, you don't need to fetch it from request.args
            productId = int(id)
            customerId = session.get("user")
            quant = 1

            conn = connect_to_database()
            cursor = conn.cursor()
            max_id = get_max_id_warenkorb()
            query = "INSERT INTO warenkorb (warenkorbid, productid, customerid, quant) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (max_id, productId, customerId, quant))
            conn.commit()

            if is_in_warenkorb:
                # add one to that id
                return warenkorb_quant_plus_one(productId)


            else:
                conn = connect_to_database()
                cursor = conn.cursor()
                max_id = get_max_id_warenkorb()
                query = "INSERT INTO warenkorb (warenkorbid, productid, customerid, quant) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (max_id, productId, customerId, quant))
                conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            # Provide more informative error handling here if necessary
            return "Error processing your request", 500
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return redirect(url_for("shop"))
    else:
        if 'warenkorb' not in session:
            session['warenkorb'] = []

        try:
            productId = int(id)
            quant = 1  # Assuming you always add one quantity for simplicity

            # Initialize 'warenkorb' in session if it doesn't exist
            warenkorb = session.get("warenkorb")
            # Assume warenkorb is a list of dictionaries with key 'productid'
            product_ids = [item['productid'] for item in warenkorb]  # Corrected line
            for id in product_ids:
                if id == productId:
                    return warenkorb_quant_plus_one(productId)
                else:
                    break
            # Create a new product item
            new_product = {'productid': productId, 'quant': quant}

            # Retrieve the current 'warenkorb', add the new item, then reassign it back to the session
            current_warenkorb = session.get('warenkorb')
            current_warenkorb.append(new_product)
            session['warenkorb'] = current_warenkorb  # Reassign to ensure Flask detects the change

            # Mark the session as modified (should be redundant but can help in certain Flask versions or setups)
            session.modified = True

        except Exception as e:
            print(f"An error occurred: {e}")
            return "Error processing your request", 500

        return redirect(url_for("shop"))
    return redirect(url_for("shop"))


def get_max_id_warenkorb():
    conn = connect_to_database()
    cursor = conn.cursor()

    query = ("SELECT warenkorbid FROM warenkorb WHERE warenkorbid = (SELECT MAX(warenkorbid) FROM warenkorb)")
    cursor.execute(query)
    max_id = cursor.fetchall()
    max_id = max_id[0]
    max_id = max_id[0]
    max_id += 1
    conn.close()
    cursor.close()
    return max_id


def get_max_id_customer():
    conn = connect_to_database()
    cursor = conn.cursor()

    query = ("SELECT customerid FROM customers WHERE customerid = (SELECT MAX(customerid) FROM customers)")
    cursor.execute(query)
    max_id = cursor.fetchall()
    max_id = max_id[0]
    max_id = max_id[0]
    max_id += 1
    conn.close()
    cursor.close()
    return max_id


@app.route("/login_do", methods=["POST"])
def login_do():
    if request.method == "POST":
        username = request.form["name"]
        password = request.form["password"]

        # Connect to your PostgreSQL database
        conn = psycopg2.connect(db_config)
        cur = conn.cursor()

    # Query to check if the user exists with the provided username and password
    cur.execute("SELECT customersid FROM customers WHERE email = %s AND password = %s", (username, password))
    user = cur.fetchone()

    if user:
        # Credentials matched, set user session
        session["user"] = user[0]  # Assuming 'id' is the first column
        cur.close()
        conn.close()
        return "It Works"  # Redirect to home or another secure page
    else:
        # Close connection
        cur.close()
        conn.close()
        return "wrong"


def render_warenkorb():
    if 'warenkorb' in session:
        all_products = []

        if session.get("user"):
            # For logged-in users, fetch product details and quantities from the database
            connection = connect_to_database()
            cursor = create_cursor(connection)

            # Query to fetch product IDs and quantities from the warenkorb table for the current user
            query = "SELECT productid, quant FROM warenkorb WHERE customerid = %s"
            cursor.execute(query, (session.get("user"),))

            # Fetch all rows from the query result
            warenkorb_items = cursor.fetchall()

            for item in warenkorb_items:
                productid, quantity = item
                product_info = get_product_info_warenkorb(productid, quantity)
                all_products.extend(product_info)

            cursor.close()
            connection.close()

        else:
            # For guest users, use the quantities from the session's warenkorb
            warenkorb = session.get("warenkorb")

            for item in warenkorb:
                productid = item['productid']
                quantity = item.get('quant', 1)  # Default to 1 if not found
                product_info = get_product_info_warenkorb(productid, quantity)
                all_products.extend(product_info)

        if all_products:
            return all_products
        else:
            return None
    else:
        # If there's no warenkorb in the session, return None or an empty list
        return None


def get_product_info_warenkorb(productid, quant):  # Default quantity is set to 1
    connection = connect_to_database()
    cursor = create_cursor(connection)

    keys = ["productid", "name_product", "price", "is_sale", "sale", "quant"]  # Added "quantity" key

    # Query to fetch data from the product table
    query = "SELECT productid, name_product, price, is_sale, sale FROM product WHERE productid = %s"
    cursor.execute(query, (str(productid),))

    # Fetch all rows from the query result
    results = cursor.fetchall()

    # Check if there are any results
    if results:
        # Convert the list of tuples into a list of dictionaries
        list_of_dicts = [dict(zip(keys, row + (quant,))) for row in results]  # Added quantity to the tuple
        return list_of_dicts
    else:
        return None


@app.route("/warenkorb/del/<id>", methods=['GET'])
def warenkorb_del(id):
    productId = int(id)
    if session.get("user"):
        connection = connect_to_database()
        cursor = create_cursor(connection)

        # Query to fetch data from the warenkorb table
        query = "DELETE FROM warenkorb WHERE customerid = %s AND productid = %s"
        cursor.execute(query, (session.get("user"), productId))

        cursor.close()
        connection.close()
        return redirect("/shop")
    else:
        warenkorb = session.get("warenkorb")
        for i in range(len(warenkorb) - 1, -1, -1):  # Iterate in reverse to safely remove items
            if warenkorb[i]['productid'] == productId:
                warenkorb.pop(i)
        session.pop("warenkorb")
        session["warenkorb"] = warenkorb
        return redirect("/shop")


@app.route("/warenkorb/edit/quant/plus1/<id>", methods=['GET'])
def warenkorb_quant_plus_one(id):
    productId = int(id)
    if session.get("user"):
        connection = connect_to_database()
        cursor = create_cursor(connection)

        # Query to fetch data from the warenkorb table
        query = "UPDATE warenkorb SET quant = quant + 1 WHERE customerid = %s AND productid = %s"
        cursor.execute(query, (session.get("user"), productId))

        cursor.close()
        connection.close()
        return redirect("/shop")
    else:
        increment_product_quantity_in_session(id)
        return redirect("/shop")


def increment_product_quantity_in_session(productId):
    # Ensure 'warenkorb' exists in session
    if 'warenkorb' not in session:
        session['warenkorb'] = []

    warenkorb = session['warenkorb']
    product_found = False

    # Increment quantity if product exists
    for item in warenkorb:
        if item['productid'] == productId:
            item['quant'] += 1
            product_found = True
            break

    # Optionally, add the product with quant=1 if not found
    if not product_found:
        warenkorb.append({'productid': productId, 'quant': 1})

    session['warenkorb'] = warenkorb
    session.modified = True


@app.route("/warenkorb/edit/quant/<id>/<value>", methods=['GET'])
def warenkorb_quant_edit(id, value):
    productId = int(id)
    value = int(value)
    if session.get("user"):
        connection = connect_to_database()
        cursor = create_cursor(connection)

        # Query to fetch data from the warenkorb table
        query = "UPDATE warenkorb SET quant = %s WHERE customerid = %s AND productid = %s"
        cursor.execute(query, (value, session.get("user"), productId))

        cursor.close()
        connection.close()
        return redirect("/shop")
    else:
        print("----------------------------------")
        print(session.get("warenkorb"))
        print("----------------------------------")
        set_product_quantity_in_session(id, value)
        print("..................................")
        print(session.get("warenkorb"))
        print("..................................")
        return redirect("/shop")


def set_product_quantity_in_session(productId, new_quantity):
    # Ensure 'warenkorb' exists in session
    if 'warenkorb' not in session:
        session['warenkorb'] = []

    warenkorb = session['warenkorb']
    product_found = False

    # Increment quantity if product exists
    for item in warenkorb:
        if item['productid'] == productId:
            item['quant'] = new_quantity
            product_found = True
            break

    session['warenkorb'] = warenkorb
    session.modified = True


@app.route("/logout")
def logout():
    if session.get("user"):
        session.pop("user")
    return redirect("/")


'''
# Route to handle form submission
@app.route("/submit", methods=["POST"])
def submit():
    app.logger.info("Form submitted")
    # Access form data (request body parameters)
    name = request.form.get("name")
    # Redirect to a new URL, passing a parameter in the URL
    return redirect(url_for("result", name=name))


# Route with a parameter in the URL
@app.route("/result/<name>")
def result(name) -> str:
    app.logger.info(f"Showing result for {name}")
    return render_template("result.html", name=name)


@app.route("/get_languages")
def get_languages() -> str:
    return render_template("languages.html", languages=languages)


###########################
# BEISPIELE
###########################
@app.route('/helloWorld')
def hello_world() -> str:
    # Die Anzeigefunktion 'hello_world' gibt den String "Hello, World" als Antwort zurück
    return 'Hello, World!'

'''

if __name__ == '__main__':
    app.run()
