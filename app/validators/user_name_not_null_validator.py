from .validator_base import Validator, ValidationResult
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, trim


class UserNameNotNullValidator(Validator[DataFrame]):

    def validate(self, data: DataFrame) -> ValidationResult:
        invalid_rows = data.filter(
            col("username").isNull() | (trim(col("username")) == "")
        )

        errors = [row.asDict() for row in invalid_rows.limit(10).collect()]

        if errors:
            return ValidationResult(is_valid=False, errors=errors)
        return ValidationResult.ok()
