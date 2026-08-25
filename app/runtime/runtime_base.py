from abc import ABC, abstractmethod

from app.pipeline.pipeline_base import PipelineBase


class Runtime(ABC):

    @abstractmethod
    def run(self, pipeline: PipelineBase, execution_id: str) -> None:
        """Execute a pipeline inside this runtime."""
        ...

