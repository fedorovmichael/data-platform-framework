from app.validators.user_name_not_null_validator import UserNameNotNullValidator
from app.validators.user_composite_validator import CompositeValidator

VALIDATOR_REGISTRY = {
    "spark_username_null_empty": UserNameNotNullValidator,
    "spark_user_composit_validation": CompositeValidator,
}
