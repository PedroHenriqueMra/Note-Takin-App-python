from abc import ABC, abstractmethod
from typing import Any, Optional

class IRepository[T](ABC):
    @abstractmethod
    def add_row(self, values:T) -> T:
        raise NotImplemented()

    @abstractmethod
    def get(self, id:int|str) -> Optional[T]:
        raise NotImplemented()
    
    @abstractmethod
    def delete(self, id:int|str) -> bool:
        raise NotImplemented()
    
    @abstractmethod
    def update(self, id:int|str, field:str, value:Any) -> Optional[T]:
        raise NotImplemented()
