from app.sources.source_base import Source
from pyspark.sql import SparkSession, DataFrame
from pathlib import Path
from app.runtime.spark_runtime import SparkRuntime


class CsvSparkSource(Source[DataFrame]):
    def __init__(self, path: str) -> None:

        if path is None:
            raise ValueError("CSV path is required.")

        spark = SparkRuntime()
        self.spark = spark.start()

        self.csv_path = Path(__file__).parent.parent.parent / path

    def read(self) -> DataFrame:
        path = str(self.csv_path)
        df = self.spark.read.csv(path, header=True, inferSchema=True)
        return df
