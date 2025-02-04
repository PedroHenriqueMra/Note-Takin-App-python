from typing import Any, Optional
from db_manager.repository.irepository import IRepository
from utils.date_now import current_date
from utils.row_exists import row_exists
from ...connections.sqlite_connection import sqlite_conn
from system_data.sql_tables_data import Note
from db_manager.repository.sql_repository.link_handler import ADMLink
from system_data.sql_tables_data import Link

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
        create_date DATETIME NOT NULL,
        edit_date DATETIME NOT NULL
        );"""
        self.cursor.execute(create_table_query)

    def add_row(self, linked_text:int, note_values:Note) -> Note|None:
        if not row_exists("text", linked_text):
            return
        
        insert_query = "INSERT INTO note(type, reference, content, create_date, edit_date) VALUES('note', ?, ?, ?, ?)"
        data_query = (note_values.reference, note_values.content, current_date(), current_date())
        self.cursor.execute(insert_query, data_query)
        row_id = self.cursor.lastrowid

        logging.info(f"Note added: reference: {note_values.reference} Content: {note_values.content}")
        ADMLink.append_note(linked_text, row_id)

        return Note (reference=note_values.reference,content=note_values.content,create_date=current_date(),edit_date=current_date())

    def get_row(self, id:int) -> Optional[Note]:
        query = "SELECT * FROM note WHERE id=?"
        data = self.cursor.execute(query, (id,)).fetchone()
        if query == None:
            return None

        return Note(reference=data["reference"], content=data["content"], create_date=data["create_date"], edit_date=data["edit_date"])

    def delete(self, id:int) -> None:
        count_before = self.cursor.execute("SELECT COUNT(*) FROM note").fetchone()
        delete_query = "DELETE FROM note WHERE id=?"
        self.cursor.execute(delete_query, (id,))
        count_after = self.cursor.execute("SELECT COUNT(*) FROM note").fetchone()

        if count_before == count_after:
            return
        
        logging.log(f"Note {id} deleted!")
        ADMLink.remove_note(id)

    def update(self, id:int|str, field:str, value:Any) -> Optional[Note]:
        pass
