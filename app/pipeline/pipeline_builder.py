from typing import Any

from app.pipeline.pipeline import Pipeline
from app.execution.pipeline_execution import PipelineExecution
from app.validators.validator_builder import ValidatorBuilder
from app.sources.source_builder import SourceBuilder
from app.sinks.sink_builder import SinkBuilder
from app.transformers.transform_builder import TransformBuilder
from app.runtime.runtime_builder import RuntimeBuilder


class PipelineBuilder:
    def __init__(self) -> None:
        self.validator_builder = ValidatorBuilder()
        self.source_builder = SourceBuilder()
        self.sink_builder = SinkBuilder()
        self.transform_builder = TransformBuilder()
        self.runtime_builder = RuntimeBuilder()

    def build(self, name: str, config: dict[str, Any]) -> PipelineExecution:
        runtime = self.runtime_builder.build(config.get("runtime"))

        source = self.source_builder.build(config.get("source"))

        validator = self.validator_builder.build(config.get("validators", []))

        transformer = self.transform_builder.build(config.get("transformation", []))

        sink = self.sink_builder.build(config.get("sink"))

        pipeline = Pipeline(
            source=source, validator=validator, transformer=transformer, sink=sink
        )

        return PipelineExecution(name=name, runtime=runtime, pipeline=pipeline)
