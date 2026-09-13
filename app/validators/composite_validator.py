from .validator_base import Validator, ValidationResult
from typing import TypeVar

T = TypeVar("T")


class CompositeValidator(Validator[T]):
    def __init__(self, validators: list[Validator[T]]) -> None:
        self.validators = validators

    def validate(self, data: T) -> ValidationResult:
        errors = []

        for validator in self.validators:
            result = validator.validate(data)

            if not result.is_valid:
                errors.extend(result.errors)

        if errors:
            return ValidationResult.fail(*errors)

        return ValidationResult.ok()
