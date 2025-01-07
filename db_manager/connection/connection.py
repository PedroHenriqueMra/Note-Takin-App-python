import sqlite3

from contextlib import contextmanager

class DBConnection:
    def __init__(self, connectionSTR):
        self.connection = connectionSTR
        self.conn:sqlite3.Connection = sqlite3.connect(self.connection)
        self.cur:sqlite3.Cursor = self.conn.cursor()
    
    @contextmanager
    def db_manager(self, change=False):
        try:
            print("Opening DB connection...")
            yield self.get_connection().cursor()
        finally:
            if change:
                print("Commit changes in data base")
                self.conn.commit()
            print("Close DB connection")
            self.conn.close()

    def get_connection(self) -> sqlite3.Connection:
        self.conn = sqlite3.connect(self.connection)
        self.cur = self.conn.cursor()
        return self.conn
    

db = DBConnection("tststst.db")
