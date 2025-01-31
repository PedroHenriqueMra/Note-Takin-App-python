import json
from typing import Any, Optional
from db_manager.repository.irepository import IRepository
from system_data.sql_tables_data import Link
from utils.row_exists import all_row_exists
from sqlite3 import OperationalError
from ...connections.sqlite_connection import sqlite_conn

# show info
import logging
logging.basicConfig(level=logging.INFO)


class ADMLink(IRepository[Link]):
    cursor = sqlite_conn.cursor()

    def __init__(self):

        create_table_query = """
        CREATE TABLE IF NOT EXISTS link (
        id VARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
        text_id INTEGER,
        note_ids json INTEGER,
        FOREIGN KEY(text_id) REFERENCES text(id),
        FOREIGN KEY(note_ids) REFERENCES note(id)
        );"""
        create_table = self.cursor.execute(create_table_query)
        if create_table is not None:
            sqlite_conn.commit()

    def add_row(self, values:Link) -> Link:
        if not all_row_exists(["text", "note"], [values.text_id, values.note_id]):
            return values
        
        inject_data = (str(values.id), values.text_id, json.dumps([values.note_id]))
        insert = "INSERT INTO link VALUES(?, ?, ?)"
        self.cursor.execute(insert, inject_data)

        logging.info(f"A new row created.\nLink id: {values.id}\nText id {values.text_id}\nNote id: {values.note_id}")
        sqlite_conn.commit()

        return values

    def get(self, id:int) -> Optional[Link]:
        query = "SELECT * FROM link WHERE id=?"
        result = self.cursor.execute(query, (id,)).fetchone()
        if result != None:
                return result
            
        return None
    
    def get_by_field(self, field:str, key:int|str) -> Optional[tuple]:
        try:
            valid_fields = ["id", "text_id", "note_id"]
            if field not in valid_fields:
                raise ValueError(f"Invalid field: {field}, Message error: {err}")
            
            data = self.cursor.execute(f"SELECT * FROM link WHERE {field}=?", (key,)).fetchone()
            return data
        except OperationalError as err:
            logging.info(f"An unexpected error was throw. Message: {err}")
            return None

    def delete(self, id:int|str) -> bool:
        
        count_table_query = "SELECT COUNT(*) FROM link"
        count_before = self.cursor.execute(count_table_query).fetchone()[0]

        delete_query = "DELETE FROM link WHERE id=?"
        self.cursor.execute(delete_query, (id,))

        count_after = self.cursor.execute(count_table_query).fetchone()[0]
        sqlite_conn.commit()

        if count_before != count_after:
            logging.info(f"Link {id} deleted")
            return True
        
        logging.info(f"Link {id} not found")
        return False
        
    @classmethod
    def delete_associations(cls, text_id:int) -> None:

        link = cls.get_by_field(self=cls, field="text_id", key=text_id)
        if link is not None:
            # delete note
            for note_id in json.loads(link[2]):
                cls.cursor.execute("DELETE FROM note WHERE id=?", (note_id,))

            # delete link table
            cls.delete(self=cls, id=link[0])

    def update(self, id:int|str, field:str, value:Any) -> Optional[Link]:
        pass

