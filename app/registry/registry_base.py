from typing import Generic, TypeVar

T = TypeVar("T")


class EntityRegistry(Generic[T]):
    def __init__(self) -> None:
        self._entities: dict[str, type[T]] = {}

    def register(self, name: str, entity: type[T]) -> None:
        if name in self._entities:
            raise ValueError(f"Entity '{name}' is already registered")
        self._entities[name] = entity

    def get(self, name: str) -> type[T]:
        if name not in self._entities:
            raise ValueError(f"Unknown registry entity '{name}'")
        return self._entities[name]

    def create(self, name: str, **kwargs) -> T:
        entity_class = self.get(name)
        return entity_class(**kwargs)
