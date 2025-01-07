from db_manager.repository.irepository import IRepository
from datetime import datetime
from typing import Optional

from db_manager.repository.dataclasses.system_data import Text
from db_manager.connection.connection import db

class ADMText(IRepository[Text]):
    def __init__(self):
        # create table
        with db.db_manager(change=True) as cur:
            table = """CREATE TABLE IF NOT EXISTS text (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type VARCHAR(5) NOT NULL,
            title VARCHAR(500) NOT NULL,
            content MEDIUMTEXT,
            create_date DATETIME NOT NULL,
            edit_date DATETIME NOT NULL
            );"""
            cur.execute(table)

    def add(self, values:Text) -> Text:
        with db.db_manager(change=True) as cur:
            date_now = self.__datenow()
            data = (values.title, values.content, date_now, date_now)
            insert = """INSERT INTO text(type, title, content, create_date, edit_date) VALUES('txt', ?, ?, ?, ?)"""
            cur.execute(insert, data)
            print(f"Item added: Title: {values.title} Content: {values.content}")

            values.create_date = date_now
            values.edit_date = date_now
            return values

    def get_by_id(self, id:int) -> Optional[Text]:
        with db.db_manager() as cur:
            # 0:id, 1:type, 2:title, 3:content, 4:create_date, 5:edit_date
            query = cur.execute("SELECT * FROM text WHERE id=?", id).fetchone()
            if query != None:
                return Text(title=query[2], content=query[3], create_date=query[4], edit_date=query[5])

            return Text.response_error(f"User {id} not found!")

    def remove_by_id(self, id:int) -> bool:
        with db.db_manager(change=True) as cur:
            count_table_query = "SELECT COUNT(*) FROM text"
            count_before = cur.execute(count_table_query).fetchone()[0]

            delete_query = f"DELETE FROM text WHERE id={id}"
            cur.execute(delete_query)

            count_after = cur.execute(count_table_query).fetchone()[0]
            if count_before != count_after:
                print(f"User {id} deleted")
                return True
            
            print(f"User {id} not found")
            return False
    
    # private methods
    def __datenow(self) -> str:
        now = datetime.now()
        return now.strftime(f"%Y-%m-%d %H:%M:%S")
