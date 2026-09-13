from typing import Generic, TypeVar

T = TypeVar("T")


class EntityRegistry(Generic[T]):
    def __init__(self) -> None:
        self._entities: dict[str, type[T]] = {}

    def register(self, name: str, entity: type[T]) -> None:
        self._entities[name] = entity

    def create(self, name: str, **kwargs) -> T:
        entity_class = self._entities[name]
        return entity_class(**kwargs)
