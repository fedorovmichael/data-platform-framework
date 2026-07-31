from app.sinks.sink_base import Sink
from pyspark.sql import DataFrame
from pathlib import Path

class SinkParquet(Sink[DataFrame]):
    def __init__(self, path: str) -> None:
        if not isinstance(path, str) or not path.strip():
            raise ValueError(f"Parquet output path must be a non-empty string.")

        self.path = Path(__file__).parent.parent.parent / path

    def write(self, data: DataFrame) -> None:
        path = str(self.path)
        data.write.mode("overwrite").parquet(path)