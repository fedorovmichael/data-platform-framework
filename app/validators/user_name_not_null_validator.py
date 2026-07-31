from .validator_base import Validator, ValidationResult
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

class UserNameNotNullValidator(Validator[DataFrame]):

    def validate(self, data: DataFrame)-> ValidationResult:
        invalid_rows = data.filter(col("username").isNull() | (col("username") == ""))
        if invalid_rows.count() > 0:
            errors =[row.asDict() for row in invalid_rows.collect()]  
            return ValidationResult(is_valid=False, errors=errors)
        return ValidationResult().ok() 
         