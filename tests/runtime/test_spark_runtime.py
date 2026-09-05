from unittest.mock import MagicMock 

import pytest

from app.runtime.spark_runtime import SparkRuntime


def test_spark_runtime_runs_pipeline(mocked_spark) -> None:

    pipeline = MagicMock()
    runtime = SparkRuntime(app_name="test-app", master="local[1]")

    execution_id = "test_execution_id"

    runtime.run(pipeline, execution_id)

    pipeline.run.assert_called_once()

    context = pipeline.run.call_args.args[0]

    assert context.execution_id == execution_id
    assert context.get_resource("spark") is mocked_spark
    mocked_spark.stop.assert_called_once_with()


def test_spark_runtime_stops_spark_when_pipeline_fails(mocked_spark) -> None:
    pipeline = MagicMock()
    pipeline.run.side_effect = RuntimeError("Pipeline failed")

    runtime = SparkRuntime()

    with pytest.raises(RuntimeError, match="Pipeline failed"):
        runtime.run(pipeline, "test-execution-id")

    mocked_spark.stop.assert_called_once_with()
