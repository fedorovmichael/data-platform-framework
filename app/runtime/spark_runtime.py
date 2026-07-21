from app.runtime.runtime import Runtime
from pyspark.sql import SparkSession

class SparkRuntime(Runtime):
    def __init__(self):
        self.spark = None

    def start(self, app_name:str = "SparkRuntime") -> SparkSession:
        self.spark = SparkSession.builder.appName(app_name).getOrCreate()
        return self.spark

    
    def stop(self):
        self.spark.stop()