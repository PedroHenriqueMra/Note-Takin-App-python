import sqlite3
from sqlite3 import Connection
from contextlib import contextmanager


class SqliteDB():

    def __init__(self):
        self.connection_string:str = "tststst.db"
        self.connection:Connection = None
        

    @contextmanager
    def db_connection(self, change=False):
        try:
            print("-> Connectiong SQLite database...")
            conn = self.get_connection()
            yield conn.cursor()
        finally:
            if change:
                print("Commiting changes in data base")
                conn.commit()
            print("-> Closing SQLite database...")

            self.close_connection()

    def get_connection(self) -> Connection:
        if self.connection == None:
            self.connection = sqlite3.connect(self.connection_string, autocommit=True)
        
        self.config_sqlite()
        return self.connection
    
    def close_connection(self) -> None:
        if self.connection != None:
            self.connection.close()
            self.connection = None

    def config_sqlite(self):
        if self.connection != None:
            self.connection.row_factory = sqlite3.Row


# single connection
sqlite = SqliteDB()
sqlite_conn = sqlite.get_connection()
