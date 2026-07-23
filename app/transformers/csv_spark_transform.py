from app.transformers.transform_base import Transformer
from pyspark.sql import DataFrame


class CsvSparkTransform(Transformer[DataFrame, DataFrame]):
    def __init__(self, dfIn: DataFrame):
        self.dfIn = dfIn

    def transform(self) -> DataFrame:
       df = self.dfIn 

       return df