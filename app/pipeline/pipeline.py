import logging

from .pipeline_base import PipelineBase
from typing import Generic, TypeVar

from app.execution.execution_context import ExecutionContext
from app.sources.source_base import Source
from app.validators.validator_base import Validator
from app.transformers.transform_base import Transformer
from app.sinks.sink_base import Sink
from app.exceptions.execution_entity_error import ExecutionEntityError
from app.pipeline.pipeline_entity_types import PipelineEntityTypes

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
        try:
            logger.info("execution_id=%s Source read started", context.execution_id)
            source_result = self.source.read(context)
            logger.info("execution_id=%s Source read completed", context.execution_id)
        except Exception as e:
            raise ExecutionEntityError(
                PipelineEntityTypes.SOURCE.value,
                context.execution_id,
                "Source read failed",
                e,
            ) from e

        try:
            logger.info("execution_id=%s Validation started", context.execution_id)
            validation_result = self.validator.validate(source_result)
        except Exception as exc:
            raise ExecutionEntityError(
                PipelineEntityTypes.VALIDATOR.value,
                context.execution_id,
                "Validation failed",
                exc,
            ) from exc

        if not validation_result.is_valid:
            raise ValueError(
                f"Validation failed with: {len(validation_result.errors)} error(s)"
            )

        logger.info("execution_id=%s Validation completed", context.execution_id)

        try:    
            logger.info("execution_id=%s Transformation started", context.execution_id)
            transform_result = self.transformer.transform(source_result)
            logger.info("execution_id=%s Transformation completed", context.execution_id)
        except Exception as exc:
            raise ExecutionEntityError(
                PipelineEntityTypes.TRANSFORMER.value,
                context.execution_id,
                "Transformer failed",
                exc,
            ) from exc

        try:
            logger.info("execution_id=%s Sink started", context.execution_id)
            self.sink.write(transform_result)
            logger.info("execution_id=%s Sink completed", context.execution_id)
        except Exception as exc:
            raise ExecutionEntityError(
                PipelineEntityTypes.SINK.value,
                context.execution_id,
                "Sink failed",
                exc,
            ) from exc


