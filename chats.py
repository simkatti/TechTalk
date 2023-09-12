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

    if chat_titles:
        for row in chat_titles:
            chat_id = row[0]
            chat_name = row[1]
            chat_content.append((chat_id, chat_name))
#viestien määrä
    return room_name, chat_content

def chat_data(chat_id):
    sql = text("SELECT name FROM chats WHERE id = :chat_id;")
    result = db.session.execute(sql, {"chat_id": chat_id})
    chat_name = result.scalar()

    sql_messages = text("SELECT message, time FROM messages WHERE chat_id = :chat_id;")
    result_messages = db.session.execute(sql_messages, {"chat_id": chat_id})
    all_messages = result_messages.fetchall()

    messages = []
    for row in all_messages:
        one_message = row[0]
        timestamp = row[1]
        # Format the timestamp as a string
        formatted_timestamp = datetime.strftime(timestamp, "%Y-%m-%d %H:%M:%S")
        messages.append((one_message, formatted_timestamp))

    return chat_name, messages


