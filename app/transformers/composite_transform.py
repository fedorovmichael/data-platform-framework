from pyspark.sql import DataFrame
from .transform_base import Transformer 
from typing import TypeVar

T = TypeVar("T")


class CompositeTransform(Transformer[DataFrame, DataFrame]):
    def __init__(self, transformers: list[Transformer[DataFrame, DataFrame]]) -> None:
        self.transformers = transformers

    def transform(self, data: DataFrame) -> DataFrame:

        result = data

        for transformer in self.transformers:
            result = transformer.transform(data)

        return result 