from unittest.mock import MagicMock

from app.sources.postgres_spark_source import PostgresSparkSource, PostgresCredentials
from app.execution.execution_context import ExecutionContext
from pyspark.sql import DataFrame


def test_read_from_db_return_data_frame():
    spark = MagicMock()    
    expected_df = MagicMock(spec=DataFrame)

    reader = MagicMock()
    reader.format.return_value = reader
    reader.option.return_value = reader
    reader.load.return_value = expected_df

    spark.read = reader

    credentials = PostgresCredentials("test_user", "test_password")
    source = PostgresSparkSource(
        host="localhost",
        port=5432,
        database="db_de",
        table="users",
        credentials=credentials,
    )

    context = ExecutionContext(
        execution_id="test_execution_id",
        resources={"spark": spark},
    )

    result = source.read(context)

    assert result is expected_df
    reader.format.assert_called_once_with("jdbc") 
    reader.option.assert_any_call("url", "jdbc:postgresql://localhost:5432/db_de")
    reader.option.assert_any_call("dbtable", "users")
    reader.option.assert_any_call("user", "test_user")
    reader.option.assert_any_call("password", "test_password")
    reader.option.assert_any_call("driver", "org.postgresql.Driver")
    assert reader.option.call_count == 5
    reader.load.assert_called_once()