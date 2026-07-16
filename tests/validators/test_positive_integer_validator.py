from app.validators.positive_integer_validator import (
    PositiveIntegerValidator,
)

def test_positive_number_is_valid():
    #Arrange
    validator = PositiveIntegerValidator()

    #Act
    result = validator.validate(10)

    #Assert
    assert result.is_valid is True
    assert result.errors == []

def test_zero_is_invalid():
    validator = PositiveIntegerValidator()

    result = validator.validate(0)

    assert result.is_valid is False
    assert result.errors == [
        "Value must be greater than zero."
    ]

def test_negative_number_is_invalid():
    validator = PositiveIntegerValidator()

    result = validator.validate(-10)

    assert result.is_valid is False
    assert result.errors == [
        "Value must be greater than zero."
    ]
