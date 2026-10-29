from .registry_base import EntityRegistry

from app.runtime.runtime_base import Runtime
from app.runtime.spark_runtime import SparkRuntime
from app.runtime.configurators.configurator_base import SparkConfigurator
from app.runtime.configurators.s3a_configurator import S3AConfigurator

runtime_registry = EntityRegistry[Runtime]()
runtime_registry.register("spark", SparkRuntime)

#configurator
spark_configurator_registry = EntityRegistry[SparkConfigurator]()
spark_configurator_registry.register("s3a", S3AConfigurator)