from app.sinks.sink_base import Sink
from pyspark.sql import DataFrame


class SinkParquet(Sink[DataFrame]):
    def __init__(self, path: str) -> None:
        if not isinstance(path, str) or not path.strip():
            raise ValueError(f"Parquet output path must be a non-empty string.")

        self.path = path

    def write(self, data: DataFrame) -> None:
        data.write.parquet(self.path)