from typing import Any, Optional
from db_manager.repository.irepository import IRepository
from utils.date_now import date_now

# show info
import logging
logging.basicConfig(level=logging.INFO)

from data.system_data import Link, Note
from db_manager.connection.sqlite_connection import db_connection

class ADMNote(IRepository[Note]):
    def __init__(self):
        with db_connection(change=True) as cur:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type VARCHAR(5) NOT NULL,
            reference TEXT NOT NULL,
            content MEDIUMTEXT,
            create_date DATETIME NOT NULL,
            edit_date DATETIME NOT NULL
            );"""
            cur.execute(create_table_query)

    def add_row(self, values:Note) -> Note:
        with db_connection(change=True) as cur:
            get_date_now = date_now()
            data = (values.reference, values.content, get_date_now, get_date_now)
            insert = """INSERT INTO note(type, reference, content, create_date, edit_date) VALUES('note', ?, ?, ?, ?)"""
            cur.execute(insert, data)
            logging.info(f"Item added: reference: {values.reference} Content: {values.content}")

            return Note (reference=values.reference,content=values.content,create_date=get_date_now,edit_date=get_date_now)

    def get_by_id(self, id:int) -> Optional[Note]:
        with db_connection() as cur:
            # 0:id, 1:type, 2:reference, 3:content, 4:create_date, 5:edit_date
            query = cur.execute("SELECT * FROM note WHERE id=?", (id,)).fetchone()
            if query != None:
                return Note(reference=query[2], content=query[3], create_date=query[4], edit_date=query[5])

            return None

    def delete_by_id(self, id:int) -> bool:
        with db_connection(change=True) as cur:
            count_table_query = "SELECT COUNT(*) FROM note"
            count_before = cur.execute(count_table_query).fetchone()[0]

            delete_query = f"DELETE FROM note WHERE id={id}"
            cur.execute(delete_query)

            count_after = cur.execute(count_table_query).fetchone()[0]
            if count_before != count_after:
                logging.info(f"Note {id} deleted")
                return True
            
            logging.info(f"Note {id} not found")
            return False

    def update(self, id:int|str, field:str, value:Any) -> Optional[Note]:
        pass
