import pytest
from expects import equal, expect, raise_error

from value_object.optional import Optional
from value_object.primitives.string import String

pytestmark = pytest.mark.unit


def test_should_create_optional_with_valid_value() -> None:
    optional = Optional.of("test")

    expect(optional.is_present()).to(equal(True))


def test_should_raise_error_when_creating_optional_with_none() -> None:
    expect(lambda: Optional.of(None)).to(raise_error(ValueError))


def test_should_create_empty_optional() -> None:
    optional = Optional.empty()

    expect(optional.is_empty()).to(equal(True))


def test_should_create_optional_with_value_object() -> None:
    optional = Optional.of(String("hello"))

    expect(optional.is_present()).to(equal(True))


def test_should_unwrap_value_object_from_optional() -> None:
    value = String("hello")
    optional = Optional.of(value)

    result = optional.unwrap()

    expect(result).to(equal(value))


def test_should_map_over_value_object_in_optional() -> None:
    optional = Optional.of(String("hello"))

    result = optional.map(lambda s: s.value.upper())

    expect(result.unwrap()).to(equal("HELLO"))


def test_should_match_on_value_object_in_optional() -> None:
    optional = Optional.of(String("hello"))

    result = optional.match(of=lambda s: s.value.upper(), empty=lambda: "")

    expect(result).to(equal("HELLO"))


def test_should_return_value_when_unwrapping_present_optional() -> None:
    value = "test_value"
    optional = Optional.of(value)

    stored_value = optional.unwrap()

    expect(stored_value).to(equal(value))


def test_should_raise_error_when_unwrapping_empty_optional() -> None:
    optional = Optional.empty()

    expect(lambda: optional.unwrap()).to(raise_error(ValueError))


def test_should_return_empty_when_mapping_over_empty_optional() -> None:
    optional = Optional.empty()

    result = optional.map(lambda value: value.upper())

    expect(result.is_empty()).to(equal(True))


def test_should_transform_present_value_with_map() -> None:
    optional = Optional.of("hello")

    result = optional.map(lambda value: value.upper())

    expect(result.unwrap()).to(equal("HELLO"))


def test_should_raise_error_when_map_function_returns_none() -> None:
    optional = Optional.of("test")

    expect(lambda: optional.map(lambda x: None)).to(raise_error(ValueError))


def test_should_raise_custom_error_with_unwrap_or_raise_on_empty() -> None:
    optional = Optional.empty()

    expect(lambda: optional.unwrap_or_raise(lambda: RuntimeError("Custom error message"))).to(
        raise_error(RuntimeError, "Custom error message")
    )


def test_should_return_value_with_unwrap_or_raise_on_present_optional() -> None:
    value = "test_value"
    optional = Optional.of(value)

    result = optional.unwrap_or_raise(lambda: RuntimeError("Should not be called"))

    expect(result).to(equal(value))


def test_should_chain_multiple_map_operations() -> None:
    optional = Optional.of("  hello world  ")

    result = optional.map(str.strip).map(lambda value: value.upper()).map(lambda value: value.split())

    expect(result.unwrap()).to(equal(["HELLO", "WORLD"]))


def test_should_call_of_function_when_match_on_present_optional() -> None:
    value = "test_value"
    optional = Optional.of(value)

    result = optional.match(of=lambda v: f"processed: {v}", empty=lambda: "default")

    expect(result).to(equal("processed: test_value"))


def test_should_call_empty_function_when_match_on_empty_optional() -> None:
    optional = Optional.empty()

    result = optional.match(of=lambda v: f"processed: {v}", empty=lambda: "default")

    expect(result).to(equal("default"))


def test_should_execute_complex_operations_with_match() -> None:
    optional = Optional.of(42)

    result = optional.match(of=lambda n: n * 2 if n > 20 else n, empty=lambda: 0)

    expect(result).to(equal(84))


def test_should_handle_exceptions_in_match_functions() -> None:
    optional = Optional.of("test")

    expect(lambda: optional.match(of=lambda v: int(v), empty=lambda: 0)).to(raise_error(ValueError))


def test_should_not_allow_to_modify_value() -> None:
    optional = Optional.of("test")

    def modify_value() -> None:
        optional._value = "modified"

    expect(modify_value).to(raise_error(AttributeError))
