from app.sinks.sink_base import Sink
from pyspark.sql import DataFrame


class SinkParquet(Sink[DataFrame]):
    def __init__(self, parquet_path: str) -> None:
        if not parquet_path:
            raise ValueError(f"Parquet save path does not valid.")

        self.parquet_path = parquet_path

    def write(self, data: DataFrame) -> None:
        data.write.parquet(self.parquet_path)