from  dataclasses import dataclass

from app.pipeline.pipeline_base import PipelineBase
from app.runtime.runtime_base import Runtime


@dataclass(slots=True)
class PipelineExecution:
    runtime: Runtime
    pipeline: PipelineBase

    def run(self) -> None:
        self.runtime.run(self.pipeline)