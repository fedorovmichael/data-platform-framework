from .validator_base import Validator, ValidationResult, ValidationError
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, trim


class UserEmailNotNullOrEmptyValidator(Validator[DataFrame]):

    def validate(self, data: DataFrame) -> ValidationResult:
        invalid_rows = data.filter(col("email").isNull() | (trim(col("email")) == ""))

        errors: list[ValidationError] = []
        for row in invalid_rows.limit(10).collect():
            errors.append(
                ValidationError(
                    rule="user_email_not_null_or_empty",
                    message="Column 'email' is missing or empty",
                    row=row.asDict(),
                )
            )

        if errors:
            return ValidationResult.fail(*errors)

        return ValidationResult.ok()
