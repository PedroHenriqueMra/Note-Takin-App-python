from db_manager.repository.irepository import IRepository
from typing import Any, Optional
from db_manager.repository.SQL_layer.link_handler import ADMLink
from utils.date_now import date_now
from ...connection.sqlite_connection import sqlite

# show info
import logging
logging.basicConfig(level=logging.INFO)

from data.SQL_table_data import Text

class ADMText(IRepository[Text]):
    def __init__(self):
        # create table
        with sqlite.db_connection(change=True) as cur:
            table = """CREATE TABLE IF NOT EXISTS text (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type VARCHAR(5) NOT NULL,
            title VARCHAR(500) NOT NULL,
            content MEDIUMTEXT,
            create_date DATETIME NOT NULL,
            edit_date DATETIME NOT NULL
            );"""
            cur.execute(table)

    def add_row(self, values:Text) -> Text:
        with sqlite.db_connection(change=True) as cur:
            get_date_now = date_now()
            data = (values.title, values.content, get_date_now, get_date_now)
            insert = """INSERT INTO text(type, title, content, create_date, edit_date) VALUES('txt', ?, ?, ?, ?)"""
            cur.execute(insert, data)
            logging.info(f"Item added: Title: {values.title} Content: {values.content}")

            return Text (title=values.title,content=values.content,create_date=get_date_now,edit_date=get_date_now)

    def get(self, id:int) -> Optional[Text]:
        with sqlite.db_connection(change=True) as cur:
            # 0:id, 1:type, 2:title, 3:content, 4:create_date, 5:edit_date
            query = cur.execute("SELECT * FROM text WHERE id=?", (id,)).fetchone()
            if query != None:
                return Text(title=query[2], content=query[3], create_date=query[4], edit_date=query[5])

            return None

    def delete(self, id:int) -> bool:
        with sqlite.db_connection(change=True) as cur:
            count_table_query = "SELECT COUNT(*) FROM text"
            count_before = cur.execute(count_table_query).fetchone()[0]

            delete_query = f"DELETE FROM text WHERE id={id}"
            cur.execute(delete_query)

            count_after = cur.execute(count_table_query).fetchone()
            [0]

            if count_before != count_after:
                ADMLink.delete_associations(id)
                logging.info(f"Text {id} deleted")
                return True
            
            logging.info(f"Text {id} not found")
            return False
        
    def update(self, id:int|str, field:str, value:Any) -> Optional[Text]:
        pass
