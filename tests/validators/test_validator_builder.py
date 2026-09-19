import pytest

from app.validators.validator_builder import ValidatorBuilder
from app.validators.composite_validator import CompositeValidator 
from app.validators.user_email_not_null_or_empty_validator import UserEmailNotNullOrEmptyValidator
from app.validators.user_name_not_null_validator import UserNameNotNullValidator


def test_build_multiple_validators_returns_composite_validator():
    config = [
        {"type": "spark_username_null_empty"},
        {"type": "spark_email_null_empty"},
    ]

    builder = ValidatorBuilder()
    result = builder.build(config)

    assert isinstance(result, CompositeValidator)
    assert len(result.validators) == 2
    assert isinstance(result.validators[0], UserNameNotNullValidator)
    assert isinstance(result.validators[1], UserEmailNotNullOrEmptyValidator)


def test_build_multiple_validators_returns_composite_validator_failed():
    config = [
        {"type": "spark_username_null_empty1"},
        {"type": "spark_email_null_empty"},
    ]

    builder = ValidatorBuilder()

    with pytest.raises(ValueError, match="Unknown registry entity 'spark_username_null_empty1'"):
      builder.build(config)


def test_build_single_validator_returns_validator():
    config = [
        {"type": "spark_username_null_empty"},
    ]

    builder = ValidatorBuilder()
    result = builder.build(config)

    assert isinstance(result, UserNameNotNullValidator)
    assert not isinstance(result, CompositeValidator)