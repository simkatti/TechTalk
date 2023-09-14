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
    add_room_ok=True #need to do
    if "username" not in session:
        return redirect("/")
    titles = chats.homepage_data()
    if request.method == "POST":
        category = request.form["category"]
        name = request.form["room_title"]
        if chats.add_room(category, name):
            return redirect("/home_page")
        else:
            add_room_ok=False
    return render_template("homepage.html", name = session.get("username"), titles=titles, add_room_ok=add_room_ok)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/rooms/<int:room_id>", methods=["GET", "POST"])
def room(room_id):
    add_chat_ok = True
    room_name, chat_conent, count = chats.roompage_data(room_id)
    if request.method =="POST":
        name = request.form["chat_title"]
        message = request.form["message"]
        chat_id = chats.add_chat(name, message, room_id)
        if chat_id:
            return redirect(f"/chat/{chat_id}")
        else:
            add_chat_ok=False

    return render_template("rooms.html", name=session.get("username"), room_name=room_name, chat_content=chat_conent, count=count, add_chat_ok=add_chat_ok, room_id=room_id)


@app.route("/chat/<int:chat_id>", methods=["GET", "POST"])
def chat(chat_id):
    chat_sent_ok=True #need to do
    chat_name, messages = chats.chat_data(chat_id)
    if request.method == "POST":
        message = request.form["new_message"]
        if chats.send(message, chat_id):
            return redirect(f"/chat/{chat_id}")
        else:
            chat_sent_ok = False
    return render_template("chat.html", name=session.get("username"), chat_name=chat_name, messages=messages, chat_id=chat_id, chat_sent_ok=chat_sent_ok)

@app.errorhandler(404)
def page_not_found(e):
    return "Page not found: " + str(e), 404
