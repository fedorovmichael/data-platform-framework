from .transform_base import Transformer
from .composite_transform import CompositeTransform
from app.registry.transformer_registry import transformer_registry


class TransformBuilder:
    def build(self, configs: list[dict]) -> Transformer:
        if not configs:
            raise ValueError("At least one transformer must be configured")

        transformers = [
            transformer_registry.create(config.get("type"), **config.get("options", {}))
            for config in configs
        ]

        if len(transformers) == 1:
            return transformers[0]

        return CompositeTransform(transformers)
