from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Sink(ABC, Generic[T]):
    """Base contract for all sinks"""

    @abstractmethod
    def write(self, data: T) -> None:
        """Sink data to the target."""
        ...
