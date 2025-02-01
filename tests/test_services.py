import unittest
from db_manager.repository.db_services.sql_getter import DataGetter

class TestGetterSqlData(unittest.TestCase):
    service = DataGetter()

    def test_getter_get_link_data(self):
        id = "f504a5cd-2fd7-46f1-91ac-dc5c4dbb81df"
        expected_value = {
            "link_id":"test",
            "text_id":"test",
            "note_ids":"test"
        }

        action = self.service.get_link_data(id)
        print("action")

        self.assertIsInstance(action, dict, "The function 'get_link_data' doens't return a dict type!")

        for key in action:
            self.assertIn(key, expected_value.keys(), f"The key {key} doesn't exist in action result")


    def test_get_text_data(self):
        id = 1
        expected_value = {}

        action = self.service.get_text_data(id)

        print(f"text structure >> {action}")


    def test_getter_get_notes_data(self):
        data_expected = {
            "id":"test",
            "type":"test",
            "reference":"test",
            "content":"test",
            "create_date":"test",
            "edit_date":"test"
        }
        ids = [1]

        action = self.service.get_notes_data(ids)
        print(action)
        
        self.assertIsInstance(action, list, "The function 'get_notes_data' doens't return a list type!")

        for dict in action:
            for key in dict:
                self.assertIn(key, data_expected.keys(), f"The key {key} required doens't exist in dict action: {dict}")


    def test_getter_get_text_data(self):
        data_expected = {
            "id":"test",
            "type":"test",
            "title":"test",
            "content":"test",
            "create_date":"test",
            "edit_date":"test"
        }
        id = 1

        action = self.service.get_text_data(id)
        print(action)
        
        self.assertIsInstance(action, dict, "The function 'get_text_data' doens't return a dict type!")

        for key in action:
            self.assertIn(key, data_expected.keys(), f"The key {key} doesn't exist in action result")
