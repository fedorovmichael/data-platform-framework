from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from dataclasses import dataclass, field

T = TypeVar("T")


@dataclass
class ValidationError:
    rule: str
    message: str
    row: dict | None = None


@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[ValidationError] = field(default_factory=list)

    @classmethod
    def ok(cls) -> "ValidationResult":
        return cls(is_valid=True, errors=[])

    @classmethod
    def fail(cls, *errors: ValidationError) -> "ValidationResult":
        return cls(is_valid=False, errors=list(errors))


class Validator(ABC, Generic[T]):
    """Base contract for all validators."""

    @abstractmethod
    def validate(self, data: T) -> ValidationResult:
        """Validate data and return a ValidationResult"""
        ...
