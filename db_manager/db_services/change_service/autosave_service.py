import threading
from utils.get_change import Differ

from time import sleep
from db_manager.db_services.change_service.change_service import ChangeService


class AutoSaveService(ChangeService):
    def __init__(self, delay:float=4.0):
        self.delay = delay

        self.__run_timer()

    def reset_timer(self):
        
        self.__run_timer()

    def __run_timer(self) -> None:
        while True:
            sleep(self.delay)
            try:
                oldcontent = self.__get_oldContent()
                newContent = self.__get_newContent()

                dff = Differ(oldcontent, newContent)
                change_list = dff.get_changeObjects()
                if change_list is not None:
                    for change in change_list:
                        self.include_query(change)

                    self.save()
            except Exception:
                return



    def __get_newContent(self) -> str:
        pass

    def __get_oldContent(self) -> str:
        oldcontent = None
        if "text" in self.tab_opened:
            oldcontent =  self.table_data["content"]["text"]["content"]
        else:
            for note in self.table_data["content"]["notes"]:
                if note["id"] == self.tab_opened["note"]:
                    oldcontent = note["content"]

        if oldcontent is None:
            raise Exception()

        return oldcontent
