import pytest
from app.sources.csv_spark_source import CsvSparkSource
from pyspark.sql import DataFrame


def test_read_returns_dataframe(spark, tmp_path):
    csv_path = tmp_path / "users.csv"
    csv_path.write_text(
        "id,name\n1,Michael\n2,Anna\n",
        encoding="utf-8",
    )

    source = CsvSparkSource(spark=spark, csv_path=str(csv_path))

    dataframe = source.read()

    assert isinstance(dataframe, DataFrame)
    assert dataframe.count() == 2
    assert dataframe.columns == ["id", "name"]


def test_initialization_without_spark_raises_error():
    with pytest.raises(ValueError, match="SparkSession is required."):
        CsvSparkSource(spark=None, csv_path="users.csv")

    
def test_initialization_without_csv_path_raises_error(spark):
    with pytest.raises(ValueError, match="CSV path is required."):
        CsvSparkSource(spark=spark, csv_path=None)