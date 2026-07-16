from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TIn = TypeVar("TIn")
TOut = TypeVar("TOut")


class Transformer(ABC, Generic[TIn], Generic[TOut]):
    """Base contract for all transformations"""

    @abstractmethod
    def transform(self, data: TIn) -> Generic[TOut]:
        """Transform data and return generic TOut"""
        ...
