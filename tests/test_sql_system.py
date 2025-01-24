import unittest

from system_data.sql_tables_data import *

from db_manager.repository.sql_repository_layer.note_db import ADMNote
from db_manager.repository.sql_repository_layer.text_db import ADMText
from db_manager.repository.sql_repository_layer.link_handler import ADMLink

class TestTextTable(unittest.TestCase):
        text = ADMText

class TestNoteTable(unittest.TestCase):
        note = ADMNote

class TestLinkTable(unittest.TestCase):
        link = ADMLink
