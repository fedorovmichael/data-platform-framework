from unittest.mock import MagicMock, patch

import os
import pytest
import psycopg

from pyspark.sql import SparkSession
from uuid import uuid4
from dotenv import load_dotenv
from app.execution.execution_context import ExecutionContext
from app.sinks.sink_postgres import SinkSparkPostgres
from app.sources.postgres_spark_source import PostgresCredentials

load_dotenv()

_host = os.environ["POSTGRES_TEST_HOST"]
_port = int(os.getenv("POSTGRES_TEST_PORT", "5432"))
_dbname = os.environ["POSTGRES_TEST_DB"]
_user = os.environ["POSTGRES_TEST_USER"]
_password = os.environ["POSTGRES_TEST_PASSWORD"]


@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder.master("local[2]")
        .appName("SparkTest")
        .config(
            "spark.jars.packages",
            ",".join(
                [
                    "org.postgresql:postgresql:42.7.8",
                    "org.apache.hadoop:hadoop-aws:3.5.0",
                ]
            ),
        )
        .getOrCreate()
    )
    yield spark

    spark.stop()


@pytest.fixture
def mocked_spark():
    with patch("app.runtime.spark_runtime.SparkSession") as mock_spark_session:
        spark = MagicMock()

        (
            mock_spark_session.builder.master.return_value.appName.return_value.config.return_value.getOrCreate.return_value
        ) = spark

        yield spark


@pytest.fixture
def spark_context(spark):
    context = ExecutionContext(
        execution_id=str(uuid4()),
        resources={
            "spark": spark,
        },
    )

    yield context


@pytest.fixture
def postgres_test_table():
    conn = psycopg.connect(
        host=_host,
        port=_port,
        dbname=_dbname,
        user=_user,
        password=_password,
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE integration_test_users (
                    id INTEGER PRIMARY KEY,
                    username VARCHAR(100),
                    email VARCHAR(255)
                )
            """)

            cursor.executemany(
                """
                INSERT INTO integration_test_users
                    (id, username, email)
                VALUES (%s, %s, %s)
                """,
                [
                    (1, "Alice", "alice@example.com"),
                    (2, "Bob", "bob@example.com"),
                ],
            )
        conn.commit()
        yield "integration_test_users", conn

    finally:
        conn.rollback()

        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS integration_test_users")

        conn.commit()
        conn.close()


@pytest.fixture
def postgres_sink():
    def create_sink(mode: str = "append") -> SinkSparkPostgres:
        return SinkSparkPostgres(
            host=_host,
            port=_port,
            database=_dbname,
            table="integration_test_users",
            credentials=PostgresCredentials(_user, _password),
            mode=mode,
        )

    return create_sink
