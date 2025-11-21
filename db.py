import sqlite3

schema = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL, 
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    bio TEXT
);
"""

def init_db(database_path: str):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    
def get_db_connection(database_path: str):
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    return conn