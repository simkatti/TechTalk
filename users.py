from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text


def login(username, password):   
    sql = text("SELECT id, password FROM users WHERE username=:username;")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["username"] = username
            session["id"] = user.id
            return True
        else:
            return False


def register(username, password):
    check_sql = text("SELECT 1 FROM users WHERE username=:username;")
    result = db.session.execute(check_sql, {"username": username})
    username_check = result.fetchone()
    if username_check:
        return False
    session["username"] = username
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password);")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return True
    except:
        return False
