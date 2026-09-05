from unittest.mock import MagicMock
import pytest

from app.pipeline.pipeline_base import PipelineBase
from app.runtime.runtime_base import Runtime
from app.execution.pipeline_execution import PipelineExecution
from app.execution.execution_status import ExecutionStatus


def test_pipeline_execution_initial_status():
    runtime = MagicMock(spec=Runtime)
    pipeline = MagicMock(spec=PipelineBase)

    execution = PipelineExecution("test_pipeline_execution", runtime, pipeline)
    assert execution.status == ExecutionStatus.PENDING


def test_pipeline_execution_success_status():
    pipeline = MagicMock(spec=PipelineBase)
    runtime = MagicMock(spec=Runtime)

    runtime.run.return_value = None

    execution = PipelineExecution("test_pipeline_execution", runtime, pipeline)
    execution.run()

    assert execution.status == ExecutionStatus.SUCCESS
    runtime.run.assert_called_once_with(
        pipeline,
        execution.execution_id,
    )


def test_pipeline_execution_failed_status():
    pipeline = MagicMock(spec=PipelineBase)
    runtime = MagicMock(spec=Runtime)

    runtime.run.side_effect = RuntimeError("Runtime failed")

    execution = PipelineExecution("test_pipeline_execution", runtime, pipeline)

    with pytest.raises(RuntimeError, match="Runtime failed"):
        execution.run()

    assert execution.status == ExecutionStatus.FAILED
    runtime.run.assert_called_once_with(
        pipeline,
        execution.execution_id,
    )

def test_pipeline_execution_unique_execution_id():
    pipeline = MagicMock(spec=PipelineBase)
    runtime = MagicMock(spec=Runtime)

    execution1 = PipelineExecution("test_pipeline_execution1", runtime, pipeline)
    execution2 = PipelineExecution("test_pipeline_execution1", runtime, pipeline)

    assert execution1.execution_id != execution2.execution_id

def test_pipeline_execution_rejects_invalid_max_attempts():
    pipeline = MagicMock(spec=PipelineBase)
    runtime = MagicMock(spec=Runtime)

    with pytest.raises(ValueError, match="max_attempts must be at least 1"):
        PipelineExecution(
            "test_pipeline",
            runtime,
            pipeline,
            max_attempts=0,
        )

def test_pipeline_execution_succeeds_after_retry():
    pipeline = MagicMock(spec=PipelineBase)
    runtime = MagicMock(spec=Runtime)

    runtime.run.side_effect = [
        RuntimeError("Runtime failed"),
        None
    ]

    execution = PipelineExecution(
        "test_pipeline",
        runtime,
        pipeline,
        max_attempts=2,
    )

    execution.run()

    assert execution.status == ExecutionStatus.SUCCESS
    assert runtime.run.call_count == 2


def test_pipeline_execution_fails_after_max_attempts():
    pipeline = MagicMock(spec=PipelineBase)
    runtime = MagicMock(spec=Runtime)

    runtime.run.side_effect = [
        RuntimeError("Attempt 1 failed"),
        RuntimeError("Attempt 2 failed"),
        RuntimeError("Attempt 3 failed"),
    ]

    execution = PipelineExecution(
        "test_pipeline",
        runtime,
        pipeline,
        max_attempts=3,
    )

    with pytest.raises(RuntimeError, match="Attempt 3 failed"):
        execution.run()

    assert execution.status == ExecutionStatus.FAILED
    assert runtime.run.call_count == 3