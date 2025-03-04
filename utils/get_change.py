from typing import List
from system_data.change_data import *


class Differ:
    def __init__(self, str_1:str, str_2:str):
        self.str_1:str = str_1
        self.str_2:str = str_2

    def get_changeObjects(self) -> List[Change]:
        if self.str_1 == self.str_2:
            return
        
        
        


    def __get_ChangeArea(self):
        pass

    def __get_object(self):
        pass

    def __compact(self) -> ChangeUpdate:
        pass

    
