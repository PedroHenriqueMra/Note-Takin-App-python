import unittest

from data.settings_data import Settings
from data.SQL_table_data import *
from utils.find_dict import find_first_key

from db_manager.repository.NoSQL_layer.config_db import ConfigDB

from db_manager.repository.SQL_layer.note_db import ADMNote
from db_manager.repository.SQL_layer.text_db import ADMText
from db_manager.repository.SQL_layer.link_handler import ADMLink

from bson.objectid import ObjectId


# class TestSqlHandlers(unittest.TestCase):
#     def setUp(self):
#         self.text = ADMText
#         self.note = ADMNote
#         self.link = ADMLink

class SettingsHandlerTest(unittest.TestCase):
    def setUp(self):
        self.config = ConfigDB()

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
    
    def find(self, id):
        find = self.config.find_settings(id)
        self.assertIsNotNone(find, "Config not found!")
        return find
    
    def test_edit_sett(self):
        # 
        # print("Old values:")
        self.to_list('678ea169bf26f99b897d822f')

        # find set
        id = '678ea169bf26f99b897d822f'
        print(f"Id = {id}")

        # edit settings
        new_values = {"SETTINGS_NAME":"New change", "AUTO_SAVE":True, "FONT_SIZE":22}
        self.config.edit_settings(id, new_values)
        
        print("new values:")
        self.to_list('678ea169bf26f99b897d822f')

class UtilsFunctionsTest(unittest.TestCase):
    def setUp(self):
        self.dict_test = {
            "id": "ABCABC",
            "name": "lorem",
            "family": {
                "wife": "she",
                "children": {
                    "kid1": {
                        "name":"eldest son",
                        "age": 12,
                        "favorit_things": {
                            "food":["apple", "hamburger"],
                            "play":["football"],
                            "watch":["mickey"],
                        }
                    },
                    "kid2": {
                        "name":"youngest son",
                        "age": 8,
                        "favorit_things": {
                            "food":["chocolate", "fries"],
                            "play":["volleyball"],
                            "watch":["cartoon"],
                            "kid2_preference": "handbal today",
                            "blah_test": {
                                "blah": "blah"
                            }
                        }
                    }
                }
            },
            "job": {
                "prinipal_work": "programmer",
                "secundary_work": "driver"
            }
        }

    def test_get_target_path_of_a_dict_find_first_key(self):
        expected_res = "{'family':{'children':{'kid2':{'favorite_things':{'blah_test':'blah'}}}}}"
        param = "blah"

        call = find_first_key(self.dict_test, param)
        print(next(call))
        # self.assertEqual(call, expected_res)



if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(UtilsFunctionsTest("test_get_target_path_of_a_dict_find_first_key"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
    # unittest.main(argv=['-v', 'UtilsFunctionsTest.test_get_target_path_of_a_dict_find_first_key'])





# {
#     "id": "ABCABC",
#     "name": "lorem",
#     "family": {
#         "wife": "she",
#         "children": {
#             "kid1": {
#                 "name":"eldest son",
#                 "age": 12,
#                 "favorit_things": {
#                     "food":["apple", "hamburger"],
#                     "play":["football"],
#                     "watch":["mickey"],
#                 }
#             },
#             "kid2": {
#                 "name":"youngest son",
#                 "age": 8,
#                 "favorit_things": {
#                     "food":["chocolate", "fries"],
#                     "play":["volleyball"],
#                     "watch":["cartoon"],
#                     "kid2_preference": "handbal today"
#                 }
#             }
#         }
#     }
# }

