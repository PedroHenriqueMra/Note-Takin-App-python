import unittest

from utils.find_dict import get_dict_path_by_key


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.hard_test = {
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
        self.real_test = {
            "SETTINGS_NAME":"default_name",
            "AUTO_SAVE":False,
            "interface": {
                "FONT_SIZE": 16,
                "FONT_FAMILY": "arial"
            }
        }

    def test_get_path_of_a_key(self):
        # tests to hard_test:
        # expected_res1 = {'family':{'children':{'kid2':{'favorit_things':{'blah_test':'blah'}}}}}
        # expected_res2 = {'family':{'children':{'kid1':'age'}}}
        # expected_res3 = {'family':{'children':{'kid1':{'favorit_things':'watch'}}}}
        # tests to real_tests:
        expected_res1 = {'interface':'FONT_SIZE'}
       
        found_key = "FONT_SIZE"

        call = get_dict_path_by_key(self.hard_test, found_key)
        call = next(call)
        
        self.assertEqual(call, expected_res1)
