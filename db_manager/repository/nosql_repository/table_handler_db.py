from typing import Union
from db_manager.connections.mgdb_connection import mongo_conn

from pymongo.collection import Collection
from bson.objectid import ObjectId

from db_manager.repository.db_services.IGetterService import IGetterService


class TableHandlerDB:

    def __init__(self, getter_service:IGetterService):
        self.getter_service:IGetterService = getter_service
        
        self.collection_name:str = "table_handler_test"
        self.collection:Collection = mongo_conn[self.collection_name]


    def create_data(self, link_id:Union[ObjectId, str]) -> dict | None:
        link_id = ObjectId(link_id) if type(link_id) != type(ObjectId) else link_id

        get_text_id = self.__get_link_data(link_id)["text_id"]
        get_note_ids = self.__get_link_data(link_id)["note_ids"]

        if len(get_text_id) or len(get_note_ids) == 0:
            return

        data = {
            "open":True,
            "changed":False,
            "text_id":get_text_id,
            "note_ids": [n for n in get_note_ids]
        }
        data_id = self.collection.insert_one(data)
        if data_id is None:
            return
        
        return {**data, "_id":data_id}
        

    def close(self, link_tab:ObjectId) -> None:
        update = str({"open":False})
        self.collection.update_one({"_id":link_tab}, {"$set": update})

    def __delete_tab(self):
        pass

    def save_text_changes(self, text_id:int):
        if self.__text_was_changed(text_id):
            # save logic
            pass


    def save_note_changes(self, note_id:int):
        if self.__note_was_changed(note_id):
            # save logic
            pass

    def save_all(self, link_id:ObjectId) -> None:
        text_id = self.__get_link_data(link_id)["text"]["id"]
        self.save_text_changes(text_id)

        note_ids = self.__get_link_data(link_id)["notes"]["id"]
        for id in note_ids:
            self.save_note_changes(id)



    def __get_link_data(self, link_id:str) -> dict:
        link_data = self.getter_service.get_link_data(link_id)
        if link_data == None:
            return None

        text_data = self.getter_service.get_text_data(link_data["text_id"])
        notes_data = self.getter_service.get_notes_data(link_data["note_ids"])
        if text_data == None or notes_data == None:
            return None
 
        res = dict()
        res["link_id"] = link_id
        res["text"] = text_data
        res["notes"] = notes_data
        return res
        


    def __text_was_changed(self, text_id:int) -> bool:
        pass

    def __note_was_changed(self, note_id:int) -> bool:
        pass
