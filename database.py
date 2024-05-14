import sqlite3


def connect():
    return sqlite3.connect("database.db")

def save(conn:sqlite3.Connection):
    conn.commit()

def close(conn:sqlite3.Connection):
    save(conn)
    conn.close()



