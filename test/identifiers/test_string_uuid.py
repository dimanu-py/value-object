import pytest
from expects import equal, expect, raise_error
from object_mother.identifiers.string_uuid_primitives_mother import (
    StringUuidPrimitivesMother,
)

from value_object.errors.incorrect_value_type_error import (
    IncorrectValueTypeError,
)
from value_object.errors.invalid_id_format_error import (
    InvalidIdFormatError,
)
from value_object.errors.required_value_error import RequiredValueError
from value_object.identifiers.string_uuid import (
    StringUuid,
)

pytestmark = pytest.mark.unit


def test_should_create_uuid_value_object() -> None:
    value = StringUuidPrimitivesMother.any()

    uuid = StringUuid(value)

    expect(uuid.value).to(equal(value))


def test_should_raise_error_when_value_is_none() -> None:
    expect(lambda: StringUuid(None)).to(raise_error(RequiredValueError))


def test_should_raise_error_when_value_is_not_string() -> None:
    expect(lambda: StringUuid(123)).to(raise_error(IncorrectValueTypeError))


def test_should_raise_error_when_value_is_not_valid_uuid() -> None:
    invalid_uuid = StringUuidPrimitivesMother.invalid()
    expect(lambda: StringUuid(invalid_uuid)).to(raise_error(InvalidIdFormatError))


def test_should_compare_equal_with_same_value() -> None:
    common_value = StringUuidPrimitivesMother.any()
    first_uuid = StringUuid(common_value)
    second_uuid = StringUuid(common_value)

    expect(first_uuid).to(equal(second_uuid))


def test_should_not_be_equal_with_different_values() -> None:
    first_uuid = StringUuid(StringUuidPrimitivesMother.any())
    second_uuid = StringUuid(StringUuidPrimitivesMother.any())

    expect(first_uuid).to_not(equal(second_uuid))
