
from .runtime_base import Runtime 
from app.registry.runtime_registry import runtime_registry 


class RuntimeBuilder:
    def build(self, config: dict) -> Runtime:
        if not config:
            raise ValueError("Runtime must be configured.")

        return runtime_registry.create(config["type"], **config.get("options", {}))