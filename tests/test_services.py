import unittest
from db_manager.repository.db_services.sql_getter import DataGetter

class TestGetterSqlData(unittest.TestCase):
    service = DataGetter()

    def test_get_link_data(self):
        id = "f504a5cd-2fd7-46f1-91ac-dc5c4dbb81df"
        expected_value = {
            "id":"",
            "text_id":"",
            "note_ids":""
        }

        action = self.service.get_link_data(id)

        print(f"link structure >> {action}")


    def test_get_text_data(self):
        id = 1
        expected_value = {}

        action = self.service.get_text_data(id)

        print(f"text structure >> {action}")


    def test_get_note_data(self):
        id = 1
        expected_value = {}

        action = self.service.get_note_data(id)

        print(f"text structure >> {action}")

    def test_get_allnotes_data(self):
            id = [1,2,3]
            expected_value = {1: {'type': 'note', 'reference': 'aleatory_title', 'content': 'NoteNoteNote', 'create_date': '2025-01-29 17:56:47', 'edit_date': '2025-01-29 17:56:47'},
            2: {'type': 'note', 'reference': 'alalla', 'content': 'plyusplus', 'create_date': '2025-01-29 18:25:02', 'edit_date': '2025-01-29 18:25:02'},
            3: {'type': 'note', 'reference': 'asdasdad', 'content': 'lolalssas', 'create_date': '2025-01-29 18:25:11', 'edit_date': '2025-01-29 18:25:11'}}

            action = self.service.get_all_notes(id)

            self.assertEqual(action, expected_value)

            for key, val in action.items():
                print()
                print(f"{key}: {val}")
