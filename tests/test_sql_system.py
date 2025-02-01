import unittest

from system_data.sql_tables_data import *

from db_manager.repository.sql_repository.note_db import ADMNote
from db_manager.repository.sql_repository.text_db import ADMText
from db_manager.repository.sql_repository.link_handler import ADMLink

class TestTextTable(unittest.TestCase):
        text:ADMText = ADMText()

        def setUp(self):
                self.new_register = Text("aleatory_title__", "lalalallala")

        def test_add_row(self):
                new_reg = self.new_register
                expected_value = Text(title=new_reg.title, content=new_reg.content)

                # after do mock!
                action = self.text.add_row(new_reg)

                self.assertIsInstance(action, Text)
                self.assertEqual(action.title, expected_value.title)
                self.assertEqual(action.content, expected_value.content)

        def test_get_row(self):
                id = 1
                title = ""
                content = ""
                expected_value = Text(title=title, content=content)

                action = self.text.get_row(id)

                self.assertIsInstance(action, Text)
                self.assertEqual(action.title, expected_value.title)
                self.assertEqual(action.content, expected_value.content)

        def test_delete(self):
                id = 1
                action = self.text.delete(id)
                self.assertIs(action)



class TestNoteTable(unittest.TestCase):
        note = ADMNote()

        def setUp(self):
                self.new_register = Note("asdasdad", "lolalssas")

        def create_register(self):
                register = self.note.add_row(self.new_register)
                if register:
                        print(f"new note register = {register}")
                        return register



class TestLinkTable(unittest.TestCase):
        link = ADMLink()

        def setUp(self):
                self.new_register = Link(1, 1)

        def create_register(self):
                register = self.link.add_row(self.new_register)
                if register:
                        print(f"new link register = {register}")
                        return register
