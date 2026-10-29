from unittest.mock import MagicMock, call

import pytest

from app.runtime.spark_runtime import SparkRuntime
from app.runtime.configurators.configurator_base import SparkConfigurator


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


def test_spark_runtime_executes_configurator(mocked_spark) -> None:
    configurator = MagicMock(spec=SparkConfigurator)
    pipeline = MagicMock()
    order = MagicMock()
    order.attach_mock(configurator.configure, "configure")
    order.attach_mock(pipeline.run, "pipeline_run")
    order.attach_mock(mocked_spark.stop, "stop")

    runtime = SparkRuntime(configurators=[configurator])
    runtime.run(pipeline, "test-execution-id")

    context = pipeline.run.call_args.args[0]

    assert context.execution_id == "test-execution-id"
    assert context.get_resource("spark") is mocked_spark

    assert order.mock_calls == [
        call.configure(mocked_spark),
        call.pipeline_run(context),
        call.stop()
    ]
    configurator.configure.assert_called_once_with(mocked_spark)
    pipeline.run.assert_called_once()
    mocked_spark.stop.assert_called_once()


def test_spark_runtime_stops_when_configurator_fails(mocked_spark) -> None:
    configurator = MagicMock(spec=SparkConfigurator)
    configurator.configure.side_effect = RuntimeError("S3A configuration failed")

    pipeline = MagicMock()
    runtime = SparkRuntime(configurators=[configurator])

    with pytest.raises(RuntimeError, match="S3A configuration failed"):
        runtime.run(pipeline, "test-execution-id")

    configurator.configure.assert_called_once_with(mocked_spark)
    pipeline.run.assert_not_called()
    mocked_spark.stop.assert_called_once()
