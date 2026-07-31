from app.validators.user_name_not_null_validator import UserNameNotNullValidator
from pyspark.sql.types import LongType, StringType, StructField, StructType


def test_validator_accepts_valid_username(spark):
    data = [{"id": 1, "username": "John"}]

    df = spark.createDataFrame(data)
    validator = UserNameNotNullValidator()
    result = validator.validate(df)

    assert result.is_valid
    assert len(result.errors) == 0


def test_validator_rejects_null_username(spark):
    schema = StructType([
        StructField("id", LongType(), nullable=False),
        StructField("username", StringType(), nullable=True)
    ])
    data = [(1, None)]

    df = spark.createDataFrame(data, schema=schema)
    validator = UserNameNotNullValidator()
    result = validator.validate(df)

    assert not result.is_valid
    assert len(result.errors) == 1


def test_validator_rejects_empty_username(spark):
    data = [{"id": 1, "username": ""}]

    df = spark.createDataFrame(data)
    validator = UserNameNotNullValidator()
    result = validator.validate(df)

    assert not result.is_valid
    assert len(result.errors) == 1


def test_validator_rejects_whitespace_username(spark):
    data = [{"id": 1, "username": "  "}]

    df = spark.createDataFrame(data)

    validator = UserNameNotNullValidator()

    result = validator.validate(df)

    assert not result.is_valid
    assert len(result.errors) == 1
