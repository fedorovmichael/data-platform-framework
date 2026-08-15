from app.transformers.composite_transformer import CompositeTransformer


def test_all_transformers_success(spark):
    data = [(1, "alice", "alice@example.com"), (2, "bob", "bob@example.com"), (3, "lee", "lee@example.com")]
    df = spark.createDataFrame(data, ["id", "username", "email"])

    transformer = CompositeTransformer()
    result = transformer.transform(df)

    rows = result.orderBy("id").collect()

    assert [row.id for row in rows] == [2, 3]
    assert [row.username for row in rows] == ["BOB", "LEE"]
    assert result.columns == ["id", "username"]