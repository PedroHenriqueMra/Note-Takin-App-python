import json
import ast
from utils.row_exists import row_exists

from db_manager.repository.sql_repository.irepository import IRepository
from ...connections.sqlite_connection import sqlite_conn

from system_data.sql_tables_data import Link
from system_data.sql_tables_data import Note
from typing import Any, Optional

# show info
import logging
logging.addLevelName("Link_Handler")
logging.BASIC_FORMAT = "\n%(levelname)s:%(name)s:%(message)s"


class ADMLink(IRepository[Link]):
    cursor = sqlite_conn.cursor()

    def __init__(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS link (
        id VARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
        text_id INTEGER,
        note_ids json INTEGER,
        FOREIGN KEY(text_id) EFERENCES text(id),
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

        logging.info(f"New link row created:\nLink id: {values.id}\nText id {values.text_id}\nNote ids: {values.note_ids}")

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
            logging.warning(f"The text ({text_id}) doesn't exist")
            cls.add_row(Link(text_id, [note_id]))

        link_row = cls.cursor.execute(select_query, (text_id,)).fetchone()
        note_ids = ast.literal_eval(link_row["note_ids"])
        if note_id not in note_ids:
            note_ids.append(note_id)

        update_query = "UPDATE link SET note_ids=? WHERE id=?"
        cls.cursor.execute(update_query, (json.dumps(note_ids), link_row["id"])).fetchone()
        logging.info(f"Note ({note_id}) was linked with text ({text_id}) successfuly.")
        
        # get note data
        get_note_query = "SELECT * FROM note WHERE id=? LIMIT 1"
        note = cls.cursor.execute(get_note_query, (note_id,)).fetchone()

        return Note(
        linked_text_id=text_id,
        reference=note["reference"],
        content=note["content"],
        create_date=note["create_date"],
        edit_date=note["edit_date"])


    @classmethod
    def remove_note(cls, note_id:int) -> None:
        query_select = "SELECT * FROM link, json_each(note_ids) WHERE json_each.value LIKE (?)"
        link_row = cls.cursor.execute(query_select, (str(note_id))).fetchmany()
        if len(link_row) is 0:
            logging.warning(f"The note ({note_id}) isn't linked to any text")
            return
        
        # check others possible results found
        for row in link_row:
            id_list = ast.literal_eval(row["note_ids"])
            if note_id in id_list:
                link_row = row
                break
        
        table_id = link_row["id"]
        old_note_ids = ast.literal_eval(link_row["note_ids"])
        new_note_ids = json.dumps([n for n in old_note_ids if n != note_id])

        query_replace = "UPDATE link SET note_ids=? WHERE id=?"
        cls.cursor.execute(query_replace, (new_note_ids, table_id))
        logging.info(f"Note ({note_id}) was deleted from linked text ({link_row["text_id"]})")


    def update(self, id:int|str, field:str, value:Any) -> Optional[Link]:
        pass
