from unittest.mock import MagicMock, patch

import pytest

from app.runtime.spark_runtime import SparkRuntime


@patch("app.runtime.spark_runtime.SparkSession")
def test_spark_runtime_runs_pipeline(mock_spark_session) -> None:
    spark = MagicMock()
    mock_spark_session.builder.master.return_value.appName.return_value.getOrCreate.return_value = (
        spark
    )

    pipeline = MagicMock()
    runtime = SparkRuntime(app_name="test-app", master="local[1]")

    runtime.run(pipeline)

    pipeline.run.assert_called_once()

    context = pipeline.run.call_args.args[0]

    assert context.get_resource("spark") is spark
    spark.stop.assert_called_once_with()


@patch("app.runtime.spark_runtime.SparkSession")
def test_spark_runtime_stops_spark_when_pipeline_fails(mock_spark_session) -> None:
    spark = MagicMock()
    mock_spark_session.builder.master.return_value.appName.return_value.getOrCreate.return_value = (
        spark
    )

    pipeline = MagicMock()
    pipeline.run.side_effect = RuntimeError("Pipeline failed")

    runtime = SparkRuntime()

    with pytest.raises(RuntimeError, match="Pipeline failed"):
        runtime.run(pipeline)

    spark.stop.assert_called_once_with()
