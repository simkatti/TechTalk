from flask import Flask
from flask import render_template, request

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

@app.route("/home_page", methods=["POST"])
def page3():
    return render_template("homepage.html", name=request.form["username"])

@app.route("/hub_pages")
def page4():
    return "Here you will see all the chats in one hub and the chats and headline should change depending which hub you click!"

