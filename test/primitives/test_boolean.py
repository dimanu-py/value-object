from typing import Any

import pytest
from expects import equal, expect, raise_error
from object_mother.primitives.boolean_primitives_mother import (
    BooleanPrimitivesMother,
)

from value_object.errors.incorrect_value_type_error import (
    IncorrectValueTypeError,
)
from value_object.errors.required_value_error import RequiredValueError
from value_object.primitives.boolean import (
    Boolean,
)

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(BooleanPrimitivesMother.any(), id="random value"),
        pytest.param(BooleanPrimitivesMother.true(), id="true value"),
        pytest.param(BooleanPrimitivesMother.false(), id="false value"),
    ],
)
def test_should_create_boolean_value_object(value: bool) -> None:
    boolean = Boolean(value)

    expect(boolean.value).to(equal(value))


def test_should_raise_error_when_value_is_none() -> None:
    expect(lambda: Boolean(None)).to(raise_error(RequiredValueError))


@pytest.mark.parametrize(
    "invalid_value",
    [
        pytest.param(1, id="integer value"),
        pytest.param(0, id="zero value"),
        pytest.param("true", id="truthy string value"),
        pytest.param("false", id="falsy string value"),
        pytest.param("", id="empty falsy string"),
        pytest.param([], id="empty falsy list"),
        pytest.param({}, id="empty falsy dict"),
    ],
)
def test_should_raise_error_when_value_has_invalid_type(invalid_value: Any) -> None:
    expect(lambda: Boolean(invalid_value)).to(raise_error(IncorrectValueTypeError))


def test_should_compare_equal_with_same_value() -> None:
    common_value = BooleanPrimitivesMother.any()
    first_boolean = Boolean(common_value)
    second_boolean = Boolean(common_value)

    expect(first_boolean).to(equal(second_boolean))


def test_should_not_be_equal_with_different_values() -> None:
    true_boolean = Boolean(BooleanPrimitivesMother.true())
    false_boolean = Boolean(BooleanPrimitivesMother.false())

    expect(true_boolean).to_not(equal(false_boolean))


def test_should_not_allow_to_modify_value() -> None:
    value = BooleanPrimitivesMother.any()
    boolean = Boolean(value)

    def modify_value() -> None:
        boolean._value = not value

    expect(modify_value).to(raise_error(AttributeError))


def test_should_have_consistent_hash_for_equal_values() -> None:
    value = BooleanPrimitivesMother.any()
    first_boolean = Boolean(value)
    second_boolean = Boolean(value)

    expect(hash(first_boolean)).to(equal(hash(second_boolean)))


def test_should_have_different_hash_for_different_values() -> None:
    true_boolean = Boolean(BooleanPrimitivesMother.true())
    false_boolean = Boolean(BooleanPrimitivesMother.false())

    expect(hash(true_boolean)).to_not(equal(hash(false_boolean)))


def test_should_be_usable_as_dict_key() -> None:
    true_boolean = Boolean(BooleanPrimitivesMother.true())
    false_boolean = Boolean(BooleanPrimitivesMother.false())

    test_dict = {true_boolean: "true_value", false_boolean: "false_value"}

    expect(test_dict[Boolean(True)]).to(equal("true_value"))
    expect(test_dict[Boolean(False)]).to(equal("false_value"))


def test_should_be_usable_in_sets() -> None:
    true_boolean = Boolean(BooleanPrimitivesMother.true())
    true_boolean_duplicated = Boolean(BooleanPrimitivesMother.true())
    false_boolean = Boolean(BooleanPrimitivesMother.false())

    boolean_set = {true_boolean, true_boolean_duplicated, false_boolean}

    expect(len(boolean_set)).to(equal(2))


def test_should_not_allow_modifying_value_through_public_name() -> None:
    value = BooleanPrimitivesMother.any()
    boolean = Boolean(value)

    def modify_public_value() -> None:
        boolean.value = not value

    expect(modify_public_value).to(raise_error(AttributeError))


def test_should_provide_access_to_wrapped_value() -> None:
    value = BooleanPrimitivesMother.any()
    boolean = Boolean(value)

    expect(boolean.value).to(equal(value))
    expect(type(boolean.value)).to(equal(bool))
