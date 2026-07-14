from abc import ABC, abstractmethod
from typing import Generic, TypeVar 

T = TypeVar("T")
class Source(ABC, Generic[T]):
    @abstractmethod
    def read(self) -> T:
        pass