import pytest

from app.transformers.transform_builder import TransformBuilder
from app.transformers.composite_transform import CompositeTransform
from app.transformers.select_columns_transformer import SelectColumnsTransform
from app.transformers.filter_rows_transformer import FilterRowsTransform


def test_retrieve_single_transformer():
    config = [
        {
            "type": "spark_select_columns",
            "options": {"columns": ["id", "username"]},
        }
    ]

    builder = TransformBuilder()
    result = builder.build(config)

    assert isinstance(result, SelectColumnsTransform)
    assert result._columns == ("id", "username")


def test_mulitple_config_transformer():

    config = [
        {
            "type": "spark_select_columns",
            "options": {"columns": ["id", "username"]},
        },
        {"type": "spark_filter_rows", "options": {"condition": "id > 1"}},
    ]

    builder = TransformBuilder()
    result = builder.build(config)

    assert isinstance(result, CompositeTransform)
    assert len(result.transformers) == 2
    assert isinstance(result.transformers[0], SelectColumnsTransform)
    assert isinstance(result.transformers[1], FilterRowsTransform)


def test_unknown_type_transformer():

    config = [
        {
            "type": "spark_select_columns1",
            "options": {"columns": ["id", "username"]},
        }
    ]

    builder = TransformBuilder()

    with pytest.raises(
        ValueError, match="Unknown registry entity 'spark_select_columns1'"
    ):
        builder.build(config)


def test_empty_list_transformers():

    config = []

    builder = TransformBuilder()

    with pytest.raises(ValueError, match="At least one transformer must be configured"):
        builder.build(config)
