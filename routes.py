from flask import redirect, render_template, request, session
from app import app
from db import db
import users
import chats


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign_in", methods=["GET", "POST"])
def signin():
    account_check = True
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            account_check = False
        else:
            return redirect("/home_page")   
    return render_template("login.html", account_check=account_check)    


@app.route("/create_account", methods=["GET", "POST"])
def createaccount():
    passwords_match = True
    username_ok = True
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            username_ok = False

        password = request.form["password"]
        password1 = request.form["password1"]

        if not password or not password1:
            passwords_match = False
        elif password != password1:
            passwords_match = False
        elif passwords_match and username_ok and users.register(username, password):
            return redirect("/home_page")
    return render_template("createaccount.html", passwords_match=passwords_match, username_ok=username_ok)

@app.route("/home_page", methods=["GET", "POST"])
def home():
    if "username" not in session:
        return redirect("/")
    titles = chats.homepage_data()
    return render_template("homepage.html", name = session.get("username"), titles=titles)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/rooms/<int:room_id>")
def room(room_id):
    room_name, chat_conent = chats.roompage_data(room_id)
    return render_template("rooms.html", name=session.get("username"), room_name=room_name, chat_content=chat_conent)


@app.route("/chat/<int:chat_id>")
def chat(chat_id):
    chat_name, messages = chats.chat_data(chat_id)
    return render_template("chat.html", name=session.get("username"), chat_name=chat_name, messages=messages )




