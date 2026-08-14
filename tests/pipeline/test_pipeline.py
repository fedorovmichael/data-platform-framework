from unittest.mock import MagicMock
import pytest

from app.pipeline.pipeline import Pipeline
from app.sources.source_base import Source
from app.validators.validator_base import Validator, ValidationResult, ValidationError
from app.transformers.transform_base import Transformer
from app.sinks.sink_base import Sink


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
            rule="id_not_null",
            message="ID cannot be null",
            row={"id":None}
        )
    )

    pipeline = Pipeline(
        source=source,
        validator=validator,
        transformer=transformer,
        sink=sink,
    )

    with pytest.raises(ValueError, match="Validation errors"):
        pipeline.run(spark_context)

    source.read.assert_called_once_with(spark_context)
    validator.validate.assert_called_once_with(source_data)

    transformer.transform.assert_not_called()
    sink.write.assert_not_called()
