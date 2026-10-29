from abc import ABC, abstractmethod
from pyspark.sql import SparkSession

class SparkConfigurator(ABC):
    @abstractmethod
    def configure(self, spark: SparkSession) -> None: ...
