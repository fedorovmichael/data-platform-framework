from app.validators.validator_base import Validator
from app.validators.user_name_not_null_validator import UserNameNotNullValidator
from app.validators.user_email_not_null_or_empty_validator import UserEmailNotNullOrEmptyValidator
from .registry_base import EntityRegistry


validator_registry = EntityRegistry[Validator]()

validator_registry.register("spark_username_null_empty", UserNameNotNullValidator)
validator_registry.register("spark_email_null_empty", UserEmailNotNullOrEmptyValidator)
