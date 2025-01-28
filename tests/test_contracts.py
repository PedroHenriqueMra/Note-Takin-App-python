import unittest
from uuid import uuid4

from system_data.settings_data import Settings
from system_data.sql_tables_data import Text
from system_data.sql_tables_data import Note
from system_data.sql_tables_data import Link


class TestDataClasses(unittest.TestCase):
    def setUp(self):
        # instances with required values
        self.settings = Settings()
        self.text = Text("",None)
        self.note = Note("",None)
        self.link = Link(0,0)
    
    def test_settings_type(self):
        self.assertEqual(self.settings.SETTINGS_NAME, "default_settings")
        self.assertEqual(self.settings.AUTO_SAVE, False)
        self.assertEqual(self.settings.FONT_SIZE, 16)
        self.assertEqual(self.settings.FONT_FAMILY, "arial")

        settings_property = {"SETTINGS_NAME":"default_settings","AUTO_SAVE":False,"FONT_SIZE":16,"FONT_FAMILY":"arial"}
        self.assertEqual(self.settings.get_settings(), settings_property)

        settings_dict_structure = {
            "SETTINGS_NAME":self.settings.SETTINGS_NAME,
            "AUTO_SAVE":self.settings.AUTO_SAVE,
            "interface": {
                "FONT_SIZE": self.settings.FONT_SIZE,
                "FONT_FAMILY": self.settings.FONT_FAMILY
            }
        }
        self.assertEqual(self.settings.get_dict_structure(), settings_dict_structure)

        # test change property method:
        change = self.settings.change_property("SETTINGS_NAME", "test_change")
        self.assertTrue(change)
        self.assertEqual(self.settings.SETTINGS_NAME, "test_change")

        # test parse method:
        object = {
            "SETTINGS_NAME":"test",
            "AUTO_SAVE":True,
            "interface": {
                "FONT_SIZE": 18,
                "FONT_FAMILY": "test"
            }
        }
        parsed_object = Settings.parse(object)
        print(parsed_object)
        self.assertIsInstance(parsed_object, Settings)

    def test_text_type(self):
        self.text.title = "test"
        self.text.content = "test"
        self.text.create_date = "test"
        self.text.edit_date = "test"
        self.text.type = "test"

    def test_note_type(self):
        self.note.reference = "test"
        self.note.content = "test"
        self.note.create_date = "test"
        self.note.edit_date = "test"
        self.note.type = "test"

    def test_link_type(self):
        self.link.text_id = 1
        self.link.note_id = 1
        self.link.id = uuid4()
