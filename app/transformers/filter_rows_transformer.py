from pyspark.sql import DataFrame

from .transform_base import Transformer

class FilterRowsTransform(Transformer[DataFrame, DataFrame]):
    def __init__(self, condition: str)-> None:

        if not condition:
          raise ValueError("Filter condition cannot be empty.")

        self._condition = condition

    def transform(self, data: DataFrame)-> DataFrame:
        return data.filter(self._condition) 