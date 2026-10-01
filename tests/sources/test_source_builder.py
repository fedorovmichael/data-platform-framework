import pytest

from app.sources.source_builder import SourceBuilder
from app.sources.csv_spark_source import CsvSparkSource
from app.sources.postgres_spark_source import PostgresSparkSource


def test_return_source():
    config = {"type": "csv_spark", "options": {"path": "data/users.csv"}}

    source = SourceBuilder()
    result = source.build(config)

    assert isinstance(result, CsvSparkSource)


def test_source_wrong_name():
    config = {"type": "csv_spark1", "options": {"path": "data/users.csv"}}

    source = SourceBuilder()
    with pytest.raises(ValueError, match="Unknown registry entity 'csv_spark1'"):
        source.build(config)


def test_source_empty_config():
    config = {}

    source = SourceBuilder()
    with pytest.raises(ValueError, match="Source must be configured."):
        source.build(config)


def test_source_orchestration_env(monkeypatch):
    monkeypatch.setenv("POSTGRES1_USER", "test_user")
    monkeypatch.setenv("POSTGRES1_PASSWORD", "test_password")

    config = {
        "type": "postgres_spark",
        "options": {
            "host": "localhost",
            "port": "5432",
            "database": "users_db",
            "table": "users_tbl",
            "credentials": {
                "provider": "env",
                "type": "postgres",
                "values": {"user": "POSTGRES1_USER", "password": "POSTGRES1_PASSWORD"},
            },
        },
    }

    source = SourceBuilder()
    result = source.build(config)

    assert isinstance(result, PostgresSparkSource)
    assert result._host == "localhost"
    assert result._port == "5432"
    assert result._database == "users_db"
    assert result._table == "users_tbl"
    assert result._credentials.user == "test_user"
    assert result._credentials.password == "test_password"
