from app.transformers.transform_base import Transformer
from pyspark.sql import DataFrame
from collections.abc import Sequence


class SelectColumnsTransform(Transformer[DataFrame, DataFrame]):
    def __init__(self, columns: Sequence[str]) -> None:

        if not columns:
            raise ValueError("Columns cannot be empty.")

        self._columns = tuple(columns)

    def transform(self, data: DataFrame) -> DataFrame:
        return data.select(*self._columns)
