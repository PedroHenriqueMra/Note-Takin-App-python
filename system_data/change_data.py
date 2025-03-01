from abc import ABC, abstractmethod
from exceptions.invalid_type import InvalidTableTypeException


class Change(ABC):
    def __init__(self, table_type:str, table_id:int):    
        self.__table_type:str = table_type
        self.table_id:int = table_id
        
        if self.__table_type not in ["text", "note"]:
            raise InvalidTableTypeException(f"The type ({self.table_type}) is not allowed.")

    @property
    def table_type(self) -> str:
        if self.__table_type not in ["text", "note"]:
            raise InvalidTableTypeException(f"The type ({self.table_type}) is not allowed.")
        
        return self.__table_type
    
    @table_type.setter
    def set_table_type(self, value:str) -> None:
        if self.table_type not in ["text", "note"]:
            raise InvalidTableTypeException(f"The type ({self.table_type}) is not allowed.")
        
        self.__table_type = value

    @abstractmethod
    def gen_change_script(self) -> tuple:
        pass

class ChangeDelete(Change):
    def __init__(self, table_type:str, table_id:int, change_starts:int, change_ends:int):
        self.change_starts:int = change_starts
        self.change_ends:int = change_ends

        if change_ends <= change_starts:
            # Invert values
            self.change_starts = change_ends
            self.change_ends = change_starts

        super().__init__(table_type, table_id)

    def gen_change_script(self) -> tuple:
        query = f"""
        UPDATE {self.table_type}
        SET content =
            CASE
                WHEN {self.change_starts} = 0 THEN
                    SUBSTR(content, {self.change_ends+1})
                ELSE
                    SUBSTR(content, 1, {self.change_starts})|| SUBSTR(content, {self.change_ends+1})
            END
        WHERE id = ?"""
        return query, (self.table_id,)

class ChangeUpdate(Change):
    def __init__(self, table_type:str, table_id:int, change_starts:int, change_ends:int, new_content:str):
        self.newContent:str = new_content
        self.change_starts:int = change_starts
        self.change_ends:int = change_ends
        if change_ends <= change_starts:
            # Invert values
            self.change_starts = change_ends
            self.change_ends = change_starts

        super().__init__(table_type, table_id)

    def gen_change_script(self) -> tuple:
        query = f"""
        UPDATE {self.table_type}
        SET content =
            CASE
                WHEN {self.change_starts} = 0 THEN
                    ? || SUBSTR(content, {self.change_ends+1})
                ELSE
                    SUBSTR(content, 1, {self.change_starts}) || ? || SUBSTR(content, {self.change_ends+1})
            END
        WHERE id = ?"""
        return query, (self.newContent, self.newContent, self.table_id,)

class ChangeInsert(Change):
    def __init__(self, table_type:str, table_id:int, new_content:str):
        self.newContent:str = new_content
        super().__init__(table_type, table_id)

    def gen_change_script(self) -> tuple:
        query = f"UPDATE {self.table_type} SET content = content || ?"
        return query, (self.newContent,)
