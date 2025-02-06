from typing import Any, Optional
from utils.date_now import current_date
from utils.row_exists import row_exists

from db_manager.repository.irepository import IRepository
from ...connections.sqlite_connection import sqlite_conn

from system_data.sql_tables_data import Note
from db_manager.repository.sql_repository.link_handler import ADMLink

# show info
import logging
logging.addLevelName("Note_Handler")
logging.BASIC_FORMAT = "\n%(levelname)s:%(name)s:%(message)s"


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

        logging.info(f"New note row created:\nreference: {note_values.reference}\nContent: {note_values.content}")
        ADMLink.append_note(linked_text, row_id)

        return Note (reference=note_values.reference,content=note_values.content,create_date=current_date(),edit_date=current_date())

    def get_row(self, id:int) -> Optional[Note]:
        query = "SELECT * FROM note WHERE id=?"
        data = self.cursor.execute(query, (id,)).fetchone()
        if query == None:
            return None

        return Note(reference=data["reference"], content=data["content"], create_date=data["create_date"], edit_date=data["edit_date"])

    def delete(self, note_id:int) -> bool:
        count_before = self.cursor.execute("SELECT COUNT(*) FROM note").fetchone()
        delete_query = f"DELETE FROM note WHERE id=?"
        self.cursor.execute(delete_query, (note_id,))
        count_after = self.cursor.execute("SELECT COUNT(*) FROM note").fetchone()

        if count_before == count_after:
            logging.info(f"Note ({note_id}) not found")
            return False
        
        logging.info(f"Note ({note_id}) deleted")
        return False

    def update(self, id:int|str, field:str, value:Any) -> Optional[Note]:
        pass
