from app.transformers.upper_case_name_transformer import UpperCaseNameTransformer
from app.transformers.composite_transformer import CompositeTransformer

TRANSFORMER_REGISTRY = {
    "spark_upper_username": UpperCaseNameTransformer,
    "spark_user_composit_transformer": CompositeTransformer,
}
