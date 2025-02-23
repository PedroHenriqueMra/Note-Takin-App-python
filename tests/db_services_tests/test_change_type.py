import unittest
from system_data.change_data import *
from exceptions.invalid_type import InvalidTableTypeException

class TestChangeData(unittest.TestCase):
    def setUp(self):
        self.table_type:str = "text"
        self.table_id:int = 1
        self.change_starts:int = 2
        self.change_ends:int = 4
        self.new_content:str = "new"

    def test_raise_exception(self):
        obj = ChangeInsert(self.table_type, self.table_id, self.change_starts, self.change_ends, self.new_content)
        
        with self.assertRaises((InvalidTableTypeException, AttributeError)):
            obj.table_type = "test" # there is not a 'test' table

    def test_date_type(self):
        obj = ChangeInsert(self.table_type, self.table_id, self.change_starts, self.change_ends, self.new_content)
        self.assertIsInstance(obj.table_type, str)
        self.assertIsInstance(obj.table_id, int)
        self.assertIsInstance(obj.change_starts, int)
        self.assertIsInstance(obj.change_ends, int)
        self.assertIsInstance(obj.newContent, str)
        

class TestChangeDeleteData(unittest.TestCase):
    def setUp(self):
        table_type = "text"
        table_id = 1
        change_starts = 2
        change_ends = 4
        self.change:ChangeDelete = ChangeDelete(table_type, table_id, change_starts, change_ends)

    def test_get_query(self):
        change = self.change
        query_expected = (f"""
        UPDATE {change.table_type}
        SET content =
            CASE
                WHEN {change.change_starts} = 0 THEN
                    SUBSTR(content, {change.change_ends+1})
                ELSE
                    SUBSTR(content, 1, {change.change_starts})|| SUBSTR(content, {change.change_ends+1})
            END
        WHERE id = ?""", (change.table_id,))
        get_query = self.change.gen_change_script()

        print(f"\nDelete script:\n{get_query[0]}\nExpected:\n{query_expected[0]}")
        self.assertEqual(get_query, query_expected)


class TestChangeUpdateData(unittest.TestCase):
    def setUp(self):
        table_type = "text"
        table_id = 1
        change_starts = 2
        change_ends = 4
        new_content = "new content"
        self.change:ChangeUpdate = ChangeUpdate(table_type, table_id, change_starts, change_ends, new_content)

    def test_get_query(self):
        change = self.change
        query_expected = (f"""
        UPDATE {change.table_type}
        SET content =
            CASE
                WHEN {change.change_starts} = 0 THEN
                    ? || SUBSTR(content, {change.change_ends+1})
                ELSE
                    SUBSTR(content, 1, {change.change_starts}) || ? || SUBSTR(content, {change.change_ends+1})
            END
        WHERE id = ?""", (change.newContent, change.newContent, change.table_id))
        get_query = self.change.gen_change_script()

        print(f"\nUpdate script:\n{get_query[0]}\nExpected:\n{query_expected[0]}")
        self.assertEqual(get_query, query_expected)


class TestChangeInsertData(unittest.TestCase):
    def setUp(self):
        table_type = "text"
        table_id = 1
        change_starts = 2
        change_ends = 4
        new_content = "new content"
        self.change:ChangeInsert = ChangeInsert(table_type, table_id, change_starts, change_ends, new_content)

    def test_get_query(self):
        change = self.change
        query_expected = f"INSERT INTO {change.table_type} (content) VALUES({change.newContent})"
        get_query = self.change.gen_change_script()

        print(f"\nInsert script:\n{get_query[0]}\nExpected:\n{query_expected[0]}")
        self.assertEqual(get_query, query_expected)


if __name__ == "__main__":
    unittest.main()
