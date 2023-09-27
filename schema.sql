CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE categories(
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    name TEXT,
    category_id INTEGER REFERENCES categories(id)
);

CREATE TABLE chats (
    id SERIAL PRIMARY KEY,
    name TEXT,
    room_id INTEGER REFERENCES rooms(id)
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    message TEXT,
    time TIMESTAMP,
    chat_id INTEGER REFERENCES chats(id),
    user_id INTEGER REFERENCES users(id)
);
