import sqlite3

open("data/sessions.db","a+").close()

db = sqlite3.connect("data/sessions.db")

db.execute("""CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""")

db.commit()
db.close()