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
        self.cursor.execute(create_table_query)


    @classmethod
    def add_row(cls, values:Link) -> Link | None:
        if not row_exists("text", values.text_id):
            return
        
        for note in values.note_ids:
            if not row_exists("note", note):
                return
        
        inject_data = (str(values.id), values.text_id, json.dumps(values.note_ids))
        insert = "INSERT INTO link VALUES(?, ?, ?)"
        cls.cursor.execute(insert, inject_data)

        logging.info(f"A new row created.\nLink id: {values.id}\nText id {values.text_id}\nNote id: {values.note_ids}")

        return values
    

    @classmethod
    def get_row(cls, id:str) -> Optional[Link]:
        query = "SELECT * FROM link WHERE id=?"
        result = cls.cursor.execute(query, (id,)).fetchone()
        if result == None:
            return None
        
        return Link(text_id=result["text_id"], note_ids=ast.literal_eval(result["note_ids"]))
    
    
    @classmethod
    def delete(cls, text_id:int) -> None:

        link = cls.get_row_by_field(field="text_id", key=text_id)
        if link is None:
            return
    
        for note_id in link.note_ids:
            cls.cursor.execute("DELETE FROM note WHERE id=?", (note_id,))

        cls.cursor.execute("DELETE FROM link WHERE id=?", (link.id,))
    

    @classmethod
    def get_row_by_field(cls, field:str, key:int|str) -> Optional[Link]:
        valid_fields = ["id", "text_id", "note_ids"]
        if field not in valid_fields:
            return
        
        query = "SELECT * FROM link WHERE {}={} LiMIT 1".format(field, key)
        data = cls.cursor.execute(query).fetchone()
        return Link(id=data["id"], text_id=data["text_id"], note_ids=ast.literal_eval(data["note_ids"]))
    

    @classmethod
    def append_note(cls, text_id:int, note_id:int) -> Note|None:
        if not row_exists("text", text_id):
            return
        if not row_exists("note", note_id):
            return

        select_query = "SELECT * FROM link WHERE text_id=? LIMIT 1"
        cls.cursor.execute(select_query, (text_id,))
        if cls.cursor.fetchone() is None:
            cls.add_row(Link(text_id, [note_id]))

        link_row = cls.cursor.execute(select_query, (text_id,)).fetchone()
        note_ids = ast.literal_eval(link_row["note_ids"])
        if note_id not in note_ids:
            note_ids.append(note_id)

        note_inserted = cls.cursor.execute(
        "UPDATE link SET note_ids=? WHERE id=?",
        (json.dumps(note_ids), link_row["id"])).fetchone()
        
        return Note(reference=note_inserted["reference"],
        content=note_inserted["content"],
        create_date=note_inserted["create_date"],
        edit_date=note_inserted["edit_date"])


    @classmethod
    def remove_note(cls, note_id:int) -> None:
        query_select = "SELECT * FROM link WHERE note_ids IN ?"
        link_row = cls.cursor.execute(query_select, (f"{note_id}",)).fetchmany()
        if link_row is None:
            return
        
        # check others possible results found
        note_ids = None
        for row in link_row:
            id_list = ast.literal_eval(row["note_ids"])
            if id_list in note_ids:
                note_ids = id_list
                break
                
        if note_ids is None:
            return
        
        table_id = link_row["id"]
        new_note_ids = [n for n in note_ids if n != note_id]

        query_replace = "UPDATE link SET note_ids={} WHERE id={}".format(new_note_ids, table_id)
        cls.cursor.execute(query_replace)


    def update(self, id:int|str, field:str, value:Any) -> Optional[Link]:
        pass
