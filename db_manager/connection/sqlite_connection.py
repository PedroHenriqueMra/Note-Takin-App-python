from contextlib import contextmanager
import sqlite3

@contextmanager
def db_connection(change=False):
    try:
        print("-> Connectiong SQLite database...")
        conn = get_connection()
        yield conn.cursor()
    finally:
        if change:
            print("Commiting changes in data base")
            conn.commit()
        print("-> Closing SQLite database...")
        conn.close()

def get_connection() -> sqlite3.Connection:
    return sqlite3.connect("tststst.db")
