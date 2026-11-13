from .registry_base import EntityRegistry

from app.sinks.sink_parquet import SinkParquet
from app.sinks.sink_s3_spark import S3SparkSink
from app.sinks.sink_base import Sink

sink_registry = EntityRegistry[Sink]()
sink_registry.register("parquet", SinkParquet)
sink_registry.register("s3_spark", S3SparkSink)
