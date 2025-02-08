from typing import Union
from db_manager.repository.db_services.IGetterService import IGetterService
from db_manager.connections.sqlite_connection import sqlite
import ast

class DataGetter(IGetterService):
    def get_link_data(self, link_id:str) -> dict:
        with sqlite.db_connection(change=False) as cur:
            query = "SELECT * FROM link WHERE id=?"
            data = cur.execute(query, (link_id,)).fetchone()
            if data == None:
                return None
            
            note_ids = ast.literal_eval(data["note_ids"])
            return {
                "link_id":data["id"],
                "text_id":data["text_id"],
                "note_ids": note_ids
            }

    def get_text_data(self, text_id:int) -> dict:
        with sqlite.db_connection(change=False) as cur:
            query = "SELECT * FROM text WHERE id=?"
            data = cur.execute(query, (text_id,)).fetchone()
            if data == None:
                return None
            
            return {
                "id":data["id"],
                "type":data["type"],
                "title":data["title"],
                "content":data["content"],
                "create_date":data["create_date"],
                "edit_date": data["edit_date"]
            }
    
    def get_notes_data(self, note_ids:list) -> dict:
        with sqlite.db_connection(change=False) as cur:
            query = "SELECT * FROM note WHERE id=?"
            for id in note_ids:
                cur.execute(query, (id,))

            data = cur.fetchall()
            if len(data) < 1:
                return None
            
            res = list()
            for note in data:
                dict_note = {
                    "id":note["id"],
                    "type":note["type"],
                    "reference":note["reference"],
                    "content":note["content"],
                    "create_date":note["create_date"],
                    "edit_date":note["edit_date"]
                }
                res.append(dict_note)
            
            return res
