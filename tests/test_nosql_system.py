import unittest

from system_data.settings_data import Settings
from db_manager.repository.nosql_repository_layer.config_db import ConfigDB

from bson.objectid import ObjectId


class TestSettingsDB(unittest.TestCase):
    config = ConfigDB()

    def to_list(self, id:ObjectId|str=None):
        try:
            list_itens = self.config.get_all_settings() if id == None else self.config.find_settings(id)

            for item in list_itens:
                print()
                if type(list_itens) == dict:
                    print(f"{item}: {list_itens[item]}")
                else:
                    print(item)
        except:
            print("Id nao encontrado")
            pass

    def create_sett(self):
        return self.config.create_settings()
    
    def test_edit_settings_data_in_db(self):
        # Get id
        id = '678ea169bf26f99b897d822f'
        print(f"Id = {id}")

        # get current settings
        current_sett = self.config.find_settings(id)
        self.assertIsNotNone(current_sett)
        print("old data:")
        print(current_sett.get_dict_structure())
        print()

        # get output values 
        new_values = {"SETTINGS_NAME":"TEStststasHHH.HHH", "AUTO_SAVE":False, "FONT_SIZE":16}
        expected_value = Settings(
            SETTINGS_NAME="Changeeed",
            AUTO_SAVE=True,
            FONT_SIZE=32,
            FONT_FAMILY=current_sett.FONT_FAMILY)


        # act:
        edited_data = self.config.edit_settings(id, new_values)
        self.assertEqual(edited_data, expected_value)
        
        print("new data:")
        print(edited_data.get_dict_structure())
