from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any

Record = dict[str, Any]

class SourceBase(ABC):
    @abstractmethod
    def read(self) -> Iterable[Record]:
        pass