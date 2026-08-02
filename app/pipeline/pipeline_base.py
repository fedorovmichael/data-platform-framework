
from abc import ABC, abstractmethod
from app.execution.execution_context import ExecutionContext

class PipelineBase(ABC):
    """Base contract for all pipelines."""

    @abstractmethod
    def run(self, context: ExecutionContext) -> None:
        """Execute the pipeline using the runtime context."""
        ...