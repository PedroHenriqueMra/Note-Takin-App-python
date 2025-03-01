import unittest
from utils.date_now import current_date
import pprint

from db_manager.db_services.change_service.change_service import ChangeService

from system_data.sql_tables_data import Text, Note
from system_data.change_data import ChangeDelete
from system_data.change_data import ChangeUpdate
from system_data.change_data import ChangeInsert

from db_manager.connections.sqlite_connection import sqlite
from db_manager.repository.sql_repository.link_handler import ADMLink
from db_manager.repository.sql_repository.text_db import ADMText
from db_manager.repository.sql_repository.note_db import ADMNote

class TestChangeService(unittest.TestCase):
    def setUp(self):
        table_data = {
            "content": {
                "text": Text("title_test", "content that will be changed"),
                "notes": [Note(1, "ref_lorem",None),Note(1, "ref_lorem",None),Note(1, "ref_lorem",None)]
            },
            "changes": {
                "changed": False,
                "text":{
                    "changed":False,
                    "change_scripts": []
                    },
                "notes": [
                    {"id":1,"changed":False,"change_scripts":[]},
                    {"id":1,"changed":False,"change_scripts":[]},
                    {"id":1,"changed":False,"change_scripts":[]}
                ]
            },
            "last_view": current_date()
        }
        
        self.service = ChangeService("table_id")
        self.service.table_data = table_data

    def test_include_query_text_field(self):
        text_change_insert = ChangeInsert("text", 1, new_content=".This is my new content!")
        text_change_update = ChangeUpdate("text", 1, 1, 7, "(The 'content' text was changed!)")
        text_change_delete = ChangeDelete("text", 1, 33,  40)

        action = self.service.include_query(text_change_insert)
        action + self.service.include_query(text_change_update)
        action + self.service.include_query(text_change_delete)

        self.assertEqual(action[0].gen_change_script(), text_change_insert.gen_change_script())
        self.assertEqual(action[1].gen_change_script(), text_change_update.gen_change_script())
        self.assertEqual(action[2].gen_change_script(), text_change_delete.gen_change_script())
        print(f"TABLE DATA FROM TEXT TEST:")
        print(pprint.pprint(self.service.table_data))


    def test_include_query_note_field(self):
        note_change_insert = ChangeInsert("note", 1, "This is a note!")
        note_change_update = ChangeUpdate("note", 1, 1, 5, "I changed this content!")
        note_change_delete = ChangeDelete("note", 1, 1, 3)

        action = self.service.include_query(note_change_insert)
        action + self.service.include_query(note_change_update)
        action + self.service.include_query(note_change_delete)

        self.assertEqual(action[0].gen_change_script(), note_change_insert.gen_change_script())
        self.assertEqual(action[1].gen_change_script(), note_change_update.gen_change_script())
        self.assertEqual(action[2].gen_change_script(), note_change_delete.gen_change_script())
        print(f"TABLE DATA FROM NOTES TEST:")
        print(pprint.pprint(self.service.table_data))

    def test_replace_script(self):
        note_test = Note(1, "test", "Text that will be changed. Lorem Lorem Lorem")
        self.service.table_data["content"]["notes"].append(note_test)
        note_test_structure = {"id":2,"changed":False,"change_scripts":[]}
        self.service.table_data["changes"]["notes"].append(note_test_structure)

        change_1 = ChangeUpdate("note", 2, 1, 4, "!changed1!")
        change_2 = ChangeUpdate("note", 2, 1, 9, "!changed2!")
        change_3 = ChangeUpdate("note", 2, 1, 12, "!changed3!")
        change_4 = ChangeUpdate("note", 2, 1, 15, "!changed4!")
        change_5 = ChangeUpdate("note", 2, 1, 20, "!changed5!")

        self.service.include_query(change_1)
        self.service.include_query(change_2)
        self.service.include_query(change_3)
        self.service.include_query(change_4)
        action = self.service.include_query(change_5)

        print(f"ACTION (replace_test):\n{action}")
        print(f"DATA STRUCTURE (replace_script):")
        print(pprint.pprint(self.service.table_data))
        print(f"ACCTION (replace_script):\n{action}")
        
        self.assertEqual(len(action), 1)
        self.assertEqual(action[0], change_5)

    def test_save_all(self):
        # self.configure_fakeData()
        txt_change = ChangeInsert("text", 1, "this is the new content for text from save_all test")
        note_change = ChangeDelete("note", 1, 1, 10)

        script_list_txt = self.service.include_query(txt_change)
        sript_list_note = self.service.include_query(note_change)

        print(f"script_list (note): {sript_list_note}")
        print(f"script_list (txt): {script_list_txt}")

        self.service.save()

        with sqlite.db_connection() as cur:
            print("TEXT CONTENT:")
            print(cur.execute("SELECT * FROM text WHERE id=?", (1,)).fetchone()["content"])
            print("NOTE CONTENT:")
            print(cur.execute("SELECT * FROM note WHERE id=?", (1,)).fetchone()["content"])

        print("STRUCTURE TABLE DATA:")
        pprint.pprint(self.service.table_data)

    def test_save_one(self):
        # self.configure_fakeData()
        txt_change = ChangeUpdate("text", 1, 1, 10, "This content was changed by save_one test.")
        note_change = ChangeInsert("note", 1, "This content wont be inluded, cause the note record wont be saved.")

        script_list_txt = self.service.include_query(txt_change)
        sript_list_note = self.service.include_query(note_change)

        print(f"script_list (note): {sript_list_note}")
        print(f"script_list (txt): {script_list_txt}")

        self.service.save_one()

        with sqlite.db_connection() as cur:
            print("TEXT CONTENT:")
            print(cur.execute("SELECT * FROM text WHERE id=?", (1,)).fetchone()["content"])
            print("NOTE CONTENT:")
            print(cur.execute("SELECT * FROM note WHERE id=?", (1,)).fetchone()["content"])

        print("STRUCTURE TABLE DATA:")
        pprint.pprint(self.service.table_data)

    
    def configure_fakeData(self):
        admlink = ADMLink()
        admtext = ADMText()
        admnote = ADMNote()

        txt = admtext.add_row(Text("title_test", "content for text test..."))
        note = admnote.add_row(Note(1, "reference for text 1...", "content for this note..."))

        self.service.table_data["content"]["text"] = txt
        self.service.table_data["content"]["notes"] = [note]
        self.service.table_data["changes"]["notes"] = [{"id":1,"changed":False,"change_scripts":[]}]
