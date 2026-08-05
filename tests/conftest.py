from unittest.mock import MagicMock, patch

import pytest

from app.runtime.spark_runtime import SparkRuntime


@pytest.fixture(scope="session")
def spark():
    runtime = SparkRuntime()
    spark = runtime.start()
    yield spark

    runtime.stop()

@pytest.fixture
def mocked_spark():
    with patch("app.runtime.spark_runtime.SparkSession") as mock_spark_session:
        spark = MagicMock()

        mock_spark_session.builder.master.return_value \
            .appName.return_value \
            .getOrCreate.return_value = spark

        yield spark