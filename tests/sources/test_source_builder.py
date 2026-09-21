import pytest

from app.sources.source_builder import SourceBuilder
from app.sources.csv_spark_source import CsvSparkSource


def test_return_source():
    config = {
              "type": "csv_spark", 
              "options": {"path": "data/users.csv"}
              }

    source = SourceBuilder()
    result = source.build(config)

    assert isinstance(result, CsvSparkSource)


def test_source_wrong_name():
    config = {
        "type": "csv_spark1",
        "options": {"path": "data/users.csv"}
    }

    source = SourceBuilder()
    with pytest.raises(ValueError, match="Unknown registry entity 'csv_spark1'"):
        source.build(config)


def test_source_empty_config():
    config = {}

    source = SourceBuilder()
    with pytest.raises(ValueError, match="Source must be configured."):
        source.build(config)
