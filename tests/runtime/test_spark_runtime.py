from app.runtime.spark_runtime import SparkRuntime


def test_spark_runtime_initializes_successfully():
    runtime = SparkRuntime()
    try:
        spark = runtime.start()

        assert spark is not None
        assert runtime.spark is spark
    finally:
        runtime.stop()


def test_stop_without_start_does_not_raise():
    runtime = SparkRuntime()

    runtime.stop()

    assert runtime.spark is None


def test_stop_clears_spark_session():
    runtime = SparkRuntime()
    runtime.start()

    runtime.stop()

    assert runtime.spark is None
