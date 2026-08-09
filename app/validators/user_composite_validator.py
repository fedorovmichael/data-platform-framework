from .validator_base import Validator, ValidationResult
from pyspark.sql import DataFrame
from .user_name_not_null_validator import UserNameNotNullValidator
from .user_email_not_null_validator import UserEmailNotNullValidator


class CompositeValidator(Validator[DataFrame]):

    def validate(self, data: DataFrame)-> ValidationResult:
        user_name_not_null = UserNameNotNullValidator()
        user_name_not_null_result = user_name_not_null.validate(data)

        user_email_not_null = UserEmailNotNullValidator()
        user_email_not_null_result = user_email_not_null.validate(data)

        if not (user_name_not_null_result.is_valid and user_email_not_null_result.is_valid):
            errors = (user_email_not_null_result.errors + user_name_not_null_result.errors)

            return ValidationResult(is_valid=False, errors=errors)

        return ValidationResult.ok()