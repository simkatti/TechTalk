from db import db
from sqlalchemy.sql import text
from datetime import datetime

def homepage_data():
    sql = text("SELECT r.id AS room_id, r.name AS room_name, c.name AS category_name FROM rooms AS r JOIN categories AS c ON r.category_id = c.id ORDER BY c.name, r.name;")
    result = db.session.execute(sql)
    data = result.fetchall()

    titles = {}
    for title in data:
        category_name = title.category_name
        room_id = title.room_id
        room_name = title.room_name
        if category_name not in titles:
            titles[category_name] = []
        titles[category_name].append((room_id, room_name))

    return titles

def roompage_data(room_id):
    sql = text("SELECT name FROM rooms WHERE id = :room_id;")
    result = db.session.execute(sql, {"room_id": room_id})
    room_name = result.scalar()

    sql_chats = text("SELECT id, name FROM chats WHERE room_id = :room_id;")
    result_chats = db.session.execute(sql_chats, {"room_id": room_id})
    chat_titles = result_chats.fetchall()
    chat_content = []
    count = 0

    if chat_titles:
        for row in chat_titles:
            chat_id = row[0]
            chat_name = row[1]
            sql_count = text("SELECT count(chat_id) FROM messages WHERE chat_id=:chat_id")
            result = db.session.execute(sql_count, {"chat_id": chat_id})
            count = result.fetchone()
            chat_content.append((chat_id, chat_name, count))

    return room_name, chat_content

def chat_data(chat_id):
    sql = text("SELECT name FROM chats WHERE id = :chat_id;")
    result = db.session.execute(sql, {"chat_id": chat_id})
    chat_name = result.scalar()

    sql_messages = text("SELECT id, message, time, user_id FROM messages WHERE chat_id = :chat_id;")
    result_messages = db.session.execute(sql_messages, {"chat_id": chat_id})
    all_messages = result_messages.fetchall()

    messages = []
    for row in all_messages:
        message_id = row[0]
        one_message = row[1]
        timestamp = row[2]
        user_id = row[3]
        time = datetime.strftime(timestamp, "%Y-%m-%d %H:%M:%S")
        messages.append((message_id, one_message, time, user_id))

    return chat_name, messages

def send(message, chat_id, user_id):
    sql=text("INSERT INTO messages (message, time, chat_id, user_id) VALUES (:message, NOW(), :chat_id, :user_id);")
    db.session.execute(sql, {"message": message, "chat_id": chat_id, "user_id": user_id})
    db.session.commit()
    return True

def add_room(category, name):
    category_sql= text("SELECT id FROM categories WHERE name=:category;")
    result = db.session.execute(category_sql, {"category": category})
    category_id = result.fetchone()
    if category_id:
        sql = text("INSERT INTO rooms (name, category_id) VALUES (:name, :category_id);")
        db.session.execute(sql, {"name": name, "category_id": category_id[0]})
        db.session.commit()
        return True
    else:
        return False
    
def add_chat(name, message, user_id, room_id):
    sql_chats = text("INSERT INTO chats (name, room_id) VALUES (:name, :room_id) RETURNING id;")
    sql_result = db.session.execute(sql_chats, {"name": name, "room_id": room_id})
    chat_row = sql_result.fetchone()

    sql_result.close()

    if chat_row is not None:
        chat_id = chat_row[0]
        print(chat_id)
        sql = text("INSERT INTO messages (message, time, chat_id, user_id) VALUES (:message, NOW(), :chat_id, :user_id);")
        db.session.execute(sql, {"message": message, "chat_id": chat_id, "user_id": user_id})
        db.session.commit()
        return chat_id
    else:
        return False
    
def delete(message_id):
    sql = text("DELETE FROM messages WHERE id=:id;")
    db.session.execute(sql, {"id": message_id})
    db.session.commit()
    return True

def check_messagecount(chat_id):
    sql = text("SELECT count(chat_id) FROM messages WHERE chat_id=:chat_id;")
    result = db.session.execute(sql, {"chat_id": chat_id})
    count = result.fetchone()
    if count and count[0]==0:
        delete_room = text("DELETE FROM chats WHERE id=:chat_id;")
        db.session.execute(delete_room, {"chat_id": chat_id})
        db.session.commit()
        return True
    else:
        return False
    
def search(query):
    searchresult = []
    if query != "":
        sql = text("SELECT DISTINCT chat_id FROM messages WHERE message LIKE :query;")
        search = db.session.execute(sql, {"query": "%" + query + "%"})
        chat_ids = [chat_id[0] for chat_id in search]

        if chat_ids:
            chat = text("SELECT id, name FROM chats WHERE id IN :chat_ids;")
            chat_info = db.session.execute(chat, {"chat_ids": tuple(chat_ids)})
            chat_data = chat_info.fetchall()

            for c_id, c_name in chat_data:
                message_count = text("SELECT count(chat_id) FROM messages WHERE chat_id=:chat_id;")
                chat_count = db.session.execute(message_count, {"chat_id": c_id})
                count = chat_count.fetchone()
                searchresult.append((c_id, c_name, count[0]))

    return searchresult