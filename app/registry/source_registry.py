from .registry_base import EntityRegistry

from app.sources.csv_spark_source import CsvSparkSource
from app.sources.source_base import Source

source_registry = EntityRegistry[Source]()
source_registry.register("csv_spark", CsvSparkSource)
