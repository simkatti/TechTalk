from flask import redirect, render_template, request, session
from app import app
import users
import fetch


@app.route("/")
def index():
    return render_template("landingpage.html")

@app.route("/login", methods=["GET", "POST"])
def signin():
    account_check = True
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            account_check = False
        else:
            return redirect("/home")   
    return render_template("loginpage.html", account_check=account_check)    


@app.route("/signup", methods=["GET", "POST"])
def createaccount():
    passwords_match = True
    username_ok = True
    username_exists = True
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 2 or len(username) > 20:
            username_ok = False

        password = request.form["password"]
        password1 = request.form["password1"]

        if not password or not password1:
            passwords_match = False
        elif password != password1:
            passwords_match = False
        elif passwords_match and username_ok: 
            if users.register(username, password):
                return redirect("/home")
            else:
                username_exists=False
    return render_template("signuppage.html", passwords_match=passwords_match, username_ok=username_ok, username_exists=username_exists)

@app.route("/home", methods=["GET", "POST"])
def home():
    add_room_ok=True 
    if "username" not in session:
        return redirect("/")
    titles = fetch.homepage_data()
    if request.method == "POST":
        category = request.form["category"]
        name = request.form["room_title"]
        if 2 < len(name) < 50 and category != "":
            if fetch.add_room(category, name):
                return redirect("/home")
        else:
            add_room_ok=False
    return render_template("homepage.html", name = session.get("username"), titles=titles, add_room_ok=add_room_ok)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/room/<int:room_id>", methods=["GET", "POST"])
def room(room_id):
    add_chat_ok = True
    room_name, chat_conent = fetch.roompage_data(room_id)
    if request.method =="POST":
        name = request.form["chat_title"]
        message = request.form["message"]
        user_id = session.get("id")
        if 2 < len(name) < 100 and 5 < len(message) < 1000:
            chat_id = fetch.add_chat(name, message, user_id, room_id)
            if chat_id:
                return redirect(f"/chat/{chat_id}")
        else:
            add_chat_ok=False

    return render_template("roomspage.html", name=session.get("username"), room_name=room_name, chat_content=chat_conent, add_chat_ok=add_chat_ok, room_id=room_id)


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
                    return redirect("/home")
                return redirect(f"/chat/{chat_id}")
            else:
                chat_delete = False

        else:
            message = request.form["new_message"]
            if 1 < len(message) < 1000:
                user_id = session.get("id")
                if fetch.send(message, chat_id, user_id):
                    return redirect(f"/chat/{chat_id}")
            else:
                chat_sent_ok = False
    return render_template("chatpage.html", name=session.get("username"), chat_name=chat_name, messages=messages, chat_id=chat_id, chat_sent_ok=chat_sent_ok, chat_delete=chat_delete)

@app.route("/searchresults", methods=["GET", "POST"])
def searchbar():
    results_found = True
    query = request.args["query"]
    content = fetch.search(query)
    if not content:
        results_found = False

    return render_template("searchpage.html", name=session.get("username"), content=content, results_found=results_found)
