import unittest

from tests.test_nosql_system import TestSettingsDB
from tests.test_services import TestGetterSqlData
from tests.test_utils import TestUtils
from tests.test_sql_system import TestTextTable
from tests.test_sql_system import TestNoteTable
from tests.test_sql_system import TestLinkTable
from tests.test_contracts import TestDataClasses


def suite():
    suite = unittest.TestSuite()

    # contracts tests
    # suite.addTest(TestDataClasses("test_settings_type"))
    # suite.addTest(TestDataClasses("test_text_type"))
    # suite.addTest(TestDataClasses("test_note_type"))
    # suite.addTest(TestDataClasses("test_link_type"))
    
    # utils test functions
    # suite.addTest(TestUtils("test_get_path_of_a_key"))

    # sql test functions
    # suite.addTest(TestTextTable("test_add_row"))
    suite.addTest(TestTextTable("test_delete"))
    # suite.addTest(TestNoteTable("test_add_row"))
    # suite.addTest(TestLinkTable("create_register"))

    # no-sql test functions
    ## config_db:
    # suite.addTest(TestSettingsDB("create_sett"))
    # suite.addTest(TestSettingsDB("to_list"))
    # suite.addTest(TestSettingsDB("test_edit_settings_data_in_db"))
    ## table_handler_db:
    

    # services:
    # suite.addTest(TestGetterSqlData("test_getter_get_link_data"))
    # suite.addTest(TestGetterSqlData("test_getter_get_text_data"))
    # suite.addTest(TestGetterSqlData("test_getter_get_notes_data"))
    

    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
