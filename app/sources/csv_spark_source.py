from pathlib import Path
from typing import cast

from pyspark.sql import SparkSession, DataFrame

from app.execution.execution_context import ExecutionContext
from app.sources.source_base import Source


class CsvSparkSource(Source[DataFrame]):
    def __init__(self, path: str) -> None:

        if path is None:
            raise ValueError("CSV path is required.")

        self.csv_path = Path(__file__).parent.parent.parent / path

    def read(self, context: ExecutionContext) -> DataFrame:
        path = str(self.csv_path)

        spark = cast(SparkSession, context.get_resource("spark"))

        return spark.read.csv(path, header=True, inferSchema=True)
