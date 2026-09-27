from .registry_base import EntityRegistry
from app.transformers.transform_base import Transformer

from app.transformers.upper_case_name_transformer import UpperCaseNameTransformer
from app.transformers.composite_transformer import CompositeTransformer
from app.transformers.select_columns_transformer import SelectColumnsTransform
from app.transformers.filter_rows_transformer import FilterRowsTransform

transformer_registry = EntityRegistry[Transformer]()
transformer_registry.register("spark_upper_username", UpperCaseNameTransformer)
transformer_registry.register("spark_select_columns", SelectColumnsTransform)
transformer_registry.register("spark_filter_rows", FilterRowsTransform)

TRANSFORMER_REGISTRY = {
    "spark_upper_username": UpperCaseNameTransformer,
    "spark_user_composit_transformer": CompositeTransformer,
}
