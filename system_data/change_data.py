from abc import ABC, abstractmethod
from exceptions.invalid_type import InvalidTypeException


class Change(ABC):
    table_type:str
    table_id:int
    change_starts:int
    change_ends:int

    @property
    def table_type(self):
        if self.table_type not in ["text", "note"]:
            raise InvalidTypeException(f"The type ({self.table_type}) is not allowed!.")
        return self.table_type
    
    @abstractmethod
    def gen_change_script(self) -> str:
        pass

class ChangeDelete(Change):
    def gen_change_script(self) -> str:
        self.change_starts
        query = f"""UPDATE {self.table_type}
                   SET content =
                   CASE
                        WHEN {self.change_starts} == 0 THEN
                            SUBSTR(content, {self.change_ends+1})
                        ELSE
                            SUBSTR(content, 1, {self.change_starts-1}) || SUBSTR(content, {self.change_ends+1})
                   END
                   WHERE id = {self.table_id}
                   )"""
        return query 

class ChangeUpdate(Change):
    def gen_change_script(self) -> str:
        self.change_starts += 1
        return "UPDATE {} SET content = substring(content, )".format()




class ChangeInsert(Change):
    def gen_change_script(self) -> str:
        pass
