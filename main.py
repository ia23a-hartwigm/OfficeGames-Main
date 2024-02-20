# Wir importieren zuerst das Flask-Objekt aus dem Package
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


users = [
    {"id": 1, "username": "user1", "password": "password1"},
    {"id": 2, "username": "user2", "password": "password2"}
]


@app.route("/")
def home():
    session["user"] = 1  # Only for testing
    app.logger.info("Rendering home page")
    render_warenkorb()

    return render_template("home.html")


@app.route("/about")
def about():
    connection = connect_to_database()
    cursor = create_cursor(connection)
    coworkers_info = get_coworker(cursor)
    cursor.close()
    connection.close()
    return render_template("about.html", coworkers=coworkers_info)


@app.route("/shop")
def shop():
    connection = connect_to_database()
    cursor = create_cursor(connection)
    product_info = get_products(cursor)
    cursor.close()
    connection.close()
    return render_template("shop.html", product_info=product_info)


@app.route("/blogs")
def blogs():
    app.logger.info("Rendering blog page")
    return render_template("blogs.html")


@app.route("/login")
def login() -> str:
    app.logger.info("Rendering shop page")
    return render_template("login.html")


@app.route("/warenkorb")
def warenkorb():
    app.logger.info("Rendering warenkorb page")
    return render_template("warenkorb.html")


@app.route("/contact")
def contact():
    app.logger.info("Rendering contact page")
    return render_template("contact.html")


@app.route("/agb")
def agb():
    app.logger.info("Rendering home page")
    return render_template("agb.html")


@app.route("/infos")
def infos():
    app.logger.info("Rendering home page")
    return render_template("infos.html")


@app.route("/review")
def review():
    app.logger.info("Rendering home page")
    return render_template("review.html")


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
    return render_template("kasse.html")
    '''    connection = connect_to_database()
    cursor = create_cursor(connection)
    
    product_info = kasse_fillin(cursor)
    
    cursor.close()
    connection.close()
    , product_info=product_info'''


@app.route("/new_user", methods=["POST"])
def new_user():
    if request.method == "POST":
        username = request.form["name"]
        password = request.form["password"]

        # Connect to your PostgreSQL database
        conn = psycopg2.connect(db_config)
        cur = conn.cursor()

    # Query to check if the user exists with the provided username and password
    cur.execute("SELECT customersid FROM customers WHERE email = %s AND password = %s", (username, password))
    user = cur.fetchone()
    print(user)


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
    if session.get("user"):
        connection = connect_to_database()
        cursor = create_cursor(connection)

        keys = ["warenkorbId", "productId", "customerId", "quant"]

        # Query to fetch data from the coworker table
        query = "SELECT warenkorbId, productId, customerId, quant FROM warenkorb WHERE customerId = %s"
        cursor.execute(query, (session.get("user"),))

        # Fetch all rows from the query result
        results = cursor.fetchall()


        # Check if there are any results
        if results:
            # Convert the list of tuples into a list of dictionaries
            list_of_dicts = [dict(zip(keys, row)) for row in results]
            print(list_of_dicts)
            return list_of_dicts
        else:
            return None


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

# test
