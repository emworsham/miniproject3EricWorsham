# db.py

import sqlite3

DATABASE_NAME = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with open('schema.sql') as f:
        create_schema = f.read()

    conn = get_db_connection()
    with conn:
        conn.executescript(create_schema)

def create_user(username, password):
    conn = get_db_connection()
    with conn:
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))

def get_user(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

def log_weight(user_id, weight):
    conn = get_db_connection()
    with conn:
        conn.execute('INSERT INTO weight_entries (user_id, weight) VALUES (?, ?)', (user_id, weight))

def get_weight_entries(user_id):
    conn = get_db_connection()
    entries = conn.execute('SELECT * FROM weight_entries WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    return entries
