from .registry_base import EntityRegistry

from app.runtime.runtime_base import Runtime
from app.runtime.spark_runtime import SparkRuntime

runtime_registry = EntityRegistry[Runtime]()
runtime_registry.register("spark", SparkRuntime)
