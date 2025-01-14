import json
import unittest

from data.system_data import *
from db_manager.connection.sqlite_connection import db_connection
from db_manager.repository.SQL_layer.note_db import ADMNote
from db_manager.repository.SQL_layer.text_db import ADMText
from db_manager.repository.SQL_layer.link_handler import ADMLink

text = ADMText()
note = ADMNote()
link = ADMLink()
    

# newt = Text("texto 1", "loremlorem")
# text.add_row(newt)

# newn = Note("referencia tal", "lorelorelorelorelore")
# note.add_row(newn)

# newl = Link(2, 2)
# link.add_row(newl)

# # text.delete_by_id(1)
# ADMLink.delete_associations(2)


class TestStringMethods(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
