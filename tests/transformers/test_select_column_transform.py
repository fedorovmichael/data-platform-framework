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


def test_select_columns_raise_error_empty_columns(tmp_path):
    csv_path = tmp_path / file_name 
    csv_path.write_text(csv_data, encoding="utf-8")

    with pytest.raises(ValueError, match="Columns can not be empty."):
        SelectColumnsTransform(columns=[])

    with pytest.raises(ValueError, match="Columns can not be empty."):
        SelectColumnsTransform(columns=None)