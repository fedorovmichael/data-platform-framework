from .pipeline_base import PipelineBase
from typing import Generic, TypeVar

from app.execution.execution_context import ExecutionContext
from app.sources.source_base import Source
from app.validators.validator_base import Validator, ValidationResult
from app.transformers.transform_base import Transformer
from app.sinks.sink_base import Sink

TIn = TypeVar("TIn")
TOut = TypeVar("TOut")


class Pipeline(PipelineBase, Generic[TIn, TOut]):
    def __init__(
        self,
        source: Source[TIn],
        validator: Validator[TIn],
        transformer: Transformer[TIn, TOut],
        sink: Sink[TOut],
    ) -> None:
        self.source = source
        self.validator = validator
        self.transformer = transformer
        self.sink = sink

    def run(self, context: ExecutionContext) -> None:
        source_result = self.source.read(context)

        validation_result = self.validator.validate(source_result)
        if not validation_result.is_valid:
            raise ValueError(f"Validation errors: {validation_result.errors}")

        transform_result = self.transformer.transform(source_result)
        self.sink.write(transform_result)
