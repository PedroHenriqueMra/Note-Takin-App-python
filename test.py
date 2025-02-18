import unittest
import glob
import os

from tests.repository_tests.test_nosql_handlers import TestSettingsDB
from tests.db_services_tests.test_getter_service import TestGetterSqlData
from tests.test_utils import TestUtils
from tests.repository_tests.test_sql_handlers import TestTextTable
from tests.repository_tests.test_sql_handlers import TestNoteTable
from tests.repository_tests.test_sql_handlers import TestLinkTable
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
    # suite.addTest(TestTextTable("test_delete_text"))
    # suite.addTest(TestTextTable("test_add_row"))
    
    # suite.addTest(TestNoteTable("test_add_row"))
    # suite.addTest(TestNoteTable("test_delete_note"))

    # suite.addTest(TestLinkTable("test_create_register"))

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


def suite_all(module=""):
    if module == "":
        dirs = [dir.path for dir in os.scandir(os.getcwd() + "\\tests") if dir.is_dir() and dir.name.endswith('_tests')]
        
        file_strings = [route for route in glob.glob(pathname="test_*", root_dir=os.getcwd() + "\\tests")]
        for dir in dirs:
            files = glob.glob(dir + "\\test_*.py")
            for f in files:
                file_strings.append(f)
        
        print(f"file_strings: {file_strings}")
        return [unittest.TestLoader().loadTestsFromName(str) for str in file_strings]
    
    files = [f for f in glob.glob(os.getcwd() + "\\tests" + f"\\{module}")]
    return [unittest.TestLoader().loadTestsFromName(str) for str in files]


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite())
    tests = suite_all()
    for test in tests:
        runner.run(test)
