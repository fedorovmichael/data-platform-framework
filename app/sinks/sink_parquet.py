from pathlib import Path

from pyspark.sql import DataFrame

from app.sinks.sink_base import Sink


class SinkParquet(Sink[DataFrame]):
    def __init__(self, path: str) -> None:
        if not isinstance(path, str) or not path.strip():
            raise ValueError("Parquet output path must be a non-empty string.")

        self.path = Path(__file__).parent.parent.parent / path

    def write(self, data: DataFrame) -> None:
        data.write.mode("overwrite").parquet(str(self.path))

