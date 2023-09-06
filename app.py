from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign_in")
def page1():
    return "Kirjaudu sisään tai luo uusi tunnus"

@app.route("/create_account")
def page2():
    return "Luo uusi tunnus"

@app.route("/homepage")
def page3():
    return "Kategoriat"