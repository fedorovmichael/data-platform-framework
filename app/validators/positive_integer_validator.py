from app.validators.validator_base import ValidationResult, Validator


class PositiveIntegerValidator(Validator[int]):
    def validate(self, data: int)-> ValidationResult:
        if data > 0:
            return ValidationResult.ok()

        return ValidationResult.fail(
            "Value must be greater than zero."
        )
        
    

