from contextlib import contextmanager
import sqlite3

@contextmanager
def db_connection(change=False):
    try:
        print("Opening DB connection...")
        conn = get_connection()
        yield conn.cursor()
    finally:
        if change:
            print("Commit changes in data base")
            conn.commit()
        print("Close DB connection")
        conn.close()

def get_connection() -> sqlite3.Connection:
    return sqlite3.connect("tststst.db")
