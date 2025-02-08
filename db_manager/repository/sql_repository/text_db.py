from typing import Any, Optional
from utils.date_now import current_date

from db_manager.repository.irepository import IRepository
from ...connections.sqlite_connection import sqlite_conn
from db_manager.repository.sql_repository.link_handler import ADMLink
from system_data.sql_tables_data import Text

# show info
import logging
logging.addLevelName("Text_Handler")
logging.BASIC_FORMAT = "\n%(levelname)s:%(name)s:%(message)s"


class ADMText(IRepository[Text]):
    cursor = sqlite_conn.cursor()

    def __init__(self):
        # create table
        table = """CREATE TABLE IF NOT EXISTS text (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type VARCHAR(5) NOT NULL,
        title VARCHAR(500) NOT NULL,
        content MEDIUMTEXT,
        create_date DATETIME NOT NULL,
        edit_date DATETIME NOT NULL
        );"""
        self.cursor.execute(table)


    def add_row(self, values:Text) -> Text:
        insert_query = "INSERT INTO text(type, title, content, create_date, edit_date) VALUES('txt', ?, ?, ?, ?)"
        data_query = (values.title, values.content, current_date(), current_date())
        self.cursor.execute(insert_query, data_query)
        
        logging.info(f"New text row created:\nTitle: {values.title}\nContent: {values.content}")
        return Text (title=values.title,content=values.content, create_date=current_date(), edit_date=current_date())


    def get_row(self, id:int) -> Optional[Text]:
        query = self.cursor.execute("SELECT * FROM text WHERE id=?", (id,)).fetchone()
        if query is None:
            return None
        
        return Text(title=query["title"], content=query["content"], create_date=query["create_date"], edit_date=query["edit_date"])


    def delete(self, id:int) -> bool:
        count_before = self.cursor.execute("SELECT COUNT(*) FROM text").fetchone()
        delete_query = f"DELETE FROM text WHERE id=?"
        self.cursor.execute(delete_query, (id,))
        count_after = self.cursor.execute("SELECT COUNT(*) FROM text").fetchone()

        if count_before != count_after:
            ADMLink.delete(id)
            logging.info(f"Text ({id}) deleted")
            return True
        
        logging.info(f"Text ({id}) not found")
        return False
        
        
    def update(self, id:int|str, field:str, value:Any) -> Optional[Text]:
        valid_fields = ["title", "content"]
        if field not in valid_fields:
            logging.warning(f"{field} is not allowed!")
            return

        if type(value) != type(Text.title) or type(value) != type(Text.content):
            logging.warning(f"The value parameter is a wrong value type!. value type: {type(value)}")
            return
        
        note_row = self.get_row(id)
        if not note_row:
            logging.warning(f"Text {id} not exists!")
            return
        
        update_query = "UPDATE text SET {} = {} WHERE id = ?".format(field, value)
        self.cursor.execute(update_query, (id))
        
        if self.cursor.rowcount != 0:
            logging.info(f"Text row of id {id} was updated")
