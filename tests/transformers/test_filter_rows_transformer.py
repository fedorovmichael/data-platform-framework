import pytest

from app.transformers.filter_rows_transformer import FilterRowsTransform


def test_filter_rows(spark):

    df = spark.createDataFrame(
        [
            (1, "alice", "alice@test.com"),
            (2, "bob", "bob@test.com"),
            (3, "charlie", "charlie@test.com"),
        ],
        ["id", "username", "email"],
    )

    transformer = FilterRowsTransform("id > 1")

    transformer_result = transformer.transform(df)

    assert [row.id for row in transformer_result.orderBy("id").collect()] == [2, 3]


def test_filter_rows_rejects_empty_condition():

    with pytest.raises(ValueError, match="Filter condition cannot be empty"):
        FilterRowsTransform(condition="")
