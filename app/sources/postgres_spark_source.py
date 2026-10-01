from typing import cast
from pyspark.sql import DataFrame, SparkSession


from .source_base import Source
from app.credentials.dataclasses.postgres_credentials import PostgresCredentials
from app.execution.execution_context import ExecutionContext


class PostgresSparkSource(Source[DataFrame]):
    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        table: str,
        credentials: PostgresCredentials,
    ):
        self._host = host
        self._port = port
        self._database = database
        self._table = table
        self._credentials = credentials

    def read(self, context: ExecutionContext) -> DataFrame:
        spark = cast(SparkSession, context.get_resource("spark"))
        return spark.createDataFrame(
            [
                (1, "alice", "alice@test.com"),
                (2, "bob", "bob@test.com"),
                (3, "charlie", "charlie@test.com"),
            ],
            ["id", "username", "email"],
        )
