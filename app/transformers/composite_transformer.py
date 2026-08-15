from pyspark.sql import DataFrame

from .transform_base import Transformer
from .select_columns_transformer import SelectColumnsTransform
from .upper_case_name_transformer import UpperCaseNameTransformer
from .filter_rows_transformer import FilterRowsTransform


class CompositeTransformer(Transformer[DataFrame, DataFrame]):

    def transform(self, data: DataFrame) -> DataFrame:

        filter_rows = FilterRowsTransform("id > 1")
        result = filter_rows.transform(data)

        upper_case_name = UpperCaseNameTransformer()
        result = upper_case_name.transform(result)

        select_columns = SelectColumnsTransform(columns=["id", "username"])
        result = select_columns.transform(result)

        return result
