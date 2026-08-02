from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.execution.execution_context import ExecutionContext

T = TypeVar("T")


class Source(ABC, Generic[T]):
    """Base contract for all data sources."""

    @abstractmethod
    def read(self, context: ExecutionContext) -> T:
        """Read data from the source."""
        ...
