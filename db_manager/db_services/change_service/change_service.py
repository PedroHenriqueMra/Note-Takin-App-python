from bson.objectid import ObjectId
import ast

from abc import abstractmethod

from db_manager.connections.mgdb_connection import mongodb
from db_manager.connections.sqlite_connection import sqlite

from exceptions.tab_not_exists import TableNotExistsException

from system_data.change_data import Change, ChangeInsert
from utils.dictsetter import *
from utils.row_exists import row_exists
from typing import List, Dict

import os
from dotenv import load_dotenv
load_dotenv()

import logging
logging.addLevelName(level=1, levelName="change_service")
logging.BASIC_FORMAT = "\n%(levelname)s:%(name)s:%(message)s"


class ChangeService():
    def __init__(self, table_id:ObjectId|str) -> None:
        self.table_id:ObjectId | str = table_id
        self.table_data:dict = dict()
        self.tab_opened:Dict[str,int] = {"text":0}
        
        self.change_table(table_id)

    def change_table(self, table_id:ObjectId|str) -> None:
        table_id = table_id if isinstance(table_id, ObjectId) else ObjectId(table_id)

        try:
            self.__get_table_data(table_id)
        except TableNotExistsException as err:
            logging.error(f"Error While the table change. Error message: {err}")
    
    def open_tab(self, note_id:int|None=None) -> dict | None:
        if self.tab_opened.keys() not in ["text","note"]:
            self.open_tab = {"text":0}
            return
        
        if note_id is None:
            self.tab_opened = {"text":0}
        else:
            for note in self.table_data["content"]["notes"]:
                if note["id"] == note_id:
                    self.tab_opened = {"note":note_id}

            if "note" not in self.tab_opened.keys():
                self.open_tab = {"text":0}
                return

        return self.tab_opened

    
    def __get_table_data(self, table_id:ObjectId) -> None:
        with mongodb.context_database() as db:
            connection_string = os.getenv("TABLE_COLLACTION")
            database = db[connection_string]
            table = database.find_one({"_id": table_id})
            if table is None:
                raise TableNotExistsException(table_id, "This table was not found!.")
            
            self.table_data = ast.literal_eval(table)
    
    def __replace_equalScripts(self, list:List[Change], change_data:Change) -> List[Change]:
        for index, change_item in enumerate(list):
            if type(change_item) == type(change_data) and hasattr(change_data, "change_starts"):
                if list.index(change_data) != index:
                    if change_item.change_starts == change_data.change_starts:
                        list.pop()
                        list[index] = change_data
        
        return list

    def include_query(self, change:Change) -> list | None:
        self.table_data["changes"]["changed"] = True

        if change.table_type == "text":
            self.table_data["changes"]["text"]["change_scripts"].append(change)
            change_scripts = self.table_data["changes"]["text"]["change_scripts"]
            self.table_data["changes"]["text"]["changed"] = True
        else:
            indx = None
            for index, note in enumerate(self.table_data["changes"]["notes"]):
                if note["id"] == change.table_id:
                    indx = index
                    break
            
            if indx == None:
                return
            
            self.table_data["changes"]["notes"][indx]["change_scripts"].append(change)
            change_scripts = self.table_data["changes"]["notes"][indx]["change_scripts"]
            self.table_data["changes"]["notes"][indx]["changed"] = True

        script_list = self.__replace_equalScripts(change_scripts, change)
        script_list = self.__organize_orderScripts(script_list)

        dictSetter(self.table_data, f"changes/{change.table_type}/change_scripts", script_list)

        return script_list
    

    def __organize_orderScripts(self, script_list:list) -> list:
        inserts = list()
        rest_objs = list()
        for item in script_list:
            print(f"type obj::: {type(item)}")
            if isinstance(item, ChangeInsert):
                inserts.append(item)
                continue
            
            print(f"type que entrou no rest::: {type(item)}")
            rest_objs.append(item)

        rest_objs.sort(key=lambda x: x.change_starts)
        return rest_objs + inserts

    def save(self) -> None:
        self.__desableAll_changed_statment()

        with sqlite.db_connection() as cur:
            for txt in self.table_data["changes"]["text"]["change_scripts"]:
                script = txt.gen_change_script()
                cur.execute(script[0], script[1])
           
            count_note_altereds = []
            for notes in self.table_data["changes"]["notes"]:
                for note_scr in notes["change_scripts"]:
                    script = note_scr.gen_change_script()
                    cur.execute(script[0], script[1])
                    count_note_altereds.append(notes["id"])

        txt_wasChanged = True if len(self.table_data["changes"]["text"]["change_scripts"]) > 0 else False
        
        count_note_altereds = None if len(count_note_altereds) == 0 else count_note_altereds
        
        # Atualize content
        # All
        if len(self.table_data["changes"]["notes"]) == len(count_note_altereds):
            self.atualize_content(note_ids=count_note_altereds, all=txt_wasChanged)

        # Only notes or Only text
        self.atualize_content(note_ids=count_note_altereds, all=False)
        
        self.__remove_scripts(all=True)

    def atualize_content(self, note_ids:List[int]|None, all:bool=False):
        with sqlite.db_connection() as cur:
            if all or note_ids is None:
                txt_content = cur.execute("SELECT * FROM text WHERE id = ?", (self.table_data["content"]["text"]["id"],)).fetchone()
                txt_content = {
                    "id":txt_content["id"],
                    "type":txt_content["type"],
                    "title":txt_content["title"],
                    "content":txt_content["content"],
                    "create_date":txt_content["create_date"],
                    "edit_date": txt_content["edit_date"]}
                self.table_data["content"]["text"] = txt_content

            if all or note_ids is not None:
                if all:
                    note_ids = list()
                    for note_id in self.table_data["content"]["notes"]:
                        note_ids.append(note_id["id"])
                
                for n_id in note_ids:
                    note_content = cur.execute("SELECT * FROM note WHERE id = ?", (n_id,))
                    note_content = {
                        "id": note_content["id"],
                        "type": note_content["type"],
                        "reference": note_content["reference"],
                        "content": note_content["content"],
                        "create_date": note_content["create_date"],
                        "edit_date": note_content["edit_date"]
                    }
                    if note_content["id"] is None:
                        continue

                    for index, note in enumerate(self.table_data["content"]["notes"]):
                        if  note["id"] == n_id:
                            self.table_data["content"]["notes"][index] = note_content
                            break

        with mongodb.context_database() as db:
            connection_string = os.getenv("TABLE_COLLACTION")
            database = db[connection_string]
            database.update_one(
                filter={"_id": self.table_id},
                update={"$set":str(self.table_data)},
                upsert=False)

    def __desableAll_changed_statment(self) -> None:
        self.table_data["changes"]["changed"] = False
        
        notes = self.table_data["changes"]["notes"]
        for note in notes:
            note["changed"] = False

        self.table_data["changes"]["text"]["changed"] = False

    def __remove_scripts(self, note_id:int|None=None, all:bool=False) -> None:
        if note_id == None or all:
            self.table_data["changes"]["text"]["change_scripts"] = []
            if not all:
                return
        
        for note in self.table_data["changes"]["notes"]:
            if note["id"] == note_id or all:
                note["change_scripts"] = []
