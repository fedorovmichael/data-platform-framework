from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Sink(ABC, Generic[T]):
    """Base contract for all sinks"""

    @abstractmethod
    def write(self, data: T) -> None:
        """Persist data to the configured destination."""
        ...
