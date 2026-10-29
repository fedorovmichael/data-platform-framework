
from .runtime_base import Runtime 
from app.registry.runtime_registry import runtime_registry 
from .configurators.configurator_builder import SparkConfiguratorBuilder


class RuntimeBuilder:
    def __init__(self):
        self._configurator_builder = SparkConfiguratorBuilder()

    def build(self, config: dict) -> Runtime:
        if not config:
            raise ValueError("Runtime must be configured.")

        options = config.get("options", {}).copy()

        if "configurators" in options:
            options["configurators"] = [
                self._configurator_builder.build(item)
                for item in options["configurators"]
            ]

        return runtime_registry.create(config["type"], **options)