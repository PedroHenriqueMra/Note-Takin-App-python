from ...connection.mgdb_connection import mongo_database
from typing import Optional, Union
from pydantic import BaseModel
from bson.objectid import ObjectId


class ConfigDB(BaseModel):

    database_name:str = "config"
    
    def __init__(self):
        with mongo_database.context_database() as db:
            database = db[self.database_name]
            if database.find_one() == None:
                self.create_settings()
        

    def get_all_settings(self) -> list:
        with mongo_database.context_database() as db:
            database = db[self.database_name]
            settings = list()
            for sett in database.find():
                settings.append(sett)

            if len(settings) == 0:
                settings = self.create_settings()
            
            return settings
        
    def find_settings(self, id:Union[str, ObjectId]) -> Optional[dict]:
        with mongo_database.context_database() as db:
            database = db[self.database_name]
            id = ObjectId(id) if type(id) != ObjectId else id
            
            return database.find_one({"_id": id})
        
    def create_settings(self) -> dict:
        with mongo_database.context_database() as db:
            database = db[self.database_name]

            structure = {
                "name_settings":"new_settings",
                "auto-save":False,
                "interface": {
                    "font-size":"16",
                    "font-family": "arial",
                }
            }
            structure_inserted = database.insert_one(structure)
            return {**structure, "_id": structure_inserted.inserted_id}

    def edit_settings() -> dict:
        pass
