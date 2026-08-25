import logging

from .pipeline_base import PipelineBase
from typing import Generic, TypeVar

from app.execution.execution_context import ExecutionContext
from app.sources.source_base import Source
from app.validators.validator_base import Validator
from app.transformers.transform_base import Transformer
from app.sinks.sink_base import Sink

TIn = TypeVar("TIn")
TOut = TypeVar("TOut")

logger = logging.getLogger(__name__)


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
        logger.info("execution_id=%s Source read started", context.execution_id)
        source_result = self.source.read(context)
        logger.info("execution_id=%s Source read completed", context.execution_id)

        logger.info("execution_id=%s Validation started", context.execution_id)
        validation_result = self.validator.validate(source_result)

        if not validation_result.is_valid:
            raise ValueError(
                f"Validation failed with: {len( validation_result.errors )} error(s)"
            )

        logger.info("execution_id=%s Validation completed", context.execution_id)

        logger.info("execution_id=%s Transformation started", context.execution_id)
        transform_result = self.transformer.transform(source_result)
        logger.info("execution_id=%s Transformation completed", context.execution_id)

        logger.info("execution_id=%s Sink started", context.execution_id)
        self.sink.write(transform_result)
        logger.info("execution_id=%s Sink completed", context.execution_id)
