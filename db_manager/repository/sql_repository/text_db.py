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


    def add_row(self, text_values:Text) -> Text:
        insert_query = "INSERT INTO text(type, title, content, create_date, edit_date) VALUES('txt', ?, ?, ?, ?)"
        data_query = (text_values.title, text_values.content, current_date(), current_date())
        self.cursor.execute(insert_query, data_query)
        
        logging.info(f"New text row created:\nTitle: {text_values.title}\nContent: {text_values.content}")
        return Text (title=text_values.title,content=text_values.content, create_date=current_date(), edit_date=current_date())


    def get_row(self, id:int) -> Optional[Text]:
        query = self.cursor.execute("SELECT * FROM text WHERE id=?", (id,)).fetchone()
        if query is None:
            return None
        
        return Text(title=query["title"], content=query["content"], create_date=query["create_date"], edit_date=query["edit_date"])


    def delete(self, text_id:int) -> bool:
        count_before = self.cursor.execute("SELECT COUNT(*) FROM text").fetchone()
        delete_query = f"DELETE FROM text WHERE id=?"
        self.cursor.execute(delete_query, (text_id,))
        count_after = self.cursor.execute("SELECT COUNT(*) FROM text").fetchone()

        if count_before != count_after:
            ADMLink.delete(text_id)
            logging.info(f"Text ({text_id}) deleted")
            return True
        
        logging.info(f"Text ({text_id}) not found")
        return False
        
        
    def update(self, id:int|str, field:str, value:Any) -> Optional[Text]:
        pass
