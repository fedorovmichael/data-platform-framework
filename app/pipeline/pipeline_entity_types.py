
from enum import Enum


class PipelineEntityTypes(str, Enum):
    SOURCE = "source"
    VALIDATOR = "validator"
    TRANSFORMER = "transformer"
    SINK = "sink"
    RUNTIME = "runtime"