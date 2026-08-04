import pytest
from app.pipeline.pipeline_builder import PipelineBuilder


class FakeSource:
    def __init__(self, path: str):
        self.path = path


def test_build_component_creates_registered_component():
    registry = {"fake_resource": FakeSource}

    component_config = {"type": "fake_resource", "options": {"path": "users.csv"}}

    component = PipelineBuilder._build_component(
        component_config=component_config,
        registry=registry,
        component_name="fake_resource",
    )

    assert isinstance(component, FakeSource)
    assert component.path == "users.csv"


def test_build_component_rejects_unknown_type():

    registry = {"fake_resource": FakeSource}

    component_config = {"type": "fake_resource1", "options": {"path": "users.csv"}}

    with pytest.raises(
        ValueError, match="Unknown fake_resource type 'fake_resource1'."
    ):
        PipelineBuilder._build_component(
            component_config=component_config,
            registry=registry,
            component_name="fake_resource",
        )


def test_build_component_rejects_invalid_options():

    registry = {"fake_resource": FakeSource}

    component_config = {"type": "fake_resource", "options": "path"}

    with pytest.raises(ValueError):
        PipelineBuilder._build_component(
            component_config=component_config,
            registry=registry,
            component_name="fake_resource",
        )


@pytest.mark.parametrize("component_type", [None, "", 123])
def test_build_component_rejects_invalid_type(component_type):
    registry = {"fake_source": FakeSource}

    component_config = {
        "type": component_type,
        "options": {
            "path": "users.csv",
        },
    }

    with pytest.raises(
        ValueError,
        match="source configuration must contain a non-empty 'type'",
    ):
        PipelineBuilder._build_component(
            component_config=component_config,
            registry=registry,
            component_name="source",
        )


def test_build_component_rejects_missing_type():
    component_config = {
        "options": {
            "path": "users.csv",
        },
    }

    with pytest.raises(
        ValueError,
        match="source configuration must contain a non-empty 'type'",
    ):
        PipelineBuilder._build_component(
            component_config=component_config,
            registry={"fake_source": FakeSource},
            component_name="source",
        )
