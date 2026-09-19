import pytest
from app.registry.registry_base import EntityRegistry


class FakeEntity:
    def __init__(self, value: str = "default") -> None:
        self.value = value

def test_register_and_create_entity():
    registry = EntityRegistry()

    registry.register("test", FakeEntity)
    result = registry.create("test")

    assert isinstance(result, FakeEntity)

def test_create_entity_with_constructor_arguments():
    registry = EntityRegistry()
    
    registry.register("test", FakeEntity)
    result = registry.create("test", value="Hello")

    assert result.value == "Hello"


def test_create_unknown_entity_raises_value_error():
    registry = EntityRegistry()
    
    registry.register("test", FakeEntity)

    with pytest.raises(ValueError, match="Unknown registry entity 'test1'"):
        registry.create("test1")
    

def test_register_duplicate_name_raises_value_error():
    registry = EntityRegistry()

    registry.register("test", FakeEntity)

    with pytest.raises(ValueError, match="Entity 'test' is already registered"):
        registry.register("test", FakeEntity)