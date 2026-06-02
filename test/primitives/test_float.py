from typing import Any

import pytest
from expects import equal, expect, raise_error
from object_mother.primitives.float_primitives_mother import (
    FloatPrimitivesMother,
)

from value_object.errors.incorrect_value_type_error import (
    IncorrectValueTypeError,
)
from value_object.errors.required_value_error import RequiredValueError
from value_object.primitives.float import (
    Float,
)

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(FloatPrimitivesMother.any(), id="random value"),
        pytest.param(FloatPrimitivesMother.positive(), id="positive value"),
        pytest.param(FloatPrimitivesMother.negative(), id="negative value"),
        pytest.param(FloatPrimitivesMother.zero(), id="zero value"),
    ],
)
def test_should_create_float_value_object(value: float) -> None:
    float_obj = Float(value)

    expect(float_obj.value).to(equal(value))


def test_should_raise_error_when_value_is_none() -> None:
    expect(lambda: Float(None)).to(raise_error(RequiredValueError))


@pytest.mark.parametrize(
    "invalid_value",
    [
        pytest.param(42, id="integer value"),
        pytest.param("3.14", id="string value"),
    ],
)
def test_should_raise_error_when_value_has_invalid_type(invalid_value: Any) -> None:
    expect(lambda: Float(invalid_value)).to(raise_error(IncorrectValueTypeError))


def test_should_compare_equal_with_same_value() -> None:
    common_value = FloatPrimitivesMother.any()
    first_float = Float(common_value)
    second_float = Float(common_value)

    expect(first_float).to(equal(second_float))


def test_should_not_be_equal_with_different_values() -> None:
    first_float = Float(FloatPrimitivesMother.positive())
    second_float = Float(FloatPrimitivesMother.negative())

    expect(first_float).to_not(equal(second_float))


def test_should_not_allow_to_modify_value() -> None:
    value = FloatPrimitivesMother.any()
    float_obj = Float(value)

    def modify_value() -> None:
        float_obj._value = value + 1.0

    expect(modify_value).to(raise_error(AttributeError))


def test_should_have_consistent_hash_for_equal_values() -> None:
    value = FloatPrimitivesMother.any()
    first_float = Float(value)
    second_float = Float(value)

    expect(hash(first_float)).to(equal(hash(second_float)))


def test_should_have_different_hash_for_different_values() -> None:
    positive_float = Float(FloatPrimitivesMother.positive())
    negative_float = Float(FloatPrimitivesMother.negative())

    expect(hash(positive_float)).to_not(equal(hash(negative_float)))


def test_should_be_usable_as_dict_key() -> None:
    positive_float = Float(1.5)
    negative_float = Float(-2.5)

    test_dict = {positive_float: "positive_value", negative_float: "negative_value"}

    expect(test_dict[Float(1.5)]).to(equal("positive_value"))
    expect(test_dict[Float(-2.5)]).to(equal("negative_value"))


def test_should_be_usable_in_sets() -> None:
    float1 = Float(3.14)
    float2 = Float(3.14)
    float3 = Float(2.71)

    float_set = {float1, float2, float3}

    expect(len(float_set)).to(equal(2))


def test_should_not_allow_modifying_value_through_public_name() -> None:
    value = FloatPrimitivesMother.any()
    float_obj = Float(value)

    def modify_public_value() -> None:
        float_obj.value = value + 1.0

    expect(modify_public_value).to(raise_error(AttributeError))


def test_should_provide_access_to_wrapped_value() -> None:
    value = FloatPrimitivesMother.any()
    float_obj = Float(value)

    expect(float_obj.value).to(equal(value))
    expect(type(float_obj.value)).to(equal(float))
