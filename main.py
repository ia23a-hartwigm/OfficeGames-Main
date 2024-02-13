# Wir importieren zuerst das Flask-Objekt aus dem Package
from flask import Flask, request, render_template, url_for, redirect, session, flash, jsonify
from flask_session import Session

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

users = [
    {"id": 1, "username": "user1", "password": "password1"},
    {"id": 2, "username": "user2", "password": "password2"}
]




@app.route("/")
def home():
    app.logger.info("Rendering home page")
    return render_template("home.html")


@app.route("/shop")
def shop():
    app.logger.info("Rendering shop page")
    return render_template("shop.html")

@app.route("/about")
def about():
    app.logger.info("Rendering shop page")
    return render_template("about-us.html")

@app.route("/faq")
def faq():
    app.logger.info("Rendering faq page")
    return render_template("faq.html")


@app.route("/login")
def login() -> str:
    app.logger.info("Rendering shop page")
    return render_template("login.html")

@app.route("/warenkorb")
def warenkorb():
    app.logger.info("Rendering warenkorb page")
    return render_template("warenkorb.html")

@app.route("/agb")
def agb():
    app.logger.info("Rendering home page")
    return render_template("agb.html")

@app.route("/datenschutz")
def datenschutz():
    app.logger.info("Rendering home page")
    return render_template("datenschutz.html")


@app.route("/q")
def read_session():
    # check if the users exist or not
    if not session.get("user"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    return jsonify(session.get("user"))



@app.route("/login_do", methods=["POST"])
def login_do():
    if request.method == "POST":
        username = request.form["name"]
        password = request.form["password"]

        # Simple check against hardcoded credentials
        for user in users:
            if username == user.get('username') and password == user.get('password'):
                # Credentials matched, set user session
                session["user"] = user.get('id')
                return "It Works"  # Redirect to home or another secure page
        return "wrong"


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
