from typing import Any

import pytest
from expects import equal, expect, raise_error

from object_mother.primitives.string_primitives_mother import (
    StringPrimitivesMother,
)
from value_object.errors.incorrect_value_type_error import (
    IncorrectValueTypeError,
)
from value_object.errors.required_value_error import RequiredValueError
from value_object.primitives.string import (
    String,
)

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(StringPrimitivesMother.any(), id="random value"),
        pytest.param(StringPrimitivesMother.empty(), id="empty string"),
    ],
)
def test_should_create_string_value_object(value: str) -> None:
    string = String(value)

    expect(string.value).to(equal(value))


def test_should_raise_error_when_value_is_none() -> None:
    expect(lambda: String(None)).to(raise_error(RequiredValueError))


@pytest.mark.parametrize(
    "invalid_value",
    [
        pytest.param(123, id="integer value"),
        pytest.param(12.34, id="float value"),
        pytest.param(True, id="boolean value"),
    ],
)
def test_should_raise_error_when_value_has_invalid_type(invalid_value: Any) -> None:
    expect(lambda: String(invalid_value)).to(raise_error(IncorrectValueTypeError))


def test_should_compare_equal_with_same_value() -> None:
    common_value = StringPrimitivesMother.any()
    first_string = String(common_value)
    second_string = String(common_value)

    expect(first_string).to(equal(second_string))


def test_should_not_be_equal_with_different_values() -> None:
    first_string = String("hello")
    second_string = String("world")

    expect(first_string).to_not(equal(second_string))


def test_should_not_allow_to_modify_value() -> None:
    value = StringPrimitivesMother.any()
    string = String(value)

    def modify_value() -> None:
        string._value = "modified"

    expect(modify_value).to(raise_error(AttributeError))


def test_should_have_consistent_hash_for_equal_values() -> None:
    value = StringPrimitivesMother.any()
    first_string = String(value)
    second_string = String(value)

    expect(hash(first_string)).to(equal(hash(second_string)))


def test_should_have_different_hash_for_different_values() -> None:
    first_string = String("hello")
    second_string = String("world")

    expect(hash(first_string)).to_not(equal(hash(second_string)))


def test_should_be_usable_as_dict_key() -> None:
    hello_string = String("hello")
    world_string = String("world")

    test_dict = {hello_string: "hello_value", world_string: "world_value"}

    expect(test_dict[String("hello")]).to(equal("hello_value"))
    expect(test_dict[String("world")]).to(equal("world_value"))


def test_should_be_usable_in_sets() -> None:
    hello_string = String("hello")
    hello_string_duplicated = String("hello")
    world_string = String("world")

    string_set = {hello_string, hello_string_duplicated, world_string}

    expect(len(string_set)).to(equal(2))


def test_should_not_allow_modifying_value_through_public_name() -> None:
    string = String("original")

    def modify_public_value() -> None:
        string.value = "modified"

    expect(modify_public_value).to(raise_error(AttributeError))


def test_should_provide_access_to_wrapped_value() -> None:
    value = StringPrimitivesMother.any()
    string = String(value)

    expect(string.value).to(equal(value))
    expect(type(string.value)).to(equal(str))
