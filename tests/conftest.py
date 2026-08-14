from unittest.mock import MagicMock, patch

import pytest
from pyspark.sql import SparkSession

from app.execution.execution_context import ExecutionContext


@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder.master("local[2]").appName("SparkTest").getOrCreate()
    yield spark

    spark.stop()


@pytest.fixture
def mocked_spark():
    with patch("app.runtime.spark_runtime.SparkSession") as mock_spark_session:
        spark = MagicMock()

        mock_spark_session.builder.master.return_value.appName.return_value.getOrCreate.return_value = (
            spark
        )

        yield spark


@pytest.fixture
def spark_context(spark):
    context = ExecutionContext(
        resources={
            "spark": spark,
        }
    )

    yield context
