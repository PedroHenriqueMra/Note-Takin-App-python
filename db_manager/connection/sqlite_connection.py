from utils.singleton import Singleton
from contextlib import contextmanager
from sqlite3 import Connection, connect


class SqliteDB:

    def __init__(self):
        self.connection_string:str = "tststst.db"

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
            conn.close()

    def get_connection(self) -> Connection:
        return connect(self.connection_string)


sqlite = SqliteDB()
