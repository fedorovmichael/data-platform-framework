from pyspark.sql import SparkSession

from app.runtime.runtime_base import Runtime
from app.execution.execution_context import ExecutionContext
from app.pipeline.pipeline_base import PipelineBase
from app.runtime.configurators.configurator_base import SparkConfigurator 


class SparkRuntime(Runtime):
    def __init__(
        self,
        app_name: str = "DataPlatformFramework",
        master: str = "local[*]",
        configurators: list[SparkConfigurator] | None = None,
    ) -> None:
        self.app_name = app_name
        self.master = master
        self.configurators = list(configurators) if configurators else []

    def run(self, pipeline: PipelineBase, execution_id: str) -> None:
        spark = (
            SparkSession.builder.master(self.master)
            .appName(self.app_name)
            .config(
                "spark.jars.packages",
                ",".join(
                    [
                        "org.postgresql:postgresql:42.7.8",
                        "org.apache.hadoop:hadoop-aws:3.5.0",
                    ]
                ),
            )
            .getOrCreate()
        )

        try:
            for configurator in self.configurators:
                configurator.configure(spark)

            context = ExecutionContext(
                execution_id=execution_id,
                resources={"spark": spark},
            )

            pipeline.run(context)
        finally:
            spark.stop()
