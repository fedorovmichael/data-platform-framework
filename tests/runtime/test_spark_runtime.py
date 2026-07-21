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

    assert runtime.stop is None