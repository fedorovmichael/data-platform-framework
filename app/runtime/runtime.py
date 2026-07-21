from abc import ABC, abstractmethod

class Runtime(ABC):

    @abstractmethod
    def start(self) -> None:
        ...

    @abstractmethod
    def stop(self) -> None:
        ...
    
