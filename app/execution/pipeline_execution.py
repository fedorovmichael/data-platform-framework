from dataclasses import dataclass, field
import logging
from uuid import uuid4
import time
from .execution_status import ExecutionStatus

from app.pipeline.pipeline_base import PipelineBase
from app.runtime.runtime_base import Runtime

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class PipelineExecution:
    name: str
    runtime: Runtime
    pipeline: PipelineBase

    execution_id: str = field(default_factory=lambda: str(uuid4()), init=False)
    status: ExecutionStatus = field(default=ExecutionStatus.PENDING, init=False)

    def run(self) -> None:
        self.status = ExecutionStatus.RUNNING
        start_time = time.perf_counter()

        try:
            logger.info(
                "execution_id=%s Pipeline %s execution started",
                self.execution_id,
                self.name,
            )

            self.runtime.run(self.pipeline, self.execution_id)

            duration_ms = (time.perf_counter() - start_time) * 1000
            self.status = ExecutionStatus.SUCCESS

            logger.info(
                "execution_id=%s Pipeline %s execution succeeded duration_ms=%.2f",
                self.execution_id,
                self.name,
                duration_ms,
            )

        except Exception:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self.status = ExecutionStatus.FAILED

            logger.exception(
                "execution_id=%s Pipeline %s execution failed duration_ms=%.2f",
                self.execution_id,
                self.name,
                duration_ms,
            )
            raise
