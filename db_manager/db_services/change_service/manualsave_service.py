from db_manager.db_services.change_service.change_service import ChangeService

from db_manager.connections.sqlite_connection import sqlite


class ChangeService(ChangeService):
    
    def save(self, note_id:int=None) -> None:
        self.__desableOne_changed_statment(note_id)
        self.__checkout_changedStatments()
        
        with sqlite.db_connection() as cur:
            if note_id == None:
                for scr_txt in self.table_data["changes"]["text"]["change_scripts"]:
                    script = scr_txt.gen_change_script()
                    cur.execute(script[0], script[1])
            else:
                notes = self.table_data["changes"]["notes"]
                for note in notes:
                    if note["id"] == note_id:
                        for note_src in notes["change_scripts"]:
                            script = note_src.gen_change_script()
                            cur.execute(script[0], script[1])

        self.__remove_scripts(note_id)

    def __remove_scripts(self, note_id:int|None=None, all:bool=False) -> None:
        if note_id == None or all:
            self.table_data["changes"]["text"]["change_scripts"] = []
            if not all:
                return
        
        for note in self.table_data["changes"]["notes"]:
            if note["id"] == note_id or all:
                note["change_scripts"] = []
    

    def __desableOne_changed_statment(self, note_id:int|None=None) -> None:
        if note_id is not None:
            notes = self.table_data["changes"]["notes"]
            for note in notes:
                if note["id"] == note_id:
                    note["changed"] = False
            return
        
        self.table_data["changes"]["text"]["changed"] = False


    def __checkout_changedStatments(self) -> None:
        notes = self.table_data["changes"]["notes"]
        for note in notes:
            if note["changed"] == True:
                return
        
        if self.table_data["changes"]["text"]["changed"] == False:
            self.table_data["changes"]["changed"] = False
