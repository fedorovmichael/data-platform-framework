import pytest
from app.runtime.spark_runtime import SparkRuntime


@pytest.fixture(scope="session")
def spark():
    runtime = SparkRuntime()
    spark = runtime.start()
    yield spark

    runtime.stop()
