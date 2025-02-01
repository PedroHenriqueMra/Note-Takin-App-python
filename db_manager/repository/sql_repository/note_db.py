from typing import Any, Optional
from db_manager.repository.irepository import IRepository
from utils.date_now import date_now
from ...connections.sqlite_connection import sqlite_conn
from system_data.sql_tables_data import Note
from db_manager.repository.sql_repository.link_handler import ADMLink

# show info
import logging
logging.basicConfig(level=logging.INFO)


class ADMNote(IRepository[Note]):
    cursor = sqlite_conn.cursor()

    def __init__(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS note (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type VARCHAR(5) NOT NULL,
        reference VARCHAR(50) NOT NULL,
        content TEXT,
        create_date DATETIME NOT NULL DEFAULT current_timestamp,
        edit_date DATETIME NOT NULL DEFAULT current_timestamp
        );"""
        create_table = self.cursor.execute(create_table_query)
        if create_table is not None:
            sqlite_conn.commit()

    def add_row(self, linked_text_:int, values:Note) -> Note:
        

        data = (values.reference, values.content)
        insert_query = "INSERT INTO note(type, reference, content, create_date, edit_date) VALUES('note', ?, ?)"
        inserted = self.cursor.execute(insert_query, data).fetchone()
        logging.info(f"Item added: reference: {values.reference} Content: {values.content}")

        sqlite_conn.commit()
        return Note (reference=inserted["reference"],content=inserted["content"],create_date=inserted["create_date"],edit_date=inserted["edit_date"])

    def get_row(self, id:int) -> Optional[Note]:
        query = "SELECT * FROM note WHERE id=?"
        data = self.cursor.execute(query, (id,)).fetchone()
        if query != None:
            return Note(reference=data["reference"], content=data["content"], create_date=data["create_date"], edit_date=data["edit_date"])

        return None

    def delete(self, id:int) -> bool:
        count_table_query = "SELECT COUNT(*) FROM note"
        count_before = self.cursor.execute(count_table_query).fetchone()

        delete_query = f"DELETE FROM note WHERE id=?"
        self.cursor.execute(delete_query, (id))

        count_after = self.cursor.execute(count_table_query).fetchone()
        if count_before != count_after:
            ADMLink.delete_note_association(id)
            logging.info(f"Note {id} deleted")
            return True
        
        logging.info(f"Note {id} not found")
        return False

    def update(self, id:int|str, field:str, value:Any) -> Optional[Note]:
        pass
