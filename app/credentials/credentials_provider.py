from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class CredentialsProvider(ABC, Generic[T]):
    @abstractmethod
    def get(self) -> T: 
        ...
