from app.transformers.transform_base import Transformer
from pyspark.sql import DataFrame
from collections.abc import Sequence


class SelectColumnsTransform(Transformer[DataFrame, DataFrame]):
    def __init__(self, columns: Sequence[str]):

        if columns is None or len(columns) == 0:
            raise ValueError("Columns can not be empty.")

        self._columns = tuple(columns)

    def transform(self, data: DataFrame) -> DataFrame:
        df = data.select(*self._columns)
        return df
