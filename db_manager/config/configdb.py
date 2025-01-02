import sqlite3

class DBContext():
    def __init__(self):
        self.conn = sqlite3.connect("test.db")
        self.cur = self.conn.cursor()

    # if it doesn't exists = False
    def table_exists(self, table_name:str) -> bool:
        cur = self.cur
        res = cur.execute(f"SELECT name FROM sqlite_master WHERE name='{table_name}'")
        if res.fetchone() is None:
            return False
        return True
    

db = DBContext()
