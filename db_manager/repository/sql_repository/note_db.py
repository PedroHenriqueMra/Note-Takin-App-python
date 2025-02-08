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
        linked_text_id INTEGER NOT NULL,
        FOREIGN KEY(linked_text_id) REFERENCES text(id),
        type VARCHAR(5) NOT NULL,
        reference VARCHAR(50) NOT NULL,
        content TEXT,
        create_date DATETIME NOT NULL,
        edit_date DATETIME NOT NULL
        );"""
        self.cursor.execute(create_table_query)

    def add_row(self, values:Note) -> Note|None:
        if not row_exists("text", values.linked_text_id):
            return
        
        insert_query = "INSERT INTO note(linked_text_id, type, reference, content, create_date, edit_date) VALUES(?, 'note', ?, ?, ?, ?)"
        data_query = (values.linked_text_id, values.reference, values.content, current_date(), current_date())
        self.cursor.execute(insert_query, data_query)
        row_id = self.cursor.lastrowid

        logging.info(f"New note row created:\nlinked_text: {values.linked_text_id}\nreference: {values.reference}\nContent: {values.content}")
        ADMLink.append_note(values.linked_text_id, row_id)

        return Note (linked_text_id=values.linked_text_id, reference=values.reference,content=values.content,create_date=current_date(),edit_date=current_date())

    def get_row(self, id:int) -> Optional[Note]:
        query = "SELECT * FROM note WHERE id=?"
        data = self.cursor.execute(query, (id,)).fetchone()
        if query == None:
            return None

        return Note(linked_text_id=data["linked_text"], reference=data["reference"], content=data["content"], create_date=data["create_date"], edit_date=data["edit_date"])

    def delete(self, id:int) -> bool:
        count_before = self.cursor.execute("SELECT COUNT(*) FROM note").fetchone()
        delete_query = f"DELETE FROM note WHERE id=?"
        self.cursor.execute(delete_query, (id,))
        count_after = self.cursor.execute("SELECT COUNT(*) FROM note").fetchone()

        if count_before == count_after:
            logging.info(f"Note ({id}) not found")
            return False
        
        logging.info(f"Note ({id}) deleted")
        return False

    def update(self, id:int|str, field:str, value:Any) -> Optional[Note]:
        valid_fields = ["reference", "content"]
        if field not in valid_fields:
            logging.warning(f"{field} is not allowed!")
            return

        if type(value) != type(Note.content) or type(value) != type(Note.reference):
            logging.warning(f"The value parameter is a wrong value type!. value type: {type(value)}")
            return
        
        note_row = self.get_row(id)
        if not note_row:
            logging.warning(f"Note {id} not exists!")
            return
        
        update_query = "UPDATE note SET {} = {} WHERE id = ?".format(field, value)
        self.cursor.execute(update_query, (id))
        
        if self.cursor.rowcount != 0:
            logging.info(f"Note row of id {id} was updated")
