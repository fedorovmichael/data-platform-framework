from app.pipeline.pipeline import Pipeline
from app.registry import (
    SINK_REGISTRY,
    SOURCE_REGISTRY,
    VALIDATOR_REGISTRY,
    TRANSFORMER_REGISTRY,
)


class PipelineBuilder:

    def build(self, config: dict) -> Pipeline:
        pass
