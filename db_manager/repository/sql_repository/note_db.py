from typing import Any, Optional
from db_manager.repository.irepository import IRepository
from utils.date_now import date_now
from ...connections.sqlite_connection import sqlite_conn
from system_data.sql_tables_data import Note

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
        create_table = self.cursor.execute(create_table_query)
        if create_table is not None:
            sqlite_conn.commit()

    def add_row(self, values:Note) -> Note:
        get_date_now = date_now()
        data = (values.reference, values.content, get_date_now, get_date_now)
        insert = """INSERT INTO note(type, reference, content, create_date, edit_date) VALUES('note', ?, ?, ?, ?)"""
        self.cursor.execute(insert, data)
        logging.info(f"Item added: reference: {values.reference} Content: {values.content}")

        sqlite_conn.commit()
        return Note (reference=values.reference,content=values.content,create_date=get_date_now,edit_date=get_date_now)

    def get(self, id:int) -> Optional[Note]:
        # 0:id, 1:type, 2:reference, 3:content, 4:create_date, 5:edit_date
        query = self.cursor.execute("SELECT * FROM note WHERE id=?", (id,)).fetchone()
        if query != None:
            return Note(reference=query[2], content=query[3], create_date=query[4], edit_date=query[5])

        return None

    def delete(self, id:int) -> bool:
        count_table_query = "SELECT COUNT(*) FROM note"
        count_before = self.cursor.execute(count_table_query).fetchone()[0]

        delete_query = f"DELETE FROM note WHERE id={id}"
        self.cursor.execute(delete_query)

        count_after = self.cursor.execute(count_table_query).fetchone()[0]
        if count_before != count_after:
            logging.info(f"Note {id} deleted")
            return True
        
        logging.info(f"Note {id} not found")
        return False

    def update(self, id:int|str, field:str, value:Any) -> Optional[Note]:
        pass
