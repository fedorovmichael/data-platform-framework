from collections.abc import Mapping
from typing import Any, TypeVar
from enum import Enum

from app.pipeline.pipeline import Pipeline

from app.registry import (
    SINK_REGISTRY,
    SOURCE_REGISTRY,
    VALIDATOR_REGISTRY,
    TRANSFORMER_REGISTRY,
)

T = TypeVar("T")


class PipelineBuilder:
    @staticmethod
    def _build_component(
        component_config: dict[str, Any],
        registry: Mapping[str, type[T]],
        component_name: str,
    ) -> T:
        component_type = component_config.get("type")
        if not isinstance(component_type, str) or not component_type:
            raise ValueError(
                f"{component_name} configuration must contain a non-empty 'type'."
            )

        component_class = registry.get(component_type)
        if component_class is None:
            raise ValueError(f"Unknown {component_name} type '{component_type}'.")

        options = component_config.get("options", {})
        if not isinstance(options, dict):
            raise ValueError(f"{component_name} options must be an object.")

        return component_class(**options)

    def build(self, config: dict[str, Any]) -> Pipeline:
        source = self._build_component(config["source"], SOURCE_REGISTRY, "source")

        validator = self._build_component(
            config["validator"], VALIDATOR_REGISTRY, "validator"
        )

        transformer = self._build_component(
            config["transformation"], TRANSFORMER_REGISTRY, "transformation"
        )

        sink = self._build_component(config["sink"], SINK_REGISTRY, "sink")

        return Pipeline(
            source=source, validator=validator, transformer=transformer, sink=sink
        )
