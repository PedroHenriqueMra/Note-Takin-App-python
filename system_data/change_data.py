from abc import ABC, abstractmethod
from exceptions.invalid_type import InvalidTableTypeException


class Change(ABC):
    def __init__(self, table_type:str, table_id:int, change_starts:int, change_ends:int):
        if self.table_type not in ["text", "note"]:
            raise InvalidTableTypeException(f"The type ({self.table_type}) is not allowed.")
        
        if self.change_ends <= self.change_starts:
            # invert values
            start = self.change_starts
            end = self.change_ends
            self.change_starts = end
            self.change_ends = start

        self.table_type:str = table_type
        self.table_id:int = table_id
        self.change_starts:int = change_starts
        self.change_ends:int = change_ends

    @abstractmethod
    def gen_change_script(self) -> str:
        pass

class ChangeDelete(Change):
    def gen_change_script(self) -> str:
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
        super().__init__(table_type, table_id, change_starts, change_ends)

    def gen_change_script(self) -> str:
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
        return query, (self.newContent, self.newContent, self.table_id)


class ChangeInsert(Change):
    def __init__(self, table_type:str, table_id:int, change_starts:int, change_ends:int, new_content:str):
        self.newContent:str = new_content
        super().__init__(table_type, table_id, change_starts, change_ends)

    def gen_change_script(self) -> str:
        query = "INSERT INTO {} (content) VALUES({})".format(self.table_type, self.newContent)
        return query
