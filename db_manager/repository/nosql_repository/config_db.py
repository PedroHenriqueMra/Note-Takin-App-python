from db_manager.connections.mgdb_connection import mongo_conn
from system_data.settings_data import Settings
from typing import Any, Dict, Optional, Union
from utils.find_dict import find_keypath
# Get 'Database' type
from pymongo.database import Database
from pymongo.collection import Collection

from bson.objectid import ObjectId

import logging
logging.basicConfig(level=logging.INFO)

class ConfigDB:

    def __init__(self):
        self.collection_name:str = "config"
        self.collection:Collection = mongo_conn[self.collection_name]

        collection = self.collection
        if collection.find_one() == None:
            # Create initial settings
            self.create_default_settings()
        

    def get_all_settings(self) -> list:
        collection = self.collection
        settings = list()
        for sett in collection.find():
            settings.append(sett)

        if len(settings) == 0:
            settings = self.create_default_settings()
        
        return settings
        
    def find_settings(self, id:Union[str, ObjectId]) -> Optional[Settings]:
        collection = self.collection
        id = ObjectId(id) if type(id) != ObjectId else id
        
        find = collection.find_one({"_id": id})
        if find == None:
            return None

        find = Settings.parse(find)
        return find
        
    # Create a default settings
    def create_default_settings(self) -> dict:
        collection = self.collection

        settings = Settings()
        id = collection.insert_one(settings.get_dict_structure()).inserted_id
        return {**settings.get_dict_structure(), "_id":id}

    def edit_settings(self, settings_id:Union[str, ObjectId], new_settings:Dict[str, Any]) -> Settings:
        settings_id = ObjectId(settings_id) if type(settings_id) != type(ObjectId) else settings_id
        collection = self.collection
        
        # Get user data in db
        get_settings = collection.find_one({"_id":settings_id})
        if get_settings == None:
            return

        # Parse dict data to Settings data
        parsed_settings = Settings.parse(get_settings)
        if parsed_settings == None:
            return
        
        # logic to upadate data:
        for key_sett, val_sett in new_settings.items():
            
            if hasattr(Settings, key_sett):
                if parsed_settings.change_property(key_sett, val_sett):
                    key_path = find_keypath(
                        parsed_settings.get_dict_structure(),
                        key_sett)
                    filter = {"_id":settings_id}
                    new_value = {str(key_path):val_sett}

                    change = collection.update_one(filter, new_value, upsert=False)
                    if change != None:
                        logging.info(f"{key_sett} Modified successfuly")

        return parsed_settings
