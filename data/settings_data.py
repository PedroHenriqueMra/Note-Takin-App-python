from dataclasses import dataclass, field
import time
from typing import Any, Optional
from bson.objectid import ObjectId


@dataclass
class Settings():

    SETTINGS_NAME:str = "default_settings"
    
    AUTO_SAVE:bool = False

    FONT_SIZE:int = 16

    FONT_FAMILY:str = "arial"
    
    @property
    def __SETTINGS(self) -> dict:
        settings = dict()
        valid_attr = [x for x in self.__class__.__dict__.keys() if x.isupper()]

        for attr in valid_attr:
            if hasattr(self, attr):
                value = getattr(self, attr)
                settings[attr] = value

        return settings

    def get_settings(self):
        return self.__SETTINGS

    # methods
    def get_dict_structure(self):
        return {
            "SETTINGS_NAME":self.__SETTINGS["SETTINGS_NAME"],
            "AUTO_SAVE":self.__SETTINGS["AUTO_SAVE"],
            "interface": {
                "FONT_SIZE": self.__SETTINGS["FONT_SIZE"],
                "FONT_FAMILY": self.__SETTINGS["FONT_FAMILY"]
            }
        }
    
    def change_property(self, prop:str, value:Any) -> bool:
        if not hasattr(self, prop):
            print("It's not a property")
            return False

        current_prop = self.__SETTINGS[prop]

        if type(current_prop) != type(value):
            print("Invalid type")
            return False

        # atualize prop value in __SETTINGS property
        self.__SETTINGS[prop] = value
        # change value property
        setattr(self, prop, value)

        # print("Prop changed successfuly")
        return True

    @classmethod
    def parse(cls, object:dict) -> Optional['Settings']:
        # To filter object keys for to get only class attributes
        object_keys = [o for o in object.keys() if hasattr(cls, o)]
        # To filter in class dict to get only attributes necessary
        cls_attr = [c for c in cls.__dict__.keys() if c.isupper() and hasattr(cls, c)]

        new_obj = Settings()
        for key_obj in object_keys:
            if key_obj not in cls_attr:
                print(f"{key_obj} property not exists in Settings")
                return None
            
            if not new_obj.change_property(key_obj, object[key_obj]):
                print("An error ocurred while changed property!")
                return None

        # print("Item parsed successfuly")
        return new_obj
