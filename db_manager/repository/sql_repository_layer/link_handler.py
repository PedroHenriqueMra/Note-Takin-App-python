import json
from sqlite3 import OperationalError
from typing import Any, Optional
from db_manager.repository.irepository import IRepository
from system_data.sql_tables_data import Link
from utils.row_exists import all_row_exists
from ...connection.sqlite_connection import sqlite

# show info
import logging
logging.basicConfig(level=logging.INFO)

class ADMLink(IRepository[Link]):
    def __init__(self):
        with sqlite.db_connection(change=True) as cur:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS link (
            id VARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
            text_id INTEGER,
            note_id json INTEGER,
            FOREIGN KEY(text_id) REFERENCES text(id),
            FOREIGN KEY(note_id) REFERENCES note(id)
            );"""
            cur.execute(create_table_query)

    def add_row(self, values:Link) -> Link:
        if not all_row_exists(["text", "note"], [values.text_id, values.note_id]):
            return values
        
        with sqlite.db_connection(change=True) as cur:
            inject_data = (str(values.id), values.text_id, json.dumps([values.note_id]))
            insert = "INSERT INTO link VALUES(?, ?, ?)"
            cur.execute(insert, inject_data)

            logging.info(f"A new row created.\nLink id: {values.id}\nText id {values.text_id}\nNote id: {values.note_id}")

            return values

    def get(self, id:int) -> Optional[Link]:
        with sqlite.db_connection(change=True) as cur:
            query = "SELECT * FROM link WHERE id=?"
            result = cur.execute(query, (id,)).fetchone()
            if result != None:
                 return result
            
        return None
    
    def get_by_field(self, field:str, key:int|str) -> Optional[Link]:
        with sqlite.db_connection(change=True) as cur:
            try:
                valid_fields = ["id", "text_id", "note_id"]
                if field not in valid_fields:
                    raise ValueError(f"Invalid field: {field}, Message error: {err}")
                
                data = cur.execute(f"SELECT * FROM link WHERE {field}=?", (key,)).fetchone()
                return data
            except OperationalError as err:
                logging.info(f"An unexpected error was throw. Message: {err}")
                return None

    def delete(self, id:int|str) -> bool:
        with sqlite.db_connection(change=True) as cur:
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
        
    @classmethod
    def delete_associations(cls, text_id:int) -> None:

        link = cls.get_by_field(self=cls, field="text_id", key=text_id)
        if link is not None:
            with sqlite.db_connection(change=True) as cur:
                # delete text
                cur.execute("DELETE FROM text WHERE id=?", (link[1],))

                # delete note
                for note_id in json.loads(link[2]):
                    cur.execute("DELETE FROM note WHERE id=?", (note_id,))

            # delete link table
            cls.delete(self=cls, id=link[0])

    def update(self, id:int|str, field:str, value:Any) -> Optional[Link]:
        pass

