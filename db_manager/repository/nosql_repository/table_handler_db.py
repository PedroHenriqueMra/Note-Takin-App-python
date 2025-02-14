from typing import Union
from db_manager.connections.mgdb_connection import mongo_conn

from pymongo.collection import Collection
from bson.objectid import ObjectId

from db_manager.db_services.getter_service.IGetterService import IGetterService
from utils.date_now import current_date

import logging
logging.addLevelName("Table_Handler_db")
logging.BASIC_FORMAT = "\n%(levelname)s:%(name)s:%(message)s"

class TableHandlerDB():

    def __init__(self, getter_service:IGetterService):
        self.getter_service:IGetterService = getter_service
        
        self.collection_name:str = "table_handler_test"
        self.collection:Collection = mongo_conn[self.collection_name]


    def create_tab(self, link_id:Union[ObjectId, str]) -> dict | None:
        link_id = ObjectId(link_id) if type(link_id) != type(ObjectId) else link_id

        get_text = self.__get_link_data(link_id)["text"]
        get_notes = self.__get_link_data(link_id)["notes"]
        note_ids = []
        for id in get_notes:
            note_ids.append(id)

        if len(get_text) or len(get_notes) == 0:
            return None

        data = {
            "content": {
                "text": get_text,
                "notes": get_notes # A list of notes
            },
            "changes": {
                "changed": False,
                "text":{
                    "changed":False,
                    "change_scripts": []
                    },
                "notes":{
                    "changed":False,
                    "change_scripts": []
                    }
            },
            "last_view": current_date()
        }

        data_id = self.collection.insert_one(data).inserted_id
        if data_id is None:
            return
        
        return {**data, "_id":data_id}
    

    def delete_tab(self, link_tab:ObjectId, with_changes:bool=False) -> dict|None:
        filter = str({"_id":link_tab})
        query_tab = self.collection.find_one(filter)
        if query_tab == None:
            return
        
        if query_tab["changes"]["changed"]:
            if with_changes:
                self.collection.delete_one(filter, comment="tab register deleted")

        return query_tab
    

    def __get_link_data(self, link_id:str) -> dict:
        link_data = self.getter_service.get_link_data(link_id)
        if link_data == None:
            return None

        text_data = self.getter_service.get_text_data(link_data["text_id"])
        notes_data = self.getter_service.get_notes_data(link_data["note_ids"])
        if text_data == None or len(notes_data) == 0:
            return None
 
        res = dict()
        res["link_id"] = link_id
        res["text"] = text_data
        res["notes"] = notes_data
        return res
