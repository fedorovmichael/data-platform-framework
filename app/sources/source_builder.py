from .source_base import Source
from app.registry.source_registry import source_registry


class SourceBuilder:
    def build(self, config: dict) -> Source:
        if not config:
            raise ValueError("Source must be configured.")

        return source_registry.create(config["type"], **config.get("options", {}))
