from .validator_base import Validator
from .composite_validator import CompositeValidator
from app.registry.validator_registry import validator_registry

class ValidatorBuilder:
    def build(self, configs: list[dict]) -> Validator:
        validators = [
            validator_registry.create(config["type"])
            for config in configs
        ]

        if len(validators) == 1:
            return validators[0]

        return CompositeValidator(validators)