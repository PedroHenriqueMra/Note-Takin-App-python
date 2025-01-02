from abc import ABC, abstractmethod

class IRepository(ABC):
    
    def __init__(self):
        self.__create_table()

    @abstractmethod
    def __create_table(self):
        pass

    @abstractmethod
    def add(self, content:dict) -> str:
        pass

    @abstractmethod
    def remove(self, id) -> str:
        pass

    @abstractmethod
    def get_by_id(self, id) -> str:
        pass
