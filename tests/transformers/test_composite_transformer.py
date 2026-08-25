import pytest
from pyspark.errors import AnalysisException

from app.transformers.composite_transformer import CompositeTransformer


def test_all_transformers_success(spark):
    data = [
        (1, "alice", "alice@example.com"),
        (2, "bob", "bob@example.com"),
        (3, "lee", "lee@example.com"),
    ]
    df = spark.createDataFrame(data, ["id", "username", "email"])

    transformer = CompositeTransformer()
    result = transformer.transform(df)

    rows = result.orderBy("id").collect()

    assert [row.id for row in rows] == [2, 3]
    assert [row.username for row in rows] == ["BOB", "LEE"]
    assert result.columns == ["id", "username"]


def test_composite_transformer_fails_when_username_missing(spark):
    data = [
        (1, "alice@example.com"),
        (2, "bob@example.com"),
    ]

    df = spark.createDataFrame(data, ["id", "email"])

    trasformer = CompositeTransformer()

    with pytest.raises(ValueError, match="Column 'username' does not exist"):
        trasformer.transform(df)