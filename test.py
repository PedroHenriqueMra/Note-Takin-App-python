import unittest

from tests.test_nosql_system import TestSettingsDB
from tests.test_utils import TestUtils
from tests.test_sql_system import TestTextTable
from tests.test_sql_system import TestNoteTable
from tests.test_sql_system import TestLinkTable


def suite():
    suite = unittest.TestSuite()

    # utils test functions
    # suite.addTest(TestUtils("test_get_path_of_a_key"))

    # sql test functions
    # suite.addTest()

    # no-sql test functions
    # suite.addTest(TestSettingsDB("create_sett"))
    suite.addTest(TestSettingsDB("to_list"))
    suite.addTest(TestSettingsDB("test_edit_settings_data_in_db"))

    # contracts tests
    # suite.addTest()
    
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
