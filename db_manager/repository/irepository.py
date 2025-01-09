from abc import ABC, abstractmethod
from typing import Optional

class IRepository[T](ABC):
    @abstractmethod
    def add_row(self, values:T) -> T:
        raise NotImplemented()

    @abstractmethod
    def get_by_id(self, id:int) -> Optional[T]:
        raise NotImplemented()
    
    @abstractmethod
    def delete_by_id(self, id:int|str) -> bool:
        raise NotImplemented()
