import unittest

from system_data.sql_tables_data import *

from db_manager.repository.sql_repository.note_db import ADMNote
from db_manager.repository.sql_repository.text_db import ADMText
from db_manager.repository.sql_repository.link_handler import ADMLink

class TestTextTable(unittest.TestCase):
        text:ADMText = ADMText()

        def setUp(self):
                self.new_register = Text("testetstts", "etetaetdad")

        def test_add_row(self):
                new_reg = self.new_register

                # then mock!
                action = self.text.add_row(new_reg)

                self.assertIsInstance(action, Text)

        def test_get_row(self):
                id = 1
                action = self.text.get_row(id)
                self.assertIsInstance(action, Text)

        def test_delete_text(self):
                id = 5
                action = self.text.delete(id)
                self.assertTrue(action)



class TestNoteTable(unittest.TestCase):
        note = ADMNote()

        def setUp(self):
                self.new_register = Note("note_0303030", "lolalssas")

        def test_add_row(self):
                new_reg = self.new_register

                # then mock!
                action = self.note.add_row(1, new_reg)
                self.assertIsInstance(action, Note)

        def test_delete_note(self):
                id = 3
                action = self.note.delete(id)



class TestLinkTable(unittest.TestCase):
        link = ADMLink()

        def setUp(self):
                self.new_register = Link(1, 1)

        def create_register(self):
                register = self.link.add_row(self.new_register)
                if register:
                        print(f"new link register = {register}")
                        return register
