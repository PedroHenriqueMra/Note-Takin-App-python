from bson.objectid import ObjectId
import ast

from db_manager.connections.mgdb_connection import mongodb
from db_manager.connections.sqlite_connection import sqlite

from exceptions.tab_not_exists import TableNotExistsException

from system_data.change_data import Change
from utils.dictsetter import *
from utils.row_exists import row_exists
from typing import List

import logging
logging.addLevelName(level=1, levelName="change_service")
logging.BASIC_FORMAT = "\n%(levelname)s:%(name)s:%(message)s"


class ChangeService():
    def __init__(self, table_id:ObjectId|str) -> None:
        self.table_id:ObjectId | str = table_id
        self.table_data:dict = dict()
        
        try:
            self.__get_table_data(self.table_id)
        except TableNotExistsException as err:
            logging.error(f"Error in constructor. Message: {err}")


    def __get_table_data(self, table_id:ObjectId) -> None:
        with mongodb.context_database() as db:
            connection_string = "table_handler_test"
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
        dictSetter(self.table_data, f"changes/{change.table_type}/change_scripts", script_list)

        return script_list

    def save(self) -> None:
        self.__desableAll_changed_statment()

        with sqlite.db_connection() as cur:
            # loop to txt changes
            for txt in self.table_data["changes"]["text"]["change_scripts"]:
                script = txt.gen_change_script()
                print(f"SCRIPTTT: {script}")
                cur.execute(script[0], script[1])
           
            # loop to note changes
            for notes in self.table_data["changes"]["notes"]:
                for note_scr in notes["change_scripts"]:
                    script = note_scr.gen_change_script()
                    cur.execute(script[0], script[1])

        self.__remove_scripts()

    def save_one(self, note_id:int=None):
        self.__desableOne_changed_statment(note_id)
        self.__reset_changeStatment()
        
        with sqlite.db_connection() as cur:
            if note_id == None:
                for scr_txt in self.table_data["changes"]["text"]["change_scripts"]:
                    script = scr_txt.gen_change_script()
                    cur.execute(script[0], script[1])
            else:
                notes = self.table_data["changes"]["notes"]
                for note in notes:
                    if note["id"] == note_id:
                        for note_src in notes["change_scripts"]:
                            script = note_src.gen_change_script()
                            cur.execute(script[0], script[1])

        self.__remove_scripts_from(note_id)


    def __desableAll_changed_statment(self) -> None:
        self.table_data["changes"]["changed"] = False
        
        notes = self.table_data["changes"]["notes"]
        for note in notes:
            note["changed"] = False

        self.table_data["changes"]["text"]["changed"] = False

    def __desableOne_changed_statment(self, note_id:int|None=None) -> None:
        if note_id is not None:
            notes = self.table_data["changes"]["notes"]
            for note in notes:
                if note["id"] == note_id:
                    note["changed"] = False
            return
        
        self.table_data["changes"]["text"]["changed"] = False

    def __reset_changeStatment(self) -> None:
        notes = self.table_data["changes"]["notes"]
        for note in notes:
            if note["changed"] == True:
                return
        
        if self.table_data["changes"]["text"]["changed"] == False:
            self.table_data["changes"]["changed"] = False

    def __remove_scripts(self) -> None:
        self.table_data["changes"]["text"]["change_scripts"] = []

        for note in self.table_data["changes"]["notes"]:
            note["change_scripts"] = []

    def __remove_scripts_from(self, note_id:int|None=None) -> None:
        if note_id == None:
            self.table_data["changes"]["text"]["change_scripts"] = []
            return
        
        for note in self.table_data["changes"]["notes"]:
            if note["id"] == note_id:
                note["change_scripts"] = []

