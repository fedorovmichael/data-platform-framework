from typing import Generic, TypeVar

from app.sources.source_base import Source
from app.validators.validator_base import Validator, ValidationResult
from app.transformers.transform_base import Transformer
from app.sinks.sink_base import Sink

T = TypeVar("T")


class Pipeline(Generic[T]):
    def __init__(
        self,
        source: Source[T],
        validator: Validator[T],
        transformer: Transformer[T],
        sink: Sink[T],
    ):
        self.source = source
        self.validator = validator
        self.transformer = transformer
        self.sink = sink

    def run(self) -> None:
        source_result = self.source.read()

        validation_result: ValidationResult = self.validator.validate(source_result)
        if not validation_result.is_valid:
            raise ValueError(f"Validation errors: {validation_result.errors}")

        transform_result = self.transformer.transform(source_result)
        self.sink.write(transform_result)
