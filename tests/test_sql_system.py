import unittest

from system_data.sql_tables_data import *

from db_manager.repository.sql_repository.note_db import ADMNote
from db_manager.repository.sql_repository.text_db import ADMText
from db_manager.repository.sql_repository.link_handler import ADMLink

class TestTextTable(unittest.TestCase):
        text = ADMText()

        def setUp(self):
                self.new_register = Text("aleatory_title", "LoreLoreLore")

        def create_register(self):
                register = self.text.add_row(self.new_register)
                if register:
                        print(f"new text register = {register}")
                        return register

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
