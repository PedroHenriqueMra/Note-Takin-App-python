from data.settings_data import Settings
from db_manager.connection.mgdb_connection import mongo_connection
from typing import Any, Dict, Optional, Union
from utils.find_dict import find_first_key
# Get 'Database' type
from pymongo.database import Database
from pymongo.collection import Collection

from bson.objectid import ObjectId


class ConfigDB:

    def __init__(self):
        # attrs
        self.collection_name:str = "config"
        self.connection:Database = mongo_connection
        self.collection:Collection = self.connection[self.collection_name]

        collection = self.collection
        if collection.find_one() == None:
            # Create initial settings
            self.create_settings()
        

    def get_all_settings(self) -> list:
        collection = self.collection
        settings = list()
        for sett in collection.find():
            settings.append(sett)

        if len(settings) == 0:
            settings = self.create_settings()
        
        return settings
        
    def find_settings(self, id:Union[str, ObjectId]) -> Optional[dict]:
        collection = self.collection
        id = ObjectId(id) if type(id) != ObjectId else id
        
        return collection.find_one({"_id": id})
        
    # Create a default settings
    def create_settings(self) -> dict:
        collection = self.collection

        settings = Settings()

        id = collection.insert_one(settings.get_dict_structure()).inserted_id

        return {**settings.get_dict_structure(), "_id":id}

    def edit_settings(self, settings_id:Union[str, ObjectId], new_settings:Dict[str, Any]) -> Settings:
        settings_id = ObjectId(settings_id) if type(settings_id) != ObjectId else settings_id

        collection = self.collection
        # Get user data in db
        get_settings = collection.find_one({"_id":settings_id})
        if get_settings == None:
            raise Exception(f"settings such id's {settings_id} not found")

        # Parse dict data to Settings data
        parsed_settings = Settings.parse(get_settings)
        if parsed_settings == None:
            raise Exception(f"Settings wasn't changed. Some object key was with wrong name!")
        
        # logic to upadate data:
        for key_sett in new_settings.keys():
            if key_sett in parsed_settings.get_settings().keys():
                val = new_settings[key_sett]

                if parsed_settings.change_property(key_sett, val):
                    filter = {"_id":settings_id}
                    key_path = find_first_key(parsed_settings.get_settings(), key_sett)
                    print(f"key path: {key_path}")
                    new_value = {"$set": {key_path:val}}
                    collection.update_one(filter, new_value)

        return parsed_settings
