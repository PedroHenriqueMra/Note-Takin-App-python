import unittest

from utils.find_dict import find_keypath
from utils.dictsetter import *


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
        # expected values to hard test:
        expected_hard_test1 = {'family': {'children': {'kid2': {'favorit_things':'kid2_preference'}}}} 
        expected_hard_test2 = {'family':{'children':{'kid1':'age'}}}
        expected_hard_test3 = {'family':{'children':{'kid1':{'favorit_things':'watch'}}}}
        
        # expected values to real tests:
        expected_real_test1 = "SETTINGS_NAME"
        expected_real_test2 = "AUTO_SAVE"
        expected_real_test3 = {'interface':'FONT_SIZE'}
        expected_real_test4 = {'interface':'FONT_FAMILY'}
       
        # hard test keys:
        hard_key1 = "kid2_preference"
        hard_key2 = "age"
        hard_key3 = "watch"

        # real test keys:
        real_key1 = "SETTINGS_NAME"
        real_key2 = "AUTO_SAVE"
        real_key3 = "FONT_SIZE"
        real_key4 = "FONT_FAMILY"

        # hard acts
        hard_call1 = find_keypath(self.hard_test, hard_key1)
        hard_call2 = find_keypath(self.hard_test, hard_key2)
        hard_call3 = find_keypath(self.hard_test, hard_key3)

        # real acts
        real_call1 = find_keypath(self.real_test, real_key1)
        real_call2 = find_keypath(self.real_test, real_key2)
        real_call3 = find_keypath(self.real_test, real_key3)
        real_call4 = find_keypath(self.real_test, real_key4)
        
        print() # print hard tests:
        print(f"(real test) Result test 1: {hard_call1}")
        print(f"(real test) Result test 2: {hard_call2}")
        print(f"(real test) Result test 3: {hard_call3}")
        print() # print real tests:
        print(f"(real test) Result test 1: {real_call1}")
        print(f"(real test) Result test 2: {real_call2}")
        print(f"(real test) Result test 3: {real_call3}")
        print(f"(real test) Result test 4: {real_call4}")
        
        # assert hard tests
        self.assertEqual(hard_call1, expected_hard_test1)
        self.assertEqual(hard_call2, expected_hard_test2)
        self.assertEqual(hard_call3, expected_hard_test3)
        # assert real tests
        self.assertEqual(real_call1, expected_real_test1)
        self.assertEqual(real_call2, expected_real_test2)
        self.assertEqual(real_call3, expected_real_test3)
        self.assertEqual(real_call4, expected_real_test4)

    def test_dict_getter(self):
        obj = {"l1":{"l2":{"l3":"value"}}}
        path = "l1/l2/l3"
        expected = {"l3":"value"}

        action = dictGetter(obj, path)
        print(f"\nDICT GETTER: {action}")

        self.assertEqual(action, expected)

    def test_dict_setter(self):
        obj = {"l1":{"l2":{"l3":{"l4":{"l5":"final_value"}}}}}
        path = "l1/l2/l3/l4/l5"
        value = "value_changed"
        expected = {"l1":{"l2":{"l3":{"l4":{"l5":"value_changed"}}}}}

        dictSetter(obj, path, value)
        print(f"\nDICT CHANGED: {obj}")

        self.assertEqual(obj, expected)
