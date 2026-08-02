from pyspark.sql import SparkSession

from app.runtime.runtime_base import Runtime
from app.execution.execution_context import ExecutionContext
from app.pipeline.pipeline_base import PipelineBase


class SparkRuntime(Runtime):
    def __init__(
        self, app_name: str = "DataPlatformFramework", master: str = "local[*]"
    ) -> None:
        self.app_name = app_name
        self.master = master

    def run(self, pipeline: PipelineBase) -> None:
        spark = (
            SparkSession.builder.master(self.master)
            .appName(self.app_name)
            .getOrCreate()
        )

        context = ExecutionContext(
            resources={
                "spark": spark,
            }
        )

        try:
            pipeline.run(context)
        finally:
            spark.stop
