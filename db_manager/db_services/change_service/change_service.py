from bson.objectid import ObjectId
import ast

from db_manager.connections.mgdb_connection import mongodb
from db_manager.connections.sqlite_connection import sqlite

from exceptions.tab_not_exists import TableNotExistsException

from system_data.change_data import Change
from utils.dictsetter import *
from utils.row_exists import row_exists

import logging
logging.addLevelName("change_service")
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
    

    def __replace_change_object(self, list:list, change_data:Change) -> list:
        for indx, chang in enumerate(list):
            if isinstance(type(change_data), type(chang)):
                if chang.change_starts == change_data.change_starts:
                    list[indx] = change_data.gen_change_script()
        
        return list

    def include_query(self, change:Change) -> list | None:
        self.table_data["changes"]["changed"] = True

        if change.table_type == "note":
            indx = None
            for note in self.table_data["changes"]["notes"]:
                if note == change.table_id:
                    indx = change.table_id
            
            if indx == None:
                return
            
            change_scripts = self.table_data["changes"][change.table_type][indx]["change_scripts"]
            self.table_data["changes"][change.table_type][indx]["change_scripts"].append(change.gen_change_script())
        else:
            self.table_data["changes"][change.table_type]["change_scripts"].append(change.gen_change_script())
            change_scripts = self.table_data["changes"][change.table_type]["change_scripts"]

        new_script_list = self.__replace_change_object(change_scripts, change)
        dictSetter(self.table_data, f"changes/{change.table_type}/change_scripts", new_script_list)

        return new_script_list

    def save(self) -> None:
        with sqlite.db_connection() as cur:
            # loop to txt changes
            for txt in self.table_data["changes"]["text"]["change_scripts"]:
                cur.execute(txt["change_scripts"])
           
            # loop to note changes
            for notes in self.table_data["changes"]["notes"]:
                for n in notes:
                    cur.execute(n["change_scripts"])

