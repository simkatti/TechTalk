from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign_in")
def page1():
    return render_template("login.html")

@app.route("/create_account")
def page2():
    return render_template("createaccount.html")

@app.route("/homepage")
def page3():
    return "Kategoriat"