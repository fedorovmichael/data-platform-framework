from app.sources.source_base import Source
from pyspark.sql import SparkSession, DataFrame


class CsvSparkSource(Source[DataFrame]):
    def __init__(self, spark: SparkSession, csv_path: str) -> None:
        if spark is None:
            raise ValueError("SparkSession is required.")

        if csv_path is None:
            raise ValueError("CSV path is required.")

        self.spark = spark
        self.csv_path = csv_path

    def read(self) -> DataFrame:

        df = self.spark.read.csv(self.csv_path, header=True, inferSchema=True)
        return df
