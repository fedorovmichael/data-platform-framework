from pyspark.sql import DataFrame

from app.sinks.sink_base import Sink, WriteMode
from app.credentials.dataclasses.postgres_credentials import PostgresCredentials

class SinkSparkPostgres(Sink[DataFrame]):
    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        table: str,
        credentials: PostgresCredentials,
        mode: str = "append",
    ) -> None:
        self._host = host
        self._port = port
        self._database = database
        self._table = table
        self._credentials = credentials
        self._mode = WriteMode(mode)

    def write(self, data: DataFrame) -> None:
        (
            data.write
            .format("jdbc")
            .mode(self._mode)
            .option("url", f"jdbc:postgresql://{self._host}:{self._port}/{self._database}")
            .option("dbtable", self._table)
            .option("user", self._credentials.user)
            .option("password", self._credentials.password)
            .option("driver", "org.postgresql.Driver")
            .save()
        )
