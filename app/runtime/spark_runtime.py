from app.runtime.runtime_base import Runtime
from pyspark.sql import SparkSession


class SparkRuntime(Runtime):
    def __init__(self):
        self.spark: SparkSession | None = None

    def start(
        self, app_name: str = "SparkRuntime", master: str = "local[*]"
    ) -> SparkSession:
        self.spark = SparkSession.builder.master(master).appName(app_name).getOrCreate()
        return self.spark

    def stop(self) -> None:
        if self.spark is not None:
            self.spark.stop()
            self.spark = None
