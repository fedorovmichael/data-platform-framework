from app.sources.source_base import Source
from pyspark.sql import SparkSession, DataFrame


class CsvSparkSource(Source):

    def read(self, spark: SparkSession, csv_path: str) -> DataFrame:
        if spark is None:
            return

        df = spark.read.csv(csv_path, header=True, inferSchema=True)
        return df
