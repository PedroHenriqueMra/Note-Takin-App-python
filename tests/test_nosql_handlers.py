import unittest

from system_data.settings_data import Settings
from db_manager.repository.nosql_repository.config_db import ConfigDB

from bson.objectid import ObjectId

from db_manager.repository.db_services.sql_getter_service import DataGetter
from db_manager.repository.nosql_repository.table_handler_db import TableHandlerDB

class TestSettingsDB(unittest.TestCase):
    def setUp(self):
        self.config:ConfigDB = ConfigDB()
        self.id:str = '678e9030155b4d08703a5a82'

    def to_list(self):
        id = self.id
        # id = None

        if id != None:
            get_settings = self.config.find_settings(id)
            print()
            print(get_settings.get_dict_structure())
            return 
        
        for sett in self.config.get_all_settings():
            print("-" * 50)
            print(sett)

    def create_sett(self):
        return self.config.create_default_settings()
    
    def test_edit_settings_data_in_db(self):
        # Get id
        id = self.id
        print()
        print(f"Id = {id}")

        # get old settings (settings before edit)
        old_sett = self.config.find_settings(id)
        self.assertIsNotNone(old_sett)

        print("---- old settings: ----")
        print(old_sett.get_dict_structure())
        print()

        # get output values 
        new_values = {"SETTINGS_NAME":"newTestststyd", "AUTO_SAVE":True, "FONT_SIZE":18, "FONT_FAMILY": 'font-sans-serif'}
        expected_value = Settings(
            SETTINGS_NAME=new_values["SETTINGS_NAME"],
            AUTO_SAVE=new_values["AUTO_SAVE"],
            FONT_SIZE=new_values["FONT_SIZE"],
            FONT_FAMILY=new_values["FONT_FAMILY"])

        # action:
        edited_data = self.config.edit_settings(id, new_values)
        self.assertEqual(edited_data.get_dict_structure(), expected_value.get_dict_structure())
        
        print("---- new data: ----")
        print(self.config.find_settings(id).get_dict_structure())
