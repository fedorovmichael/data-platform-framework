import pytest

from app.sinks.sink_builder import SinkBuilder
from app.sinks.sink_parquet import SinkParquet


def test_return_sink():
    config = {"type": "parquet", "options": {"path": "data/output/users.parquet"}}

    sink = SinkBuilder()
    result = sink.build(config)

    assert isinstance(result, SinkParquet)


def test_sink_wrong_name():
    config = {"type": "parquet1", "options": {"path": "data/output/users.parquet"}}

    sink = SinkBuilder()
    with pytest.raises(ValueError, match="Unknown registry entity 'parquet1'"):
        sink.build(config)


def test_sink_empty_config():
    config = {}

    sink = SinkBuilder()
    with pytest.raises(ValueError, match="Sink must be configured."):
        sink.build(config)
