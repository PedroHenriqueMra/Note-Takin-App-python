from typing import Optional
from db_manager.repository.irepository import IRepository
from data.system_data import Link
from utils.row_exists import all_row_exists

# show info
import logging
logging.basicConfig(level=logging.INFO)

from db_manager.connection.connection import db

class ADMLink(IRepository[Link]):
    def __init__(self):
        with db.db_manager(change=True) as cur:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS link (
            id VARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
            text_id INTEGER NOT NULL,
            note_id INTEGER NOT NULL,
            FOREIGN KEY(text_id) REFERENCES text(id),
            FOREIGN KEY(note_id) REFERENCES note(id)
            );"""
            cur.execute(create_table_query)

    def add_row(self, values:Link) -> Link:
        if not all_row_exists(["text", "note"], [values.text_id, values.note_id]):
            return values
        
        with db.db_manager(change=True) as cur:
            inject_data = (str(values.id), values.text_id, values.note_id)
            insert = "INSERT INTO link VALUES(?, ?, ?)"
            cur.execute(insert, inject_data)
            logging.info(f"A new row created.\nLink id: {values.id}\nText id {values.text_id}\nNote id: {values.note_id}")

            return values

    def get_by_id(self, id:int) -> Optional[Link]:
        with db.db_manager() as cur: 
            query = "SELECT * FROM link WHERE id=?"
            result = cur.execute(query, (id,)).fetchone()
            if result != None:
                 return result
            
        return None

    def delete_by_id(self, id:int) -> bool:
        with db.db_manager(change=True) as cur:
            count_table_query = "SELECT COUNT(*) FROM link"
            count_before = cur.execute(count_table_query).fetchone()[0]

            delete_query = "DELETE FROM link WHERE id=?"
            cur.execute(delete_query, (id,))

            count_after = cur.execute(count_table_query).fetchone()[0]
            if count_before != count_after:
                logging.info(f"Link {id} deleted")
                return True
            
            logging.info(f"Link {id} not found")
            return False
