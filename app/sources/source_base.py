from abc import ABC, abstractmethod
from typing import Generic, TypeVar 

T = TypeVar("T")
class Source(ABC, Generic[T]):
    """Base contract for all data sources."""
    
    @abstractmethod
    def read(self) -> T:
        """Read data from the source."""
        ...