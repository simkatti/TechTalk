from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign_in")
def page1():
    return render_template("login.html")

@app.route("/create_account", methods=["GET", "POST"])
def page2():
    passwords_match = True
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password1 = request.form["password1"]

        if not password or not password1:
            passwords_match = False
        elif password == password1:
            session["username"] = username
            hash_value = generate_password_hash(password)
            sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
            db.session.execute(sql, {"username":username, "password":hash_value})
            db.session.commit()
            return redirect("/home_page")
        else:
            passwords_match = False
        

    return render_template("createaccount.html", passwords_match=passwords_match)

@app.route("/home_page", methods=["GET", "POST"])
def page3():
    return render_template("homepage.html", name = session.get("username"))

@app.route("/hub_pages")
def page4():
    return "Here you will see all the chats in one hub and the chats and headline should change depending which hub you click!"

