import json
import ast
from typing import Any, Optional
from db_manager.repository.irepository import IRepository
from system_data.sql_tables_data import Link
from system_data.sql_tables_data import Note
from utils.row_exists import row_exists
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

    
    def add_row(self, values:Link) -> Link | None:
        if not row_exists("text", values.text_id):
            return
        
        for note in values.note_ids:
            if not row_exists("note", note):
                return
        
        inject_data = (str(values.id), values.text_id, json.dumps(values.note_ids))
        insert = "INSERT INTO link VALUES(?, ?, ?)"
        self.cursor.execute(insert, inject_data)

        logging.info(f"A new row created.\nLink id: {values.id}\nText id {values.text_id}\nNote id: {values.note_ids}")
        sqlite_conn.commit()

        return values
    

    def get_row(self, id:str) -> Optional[Link]:
        query = "SELECT * FROM link WHERE id=?"
        result = self.cursor.execute(query, (id,)).fetchone()
        if result == None:
            return None
        
        return Link(text_id=result["text_id"], note_ids=ast.literal_eval(result["note_ids"]))
    
    
    def get_by_field(self, field:str, key:int|str) -> Optional[Link]:
        try:
            valid_fields = ["id", "text_id", "note_ids"]
            if field not in valid_fields:
                raise ValueError(f"Invalid field: {field}, Message error: {err}")
            
            data_query = (field, key)
            query = "SELECT * FROM link WHERE ?=? LiMIT 1"
            data = self.cursor.execute(query, data_query).fetchone()
            return data
        except OperationalError as err:
            logging.info(f"An unexpected error was throw. Message: {err}")
            return None
        

    def delete(self, id:int|str) -> bool:
        
        count_table_query = "SELECT COUNT(*) FROM link"
        count_before = self.cursor.execute(count_table_query).fetchone()

        delete_query = "DELETE FROM link WHERE id=?"
        self.cursor.execute(delete_query, (id,))

        count_after = self.cursor.execute(count_table_query).fetchone()
        sqlite_conn.commit()

        if count_before != count_after:
            logging.info(f"Link {id} deleted")
            return True
        
        logging.info(f"Link {id} not found")
        return False
    
    
    def add_note(self, link_id:str, note_id:int) -> Note|None:
        query_select = "SELECT * FROM link WHERE id=? LIMIT 1"
        link_row = self.cursor.execute(query_select, (link_id,))
        if link_row is None:
            return None
        
        # check note existence:
        query_select = "SELECT * FROM note WHERE id=?"
        note_row = self.cursor.execute(query_select, (note_id,))
        if note_row is None:
            return None

        note_ids = ast.literal_eval(link_row["note_ids"])
        note_ids.append(note_id)
        query_replace = "UPDATE link SET note_ids=? WHERE id=?"
        note_inserted = self.cursor.execute(query_replace, (note_ids,note_id)).fetchone()
        if note_inserted is None:
            return None
        
        return Note(reference=note_row["reference"], content=note_row["content"], create_date=note_row["create_date"], edit_date=["edit_date"])
    
        
    @classmethod
    def create_association(cls, text_id:int) -> None:
        pass

    @classmethod
    def delete_associations(cls, text_id:int) -> None:

        link = cls.get_by_field(self=cls, field="text_id", key=text_id)
        if link is not None:
            for note_id in link.note_ids:
                cls.cursor.execute("DELETE FROM note WHERE id=?", (note_id,))

            # delete link table
            cls.delete(self=cls, id=str(link.id))


    @classmethod
    def delete_note_association(cls, note_id:int) -> None:
        query_select = "SELECT * FROM link WHERE note_ids IN ?"
        link_row = cls.cursor.execute(query_select, (f"[{note_id}]",)).fetchone()
        if link_row == None:
            return
        
        table_id = query_select["id"]
        note_ids = ast.literal_eval(link_row["note_ids"])
        new_note_ids = [n for n in note_ids if n != note_id]

        data_query = (new_note_ids, table_id)
        query_replace = "UPDATE link SET note_ids=? WHERE id=?"
        cls.cursor.execute(query_replace, data_query)


    def update(self, id:int|str, field:str, value:Any) -> Optional[Link]:
        pass

