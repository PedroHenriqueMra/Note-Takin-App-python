from bson.objectid import ObjectId
import ast

from db_manager.connections.mgdb_connection import mongodb

from exceptions.tab_not_exists import TableNotExistsException

import logging

from system_data.change_data import Change
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
    
    def insert_query(self, change:Change, note_id:int=None) -> list | None:
        pass

    def update_query(self, change:Change, note_id:int=None) -> list | None:
        pass

    def delete_query(self, change:Change, note_id:int=None) -> list | None:
        pass

    def save(self) -> None:
        pass
