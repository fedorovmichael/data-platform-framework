import os

from app.sources.postgres_spark_source import PostgresSparkSource, PostgresCredentials
from app.execution.execution_context import ExecutionContext
from pyspark.sql import DataFrame


def test_postgres_source_reads_real_data(spark_context, postgres_test_table):

    credentials = PostgresCredentials(
        user=os.environ["POSTGRES_TEST_USER"],
        password=os.environ["POSTGRES_TEST_PASSWORD"],
    )

    source = PostgresSparkSource(
        host=os.environ["POSTGRES_TEST_HOST"],
        port=int(os.getenv("POSTGRES_TEST_PORT", "5432")),
        database=os.environ["POSTGRES_TEST_DB"],
        table=postgres_test_table,
        credentials=credentials,
    )

    df = source.read(spark_context)

    rows = df.orderBy("id").collect()

    assert df.columns == ["id", "username", "email"]
    assert len(rows) == 2
    assert rows[0].username == "Alice"
    assert rows[1].username == "Bob"
