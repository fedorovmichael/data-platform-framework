import pytest
from app.sources.csv_spark_source import CsvSparkSource
from app.execution.execution_context import ExecutionContext
from pyspark.sql import DataFrame


def test_read_returns_dataframe(spark, tmp_path):
    csv_path = tmp_path / "users.csv"
    csv_path.write_text(
        "id,name\n1,Michael\n2,Anna\n",
        encoding="utf-8",
    )

    source = CsvSparkSource(path=str(csv_path))

    context = ExecutionContext(
        execution_id="test_execution_id",
        resources={"spark": spark},
    )

    dataframe = source.read(context)

    assert isinstance(dataframe, DataFrame)
    assert dataframe.count() == 2
    assert dataframe.columns == ["id", "name"]


def test_initialization_without_spark_raises_error(tmp_path):
    csv_path = tmp_path / "users.csv"
    source = CsvSparkSource(path=str(csv_path))

    context = ExecutionContext(
        execution_id="test_execution_id",
        resources={"spark": None},
    )

    with pytest.raises(ValueError, match="SparkSession is required."):
       source.read(context) 
    
def test_initialization_without_csv_path_raises_error():
    with pytest.raises(ValueError, match="CSV path must be a non-empty string."):
        CsvSparkSource(path=None)