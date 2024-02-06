# Wir importieren zuerst das Flask-Objekt aus dem Package
from flask import Flask, request, render_template, url_for, redirect, session
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

"""
Festlegen einer Route für die Homepage. Der String in den Klammern
bildet das URL-Muster ab, unter dem der folgende Code ausgeführt
werden soll.
z.B.
* @app.route('/')    -> http://127.0.0.1:5000/
* @app.route('/abc') -> http://127.0.0.1:5000/abc
"""


@app.route("/")
def home() -> str:
    app.logger.info("Rendering home page")
    return render_template("home.html")


@app.route("/shop")
def shop() -> str:
    app.logger.info("Rendering About Flask page")
    return render_template("shop.html")


@app.route("/about-us")
def about_us() -> str:
    app.logger.info("Rendering About Flask page")
    return render_template("about-us.html")


@app.route("/faq")
def faq() -> str:
    app.logger.info("Rendering About Flask page")
    return render_template("faq.html")


@app.route("/warenkorb")
def warenkorb() -> str:
    app.logger.info("Rendering About Flask page")
    return render_template("warenkorb.html")


@app.route("/login")
def login() -> str:
    app.logger.info("Rendering About Flask page")
    return render_template("login.html")


@app.route("/register")
def new_user() -> str:
    app.logger.info("Rendering About Flask page")
    return render_template("new_user.html")


@app.route("/kasse")
def kasse() -> str:
    app.logger.info("Rendering About Flask page")
    return render_template("kasse.html")


@app.route("/impressum")
def impressum() -> str:
    app.logger.info("Rendering About Flask page")
    return render_template("impressum.html")


@app.route("/agb")
def agb() -> str:
    app.logger.info("Rendering About Flask page")
    return render_template("agb.html")


@app.route("/datenschutz")
def datenschutz() -> str:
    app.logger.info("Rendering About Flask page")
    return render_template("datenschutz.html")


@app.route("/login_do", methods=["POST", "GET"])
def login_do():
    # if form is submited
    if request.method == "POST":
        # record the user name
        session["name"] = request.form.get("name")
        session["pw"] = request.form.get("pw")
        # redirect to the main page
        return redirect("/")
    return render_template("login.html")


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
