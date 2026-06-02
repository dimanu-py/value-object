from typing import Any

import pytest
from expects import equal, expect, raise_error
from object_mother.primitives.integer_primitives_mother import (
    IntegerPrimitivesMother,
)

from value_object.errors.incorrect_value_type_error import (
    IncorrectValueTypeError,
)
from value_object.errors.required_value_error import RequiredValueError
from value_object.primitives.integer import (
    Integer,
)

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(IntegerPrimitivesMother.any(), id="random value"),
        pytest.param(IntegerPrimitivesMother.positive(), id="positive integer"),
        pytest.param(IntegerPrimitivesMother.negative(), id="negative integer"),
        pytest.param(IntegerPrimitivesMother.zero(), id="zero value"),
    ],
)
def test_should_create_integer_value_object(value: int) -> None:
    integer = Integer(value)

    expect(integer.value).to(equal(value))


def test_should_raise_error_when_value_is_none() -> None:
    expect(lambda: Integer(None)).to(raise_error(RequiredValueError))


@pytest.mark.parametrize(
    "invalid_value",
    [
        pytest.param(12.34, id="float value"),
        pytest.param("42", id="string value"),
        pytest.param([], id="list value"),
        pytest.param({}, id="dict value"),
    ],
)
def test_should_raise_error_when_value_has_invalid_type(invalid_value: Any) -> None:
    expect(lambda: Integer(invalid_value)).to(raise_error(IncorrectValueTypeError))


def test_should_compare_equal_with_same_value() -> None:
    common_value = IntegerPrimitivesMother.any()
    first_integer = Integer(common_value)
    second_integer = Integer(common_value)

    expect(first_integer).to(equal(second_integer))


def test_should_not_be_equal_with_different_values() -> None:
    first_integer = Integer(IntegerPrimitivesMother.positive())
    second_integer = Integer(IntegerPrimitivesMother.negative())

    expect(first_integer).to_not(equal(second_integer))


def test_should_not_allow_to_modify_value() -> None:
    value = IntegerPrimitivesMother.any()
    integer = Integer(value)

    def modify_value() -> None:
        integer._value = value + 1

    expect(modify_value).to(raise_error(AttributeError))


def test_should_have_consistent_hash_for_equal_values() -> None:
    value = IntegerPrimitivesMother.any()
    first_integer = Integer(value)
    second_integer = Integer(value)

    expect(hash(first_integer)).to(equal(hash(second_integer)))


def test_should_have_different_hash_for_different_values() -> None:
    first_integer = Integer(IntegerPrimitivesMother.positive())
    second_integer = Integer(IntegerPrimitivesMother.negative())

    expect(hash(first_integer)).to_not(equal(hash(second_integer)))


def test_should_be_usable_as_dict_key() -> None:
    forty_two = Integer(42)
    twenty_four = Integer(24)

    test_dict = {forty_two: "forty_two_value", twenty_four: "twenty_four_value"}

    expect(test_dict[Integer(42)]).to(equal("forty_two_value"))
    expect(test_dict[Integer(24)]).to(equal("twenty_four_value"))


def test_should_be_usable_in_sets() -> None:
    forty_two = Integer(42)
    forty_two_duplicated = Integer(42)
    twenty_four = Integer(24)

    integer_set = {forty_two, forty_two_duplicated, twenty_four}

    expect(len(integer_set)).to(equal(2))


def test_should_not_allow_modifying_value_through_public_name() -> None:
    value = IntegerPrimitivesMother.any()
    integer = Integer(value)

    def modify_public_value() -> None:
        integer.value = value + 1

    expect(modify_public_value).to(raise_error(AttributeError))


def test_should_provide_access_to_wrapped_value() -> None:
    value = IntegerPrimitivesMother.any()
    integer = Integer(value)

    expect(integer.value).to(equal(value))
    expect(type(integer.value)).to(equal(int))
