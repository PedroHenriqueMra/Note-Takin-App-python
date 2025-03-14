from ast import Dict
from typing import List
from system_data.change_data import *

import difflib


class Differ:
    def __init__(self, str_1:str, str_2:str, table_type:str, table_id:int):
        self.str_1:str = str_1
        self.str_2:str = str_2
        self.table_type:str = table_type
        self.table_id:int = table_id

    def get_changeObjects(self) -> List[Change]:
        if self.str_1 == self.str_2:
            return []
        
        changeInfo = self.__get_ChangeInfo()
        change_objects = list()
        for change_data in changeInfo:
            change_objects.append(self.__get_object(change_data))

        return change_objects
    

    def __get_ChangeInfo(self) -> list:
        diff = difflib.ndiff(self.str_1, self.str_2)
        data = list()
        change_starts = None
        new_content = ""
        last_signal = None
        change_type = None

        def create_object(end_index:int) -> None:
            nonlocal change_starts, new_content, change_type 
            if change_starts is not None:
                obj = {
                    "type": change_type,
                    "change_starts": change_starts,
                    "change_ends": end_index,
                }

                if change_type in ("insert", "update"):
                    obj["new_content"] = new_content

                data.append(obj)
                change_starts = None
                new_content = ""

        for i, dff in enumerate(diff):
            code = dff[0]
            char = dff[2]

            if code in ("+", "-"):
                if last_signal is None:
                    last_signal = code

                if last_signal is not None and code != last_signal:
                    create_object(i+1)

                if change_starts is None:
                    change_starts = i+1
                    if code == "+":
                        if i+1 > len(self.str_1):
                            change_type = "insert"
                        else:
                            change_type = "update"
                        new_content += char
                    else:
                        change_type = "delete"

                continue
            
            create_object(i+1)

        return data

    def __get_object(self, data:dict) -> Change:
        if data["type"] == "delete":
            return ChangeDelete(
                table_type=self.table_type,
                table_id=self.table_id,
                change_starts=data["change_starts"],
                change_ends=data["change_ends"]
            )
        elif data["type"] == "update":
            return ChangeUpdate(
                table_type=self.table_type,
                table_id=self.table_id,
                change_starts=data["change_starts"],
                change_ends=data["change_ends"],
                new_content=data["new_content"]
            )
        
        return ChangeInsert(
            table_type=self.table_type,
            table_id=self.table_id,
            new_content=data["new_content"]
        )

    def __compact(self) -> ChangeUpdate:
        pass
