import pytest
from app.pipeline.pipeline_builder import PipelineBuilder


class FakeSource:
    def __init__(self, path:str):
        self.path = path

def test_build_component_creates_registered_component():
    registry = {
        "fake_resource": FakeSource
    }

    component_config = {
        "type": "fake_resource",
        "options": { "path": "users.csv" }
    }

    component = PipelineBuilder._build_component(
        component_config=component_config,
        registry=registry,
        component_name="fake_resource"
    )

    assert isinstance(component, FakeSource)
    assert component.path == "users.csv"

def test_build_component_rejects_unknown_type():
    
    registry = {
        "fake_resource": FakeSource
    }

    component_config = {
        "type": "fake_resource1",
        "options": { "path": "users.csv" }
    }

    with pytest.raises(ValueError):
        component = PipelineBuilder._build_component(
            component_config=component_config,
            registry=registry,
            component_name="fake_resource"
        )


def test_build_component_rejects_invalid_options():

    registry = {
        "fake_resource": FakeSource
    }

    component_config = {
        "type": "fake_resource",
        "options": "path"
    }

    with pytest.raises(ValueError):
        component = PipelineBuilder._build_component(
            component_config=component_config,
            registry=registry,
            component_name="fake_resource"
        )


def test_build_component_passes_options_to_constructor():
    ...

