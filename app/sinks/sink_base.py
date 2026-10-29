from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from enum import Enum

T = TypeVar("T")


class Sink(ABC, Generic[T]):
    """Base contract for all sinks"""

    @abstractmethod
    def write(self, data: T) -> None:
        """Persist data to the configured destination."""
        ...

class WriteMode(str, Enum):
    APPEND = "append"
    OVERWRITE = "overwrite"
    IGNORE = "ignore"
    ERROR_IF_EXISTS = "errorifexists"

