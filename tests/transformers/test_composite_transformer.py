import pytest

from app.transformers.transform_builder import TransformBuilder


def test_transform_builder_executes_transformers_sequentially(spark):
    data = [
        (1, "alice", "alice@example.com"),
        (2, "bob", "bob@example.com"),
        (3, "lee", "lee@example.com"),
    ]
    config = [
        {
            "type": "spark_select_columns",
            "options": {"columns": ["id", "username"]},
        },
        {"type": "spark_filter_rows", "options": {"condition": "id > 1"}},
        {"type": "spark_upper_username"},
    ]
    df = spark.createDataFrame(data, ["id", "username", "email"])

    builder = TransformBuilder()
    transformer = builder.build(config)
    result = transformer.transform(df)

    rows = result.orderBy("id").collect()

    assert [row.id for row in rows] == [2, 3]
    assert [row.username for row in rows] == ["BOB", "LEE"]
    assert result.columns == ["id", "username"]

