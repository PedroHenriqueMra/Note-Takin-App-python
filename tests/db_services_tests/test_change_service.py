import unittest
from utils.date_now import current_date

from db_manager.db_services.change_service.change_service import ChangeService

from system_data.sql_tables_data import Text, Note
from system_data.change_data import ChangeDelete
from system_data.change_data import ChangeUpdate
from system_data.change_data import ChangeInsert

class TestChangeService(unittest.TestCase):
    def setUp(self):
        table_data = {
            "content": {
                "text": Text("title_test", "content that will be changed"),
                "notes": [Note(1, "ref_lorem"),Note(1, "ref_lorem"),Note(1, "ref_lorem")]
            },
            "changes": {
                "changed": False,
                "text":{
                    "changed":False,
                    "change_scripts": []
                    },
                "notes": [
                    {"id":1,"changed":False,"change_scripts":[]},
                    {"id":2,"changed":False,"change_scripts":[]},
                    {"id":3,"changed":False,"change_scripts":[]}
                ]
            },
            "last_view": current_date()
        }
        
        self.service = ChangeService("lorem")
        self.service.table_data = table_data

    def test_include_query_text_field(self):
        text_change_insert = ChangeInsert("text", 1, new_content=".This is my new content!")
        text_change_update = ChangeUpdate("text", 1, 1, 7, "(The 'content' text was changed!)")
        text_change_delete = ChangeDelete("text", 1, 33,  40)

        action = self.service.include_query(text_change_insert)
        action + self.service.include_query(text_change_update)
        action + self.service.include_query(text_change_delete)

        print(f"\nACTION (text): {action}")

        self.assertEqual(action[0], text_change_insert.gen_change_script())
        self.assertEqual(action[1], text_change_update.gen_change_script())
        self.assertEqual(action[2], text_change_delete.gen_change_script())

    def test_include_query_note_field(self):
        note_change_insert = ChangeInsert("note", 1, new_content=".This is a note!")
        note_change_update = ChangeUpdate("note", 1, 1, 5, "I changed this content!")
        note_change_delete = ChangeDelete("note", 1, 1, 3)

        action = self.service.include_query(note_change_insert)
        action + self.service.include_query(note_change_update)
        action + self.service.include_query(note_change_delete)

        print(f"\nACTION (note): {action}")

        self.assertEqual(action[0], note_change_insert.gen_change_script())
        self.assertEqual(action[1], note_change_update.gen_change_script())
        self.assertEqual(action[2], note_change_delete.gen_change_script())


    def test_save(self):
        pass
