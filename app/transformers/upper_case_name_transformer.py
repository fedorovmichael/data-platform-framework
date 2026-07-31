from .transform_base import Transformer
from pyspark.sql import DataFrame
from pyspark.sql.functions import upper, col

class UpperCaseNameTransformer(Transformer[DataFrame, DataFrame]):

    def transform(self, data: DataFrame) -> DataFrame:
        if "username" not in data.columns:
            raise ValueError(f"Column 'username' does not exist in input data frame.")

        return data.withColumn("username", upper(col("username")))
