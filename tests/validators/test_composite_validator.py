from app.validators.user_composite_validator import CompositeValidator


def test_all_validators_success(spark):
    data = [(1, "alice", "alice@example.com"), (2, "bob", "bob@example.com")]
    df = spark.createDataFrame(data, ["id", "username", "email"])

    validator = CompositeValidator()

    validator_result = validator.validate(df)

    assert validator_result.is_valid is True
    assert validator_result.errors == []


def test_one_validator_fails(spark):
    data = [(1, "", "alice@example.com"), (2, "bob", "bob@example.com")]
    df = spark.createDataFrame(data, ["id", "username", "email"])

    validator = CompositeValidator()

    validator_result = validator.validate(df)

    assert validator_result.is_valid is False
    assert len(validator_result.errors) == 1
    assert validator_result.errors[0].rule == "user_name_not_null_or_empty"


def test_all_validators_fail(spark):
    data = [(1, "", "alice@example.com"), (2, "bob", "")]
    df = spark.createDataFrame(data, ["id", "username", "email"])

    validator = CompositeValidator()

    validator_result = validator.validate(df)

    assert validator_result.is_valid is False
    assert len(validator_result.errors) == 2

    messages = [error.message for error in validator_result.errors]

    assert "Column 'username' is missing or empty" in messages
    assert "Column 'email' is missing or empty" in messages
