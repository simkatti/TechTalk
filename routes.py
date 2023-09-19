from flask import redirect, render_template, request, session
from app import app
import users
import fetch


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def signin():
    account_check = True
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            account_check = False
        else:
            return redirect("/homepage")   
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
            return redirect("/homepage")
    return render_template("createaccount.html", passwords_match=passwords_match, username_ok=username_ok)

@app.route("/homepage", methods=["GET", "POST"])
def home():
    add_room_ok=True #need to fix
    if "username" not in session:
        return redirect("/")
    titles = fetch.homepage_data()
    if request.method == "POST":
        category = request.form["category"]
        name = request.form["room_title"]
        if len(name) >2 and category != "":
            if fetch.add_room(category, name):
                return redirect("/homepage")
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
    room_name, chat_conent = fetch.roompage_data(room_id)
    if request.method =="POST":
        name = request.form["chat_title"]
        message = request.form["message"]
        user_id = session.get("id")
        if len(name)>2 and len(message)>5:
            chat_id = fetch.add_chat(name, message, user_id, room_id)
            if chat_id:
                return redirect(f"/chat/{chat_id}")
        else:
            add_chat_ok=False

    return render_template("rooms.html", name=session.get("username"), room_name=room_name, chat_content=chat_conent, add_chat_ok=add_chat_ok, room_id=room_id)


@app.route("/chat/<int:chat_id>", methods=["GET", "POST"])
def chat(chat_id):
    chat_sent_ok=True 
    chat_delete = True
    chat_name, messages= fetch.chat_data(chat_id)
    if request.method == "POST":
        if "message_id" in request.form:
            message_id = int(request.form["message_id"])
            if fetch.delete(message_id):
                count = fetch.check_messagecount(chat_id)
                if count:
                    return redirect("/homepage")
                else:
                    return redirect(f"/chat/{chat_id}")
            else:
                chat_delete = False

        else:
            message = request.form["new_message"]
            if len(message) > 1:
                user_id = session.get("id")
                if fetch.send(message, chat_id, user_id):
                    return redirect(f"/chat/{chat_id}")
            else:
                chat_sent_ok = False
    return render_template("chat.html", name=session.get("username"), chat_name=chat_name, messages=messages, chat_id=chat_id, chat_sent_ok=chat_sent_ok, chat_delete=chat_delete)

# delete chats???