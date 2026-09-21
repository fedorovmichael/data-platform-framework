from .sink_base import Sink 
from app.registry.sink_registry import sink_registry 


class SinkBuilder:
    def build(self, config: dict) -> Sink:
        if not config:
            raise ValueError("Sink must be configured.")

        return sink_registry.create(config["type"], **config.get("options", {}))