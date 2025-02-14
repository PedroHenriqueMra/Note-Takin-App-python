import unittest
from unittest.mock import Mock 

from system_data.sql_tables_data import *

from db_manager.repository.sql_repository.note_db import ADMNote
from db_manager.repository.sql_repository.text_db import ADMText
from db_manager.repository.sql_repository.link_handler import ADMLink


class TestTextTable(unittest.TestCase):
        def setUp(self):
                self.text:ADMText = ADMText()
                self.new_register:Text = Text("testetstts", "etetaetdad")

        def test_add_row(self):
                new_reg = self.new_register

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
        def setUp(self):
                self.note:ADMNote = ADMNote()
                self.new_register:Note = Note(1, "note_0303030", "lolalssas")

        def test_add_row(self):
                new_reg = self.new_register

                action = self.note.add_row(1, new_reg)
                self.assertIsInstance(action, Note)

        def test_get_row(self):
                id = 1
                action = self.note.get_row(id)
                self.assertIsInstance(action, Note)

        def test_delete_note(self):
                id = 3
                action = self.note.delete(id)
                self.assertTrue(action)



class TestLinkTable(unittest.TestCase):
        def setUp(self):
                self.link:ADMLink = ADMLink()
                self.new_register:Link = Link(1, 1)

        def create_register(self):
                new_reg = self.new_register

                action = self.link.add_row(1, new_reg)
                self.assertIsInstance(action, Link)

        def append_note(self):
                linked_text_id = 1
                note_id = 1

                action = self.link.append_note(linked_text_id, note_id)
                self.assertIsNone(action) # force error
                self.assertIsInstance(action, Note) # Greate result

        def remove_note(self):
                note_id = 1
                action = self.link.remove_note(note_id)
                self.assertIsNone(action)
