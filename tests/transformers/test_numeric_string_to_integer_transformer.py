import pytest

from app.transformers.numeric_string_to_integer_transformer import (
    NumericStringToIntegerTransformer,
)


def test_numeric_string_is_transformed_to_integer():
    transformer = NumericStringToIntegerTransformer()
    result = transformer.transform("10")
    assert result == 10
    assert isinstance(result, int)


def test_non_numeric_string_raises_value_error():
    transformer = NumericStringToIntegerTransformer()
    with pytest.raises(ValueError):
        transformer.transform("not")
