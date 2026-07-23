import pytest
from app.transformers.select_columns_transform import SelectColumnsTransform

file_name = "select_columns_users.csv"
csv_data = "id,name,sex\n1,Michael,m\n2,Anna,f\n3,Nina,f\n4,Valera,m\n5,Nicol,f\n"


def test_select_columns(spark, tmp_path):
    csv_path = tmp_path / file_name
    csv_path.write_text(
        csv_data,
        encoding="utf-8",
    )

    df = spark.read.csv(str(csv_path), header=True, inferSchema=True)

    transform = SelectColumnsTransform(columns=["name", "sex"])
    result = transform.transform(df)

    assert result.columns == ["name", "sex"]


@pytest.mark.parametrize("columns", [[], (), None])
def test_select_columns_raise_error_empty_columns(columns):
    with pytest.raises(ValueError, match="Columns cannot be empty."):
        SelectColumnsTransform(columns=columns)


def test_select_columns_rejects_unknown_column(spark):
    df = spark.createDataFrame([(1,"Michael")], ["id", "name"])
    transform = SelectColumnsTransform(["unknown"])

    with pytest.raises(Exception):
        transform.transform(df)
