import unittest

from utils.get_change import Differ

from system_data.change_data import Change
from system_data.change_data import ChangeDelete
from system_data.change_data import ChangeInsert
from system_data.change_data import ChangeUpdate

class TestGetChange(unittest.TestCase):
    def setUp(self):
        self.table_type = "text"
        self.table_id = 1

        str_1 = "Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem aaaaaaaaaaaaaaaaaaa"
        str_2 = "Lorem Lorem Lorem Lorem alalla Lorem Lorem Lorem Lorem Lorem"
        self.diff = Differ(str_1, str_2)

    def test_get_changeObjects(self):
        value_expected = [
            ChangeDelete(self.table_type, self.table_id, 1, 6),
            ChangeUpdate(self.table_type, self.table_id, 13, 26, ""),
            ChangeInsert(self.table_type, self.table_id, " Text-inserido")
        ]
        
        get_changeList = self.diff.get_changeObjects()
        # for expected, item in zip(value_expected, get_changeList):
        #     self.assertEqual(expected, item)
