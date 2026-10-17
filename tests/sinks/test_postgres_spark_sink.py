import pytest

from unittest.mock import MagicMock

from app.sources.postgres_spark_source import PostgresSparkSource, PostgresCredentials
from app.sinks.sink_postgres import SinkSparkPostgres
from app.execution.execution_context import ExecutionContext
from pyspark.sql import DataFrame


def test_read_from_data_frame_and_save_in_db():
    df = MagicMock(spec=DataFrame)

    writer = MagicMock()
    writer.format.return_value = writer
    writer.mode.return_value = writer
    writer.option.return_value = writer

    df.write = writer

    credentials = PostgresCredentials("test_user", "test_password")
    sink = SinkSparkPostgres(
        host="localhost",
        port=5432,
        database="db_de",
        table="users",
        credentials=credentials,
    )

    result = sink.write(df)

    assert result is None 
    writer.format.assert_called_once_with("jdbc") 
    writer.option.assert_any_call("url", "jdbc:postgresql://localhost:5432/db_de")
    writer.option.assert_any_call("dbtable", "users")
    writer.option.assert_any_call("user", "test_user")
    writer.option.assert_any_call("password", "test_password")
    writer.option.assert_any_call("driver", "org.postgresql.Driver")
    assert writer.option.call_count == 5
    writer.save.assert_called_once()


def test_invalid_write_mode_raises_value_error():
    credentials = PostgresCredentials("test_user", "test_password")

    with pytest.raises(ValueError):
        SinkSparkPostgres(
            host="localhost",
            port=5432,
            database="db_de",
            table="users",
            credentials=credentials,
            mode="mode"
        )

def test_write_failure_propagates_exception():
    df = MagicMock(spec=DataFrame)

    writer = MagicMock()
    writer.format.return_value = writer
    writer.mode.return_value = writer
    writer.option.return_value = writer
    writer.save.side_effect = RuntimeError("Write failed")

    df.write = writer

    credentials = PostgresCredentials("test_user", "test_password")
    sink = SinkSparkPostgres(
        host="localhost",
        port=5432,
        database="db_de",
        table="users",
        credentials=credentials,
    )

    with pytest.raises(RuntimeError, match="Write failed"):
        sink.write(df)

    writer.format.assert_called_once_with("jdbc") 
    writer.option.assert_any_call("url", "jdbc:postgresql://localhost:5432/db_de")
    writer.option.assert_any_call("dbtable", "users")
    writer.option.assert_any_call("user", "test_user")
    writer.option.assert_any_call("password", "test_password")
    writer.option.assert_any_call("driver", "org.postgresql.Driver")
    assert writer.option.call_count == 5
    writer.mode.assert_called_once_with("append")
    writer.save.assert_called_once()