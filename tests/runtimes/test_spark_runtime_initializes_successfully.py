from app.runtime.spark_runtime import SparkRuntime


def test_spark_runtime_initializes_successfully():
    runtime = SparkRuntime()

    spark = runtime.start()

    assert spark is not None
    assert runtime.spark is spark

    runtime.stop()