from bson.objectid import ObjectId
import ast

from db_manager.connections.mgdb_connection import mongodb

from exceptions.tab_not_exists import TableNotExistsException

from system_data.change_data import Change
from utils.dictsetter import *
from utils.row_exists import row_exists

import logging
logging.addLevelName("change_service")
logging.BASIC_FORMAT = "\n%(levelname)s:%(name)s:%(message)s"


class ChangeService():
    def __init__(self, table_id:ObjectId) -> None:
        self.table_id:ObjectId = table_id
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
    

    def insert_query(self, change:Change) -> list | None:
        self.table_data["changes"]["changed"] = True
        
        change_scripts = self.table_data["changes"][change.table_type]["change_scripts"]

        new_script_list = self.replace_change_object(change_scripts)
        dictSetter(self.table_data, f"changes/{change.table_type}/change_scripts", new_script_list)



    def update_query(self, change:Change) -> list | None:
        self.table_data["changes"]["changed"] = True
        
    def delete_query(self, change:Change) -> list | None:
        self.table_data["changes"]["changed"] = True

    def replace_change_object(self, list:list, change_data:Change) -> list:
        for ind, ch in enumerate(list):
            if isinstance(type(change_data), type(ch)):
                if ch.change_starts == change_data.change_starts:
                    list[ind] = change_data
        
        return list


    def save(self) -> None:
        pass
