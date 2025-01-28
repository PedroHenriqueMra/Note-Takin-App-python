import sqlite3
from sqlite3 import Connection, connect
from contextlib import contextmanager


class SqliteDB():

    def __init__(self):
        self.connection_string:str = ":memory:"
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
        if self.connection is None:
            self.connection = connect(self.connection_string)
            # get fetchone in row format
            self.connection.row_factory = sqlite3.Row
        
        return self.connection
    
    def close_connection(self) -> None:
        if self.connection is not None:
            self.connection.close()


# single connection
sqlite = SqliteDB()
sqlite_conn = sqlite.get_connection()
