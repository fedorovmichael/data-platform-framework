from unittest.mock import MagicMock
import pytest

from app.pipeline.pipeline import Pipeline
from app.sources.source_base import Source
from app.validators.validator_base import Validator, ValidationResult, ValidationError
from app.transformers.transform_base import Transformer
from app.sinks.sink_base import Sink
from app.exceptions.execution_entity_error import ExecutionEntityError
from app.pipeline.pipeline_entity_types import PipelineEntityTypes


def test_pipeline_runs_successfully(spark_context) -> None:

    source = MagicMock(spec=Source)
    validator = MagicMock(spec=Validator)
    transformer = MagicMock(spec=Transformer)
    sink = MagicMock(spec=Sink)

    source_data = [{"id": 1, "name": "Michael"}]
    transformed_data = [{"id": 1, "name": "MICHAEL"}]

    source.read.return_value = source_data
    validator.validate.return_value = ValidationResult.ok()
    transformer.transform.return_value = transformed_data

    pipeline = Pipeline(
        source=source,
        validator=validator,
        transformer=transformer,
        sink=sink,
    )

    pipeline.run(spark_context)

    source.read.assert_called_once_with(spark_context)
    validator.validate.assert_called_once_with(source_data)
    transformer.transform.assert_called_once_with(source_data)
    sink.write.assert_called_once_with(transformed_data)


def test_pipeline_stops_when_validation_fails(spark_context) -> None:

    source = MagicMock(spec=Source)
    validator = MagicMock(spec=Validator)
    transformer = MagicMock(spec=Transformer)
    sink = MagicMock(spec=Sink)

    source_data = [{"id": None}]

    source.read.return_value = source_data
    validator.validate.return_value = ValidationResult.fail(
        ValidationError(
            rule="id_not_null", message="ID cannot be null", row={"id": None}
        )
    )

    pipeline = Pipeline(
        source=source,
        validator=validator,
        transformer=transformer,
        sink=sink,
    )

    with pytest.raises(ValueError, match=r"Validation failed with: 1 error\(s\)"):
        pipeline.run(spark_context)

    source.read.assert_called_once_with(spark_context)
    validator.validate.assert_called_once_with(source_data)

    transformer.transform.assert_not_called()
    sink.write.assert_not_called()


def test_pipeline_source_execution_error(spark_context) -> None:

    source = MagicMock(spec=Source)
    validator = MagicMock(spec=Validator)
    transformer = MagicMock(spec=Transformer)
    sink = MagicMock(spec=Sink)

    source.read.side_effect = RuntimeError("Source read failed")

    pipeline = Pipeline(
        source=source,
        validator=validator,
        transformer=transformer,
        sink=sink,
    )

    with pytest.raises(ExecutionEntityError) as exc_info:
        pipeline.run(spark_context)

    error = exc_info.value

    assert error.entity_name == PipelineEntityTypes.SOURCE.value
    assert error.execution_id == spark_context.execution_id
    assert error.message == "Source read failed"
    assert isinstance(error.cause, RuntimeError)
    assert str(error.cause) == "Source read failed"
    assert error.__cause__ is error.cause
    validator.validate.assert_not_called()
    transformer.transform.assert_not_called()
    sink.write.assert_not_called()


def test_pipeline_validator_execution_error(spark_context) -> None:

    source = MagicMock(spec=Source)
    validator = MagicMock(spec=Validator)
    transformer = MagicMock(spec=Transformer)
    sink = MagicMock(spec=Sink)

    validator.validate.side_effect = RuntimeError("Validator validation failed")

    pipeline = Pipeline(
        source=source,
        validator=validator,
        transformer=transformer,
        sink=sink,
    )

    with pytest.raises(ExecutionEntityError) as exc_info:
        pipeline.run(spark_context)

    error = exc_info.value

    assert error.entity_name == PipelineEntityTypes.VALIDATOR.value
    assert error.execution_id == spark_context.execution_id
    assert error.message == "Validation failed"
    assert isinstance(error.cause, RuntimeError)
    assert str(error.cause) == "Validator validation failed"
    assert error.__cause__ is error.cause
    transformer.transform.assert_not_called()
    sink.write.assert_not_called()


def test_pipeline_transformer_execution_error(spark_context) -> None:

    source = MagicMock(spec=Source)
    validator = MagicMock(spec=Validator)
    transformer = MagicMock(spec=Transformer)
    sink = MagicMock(spec=Sink)

    transformer.transform.side_effect = RuntimeError("Transformer transform failed")

    pipeline = Pipeline(
        source=source,
        validator=validator,
        transformer=transformer,
        sink=sink,
    )

    with pytest.raises(ExecutionEntityError) as exc_info:
        pipeline.run(spark_context)

    error = exc_info.value

    assert error.entity_name == PipelineEntityTypes.TRANSFORMER.value
    assert error.execution_id == spark_context.execution_id
    assert error.message == "Transformer failed"
    assert isinstance(error.cause, RuntimeError)
    assert str(error.cause) == "Transformer transform failed"
    assert error.__cause__ is error.cause
    sink.write.assert_not_called()


def test_pipeline_sink_execution_error(spark_context) -> None:

    source = MagicMock(spec=Source)
    validator = MagicMock(spec=Validator)
    transformer = MagicMock(spec=Transformer)
    sink = MagicMock(spec=Sink)

    sink.write.side_effect = RuntimeError("Sink write failed")

    pipeline = Pipeline(
        source=source,
        validator=validator,
        transformer=transformer,
        sink=sink,
    )

    with pytest.raises(ExecutionEntityError) as exc_info:
        pipeline.run(spark_context)

    error = exc_info.value

    assert error.entity_name == PipelineEntityTypes.SINK.value
    assert error.execution_id == spark_context.execution_id
    assert error.message == "Sink failed"
    assert isinstance(error.cause, RuntimeError)
    assert str(error.cause) == "Sink write failed"
    assert error.__cause__ is error.cause
