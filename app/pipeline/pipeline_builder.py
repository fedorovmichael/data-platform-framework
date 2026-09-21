from collections.abc import Mapping
from typing import Any, TypeVar

from app.pipeline.pipeline import Pipeline
from app.execution.pipeline_execution import PipelineExecution
from app.validators.validator_builder import ValidatorBuilder
from app.sources.source_builder import SourceBuilder

from app.registry import (
    SINK_REGISTRY,
    TRANSFORMER_REGISTRY,
    RUNTIME_REGISTRY,
)

T = TypeVar("T")


class PipelineBuilder:
    def __init__(self) -> None:
        self.validator_builder = ValidatorBuilder()
        self.source_builder = SourceBuilder()

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

    def build(self, name: str, config: dict[str, Any]) -> PipelineExecution:
        runtime = self._build_component(config["runtime"], RUNTIME_REGISTRY, "runtime")

        source = self.source_builder.build(config.get("source"))

        validator = self.validator_builder.build(config.get("validators", []))

        transformer = self._build_component(
            config["transformation"], TRANSFORMER_REGISTRY, "transformation"
        )

        sink = self._build_component(config["sink"], SINK_REGISTRY, "sink")

        pipeline = Pipeline(
            source=source, validator=validator, transformer=transformer, sink=sink
        )

        return PipelineExecution(name=name, runtime=runtime, pipeline=pipeline)
