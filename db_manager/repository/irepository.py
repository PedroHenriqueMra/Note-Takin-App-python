from abc import ABC, abstractmethod

class IRepository[T](ABC):
    @abstractmethod
    def add(self, values:T) -> T:
        raise NotImplemented()

    @abstractmethod
    def get_by_id(self, id:int) -> T:
        raise NotImplemented()
    
    @abstractmethod
    def remove_by_id(self, id:int) -> str:
        raise NotImplemented()
