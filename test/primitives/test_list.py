from typing import Any

import pytest
from expects import be_false, be_none, be_true, equal, expect, raise_error
from object_mother.primitives.list_primitives_mother import ListPrimitivesMother

from value_object.aggregate import Aggregate
from value_object.errors.incorrect_value_type_error import IncorrectValueTypeError
from value_object.errors.required_value_error import RequiredValueError
from value_object.primitives.list import List
from value_object.primitives.string import String

pytestmark = pytest.mark.unit


class Strings(List[str]): ...


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(ListPrimitivesMother.empty(), id="empty string list"),
        pytest.param(["hello", "world", "test"], id="multiple strings list"),
    ],
)
def test_should_create_string_list_value_object(value: list[str]) -> None:
    strings = Strings(value)

    expect(strings.value).to(equal(value))


def test_should_create_from_primitives_with_primitive_types() -> None:
    primitive_list = ["a", "b", "c", "d", "e"]

    strings = Strings.from_primitives(primitive_list)

    expect(strings.value).to(equal(primitive_list))


def test_should_create_from_primitives_with_empty_list() -> None:
    empty_list = Strings.from_primitives([])

    expect(empty_list.value).to(equal([]))


def test_should_create_from_primitives_with_value_objects() -> None:
    class Email(String): ...

    class Emails(List[Email]): ...

    primitive_emails = ["john@example.com", "jane@example.com", "bob@example.com"]

    emails = Emails.from_primitives(primitive_emails)

    expect(len(emails)).to(equal(len(primitive_emails)))
    expected_emails = [Email(email) for email in primitive_emails]
    expect(emails.value).to(equal(expected_emails))


def test_should_create_from_primitives_with_aggregates() -> None:
    class Person(Aggregate):
        def __init__(self, name: str, age: int, email: str):
            self.name = name
            self.age = age
            self.email = email

    class People(List[Person]): ...

    primitive_persons = [
        {"name": "John Doe", "age": 30, "email": "john@example.com"},
        {"name": "Jane Smith", "age": 25, "email": "jane@example.com"},
    ]

    persons = People.from_primitives(primitive_persons)

    expect(len(persons)).to(equal(len(primitive_persons)))
    expected_persons = [Person(**person) for person in primitive_persons]
    expect(persons.value).to(equal(expected_persons))


def test_should_raise_error_when_trying_to_create_list_of_value_objects_with_primitives() -> None:
    class Email(String): ...

    class Emails(List[Email]): ...

    primitive_list = ["john@example.com", "jane@example.com", "bob@example.com"]

    expect(lambda: Emails(primitive_list)).to(raise_error(IncorrectValueTypeError))


def test_should_raise_error_when_value_is_none() -> None:
    expect(lambda: Strings(None)).to(raise_error(RequiredValueError))


def test_should_raise_error_for_unparameterized_subclass() -> None:
    def create_unparameterized_subclass():
        class InvalidList(List): ...

        return InvalidList

    expect(create_unparameterized_subclass).to(raise_error(TypeError))


@pytest.mark.parametrize(
    "invalid_value",
    [
        pytest.param(42, id="integer value"),
        pytest.param(3.14, id="float value"),
        pytest.param(True, id="boolean value"),
        pytest.param({"a": 1, "b": 2}, id="dict value"),
        pytest.param([1, 2, 3, 4], id="list of integers"),
        pytest.param([1, 2, "three"], id="list with mixed types"),
    ],
)
def test_should_raise_error_when_value_has_invalid_type(invalid_value: Any) -> None:
    expect(lambda: Strings(invalid_value)).to(raise_error(IncorrectValueTypeError))


def test_should_compare_equal_with_same_value() -> None:
    common_value = ["a", "b", "c"]
    first_list = Strings(common_value)
    second_list = Strings(common_value)

    expect(first_list).to(equal(second_list))


def test_should_not_be_equal_with_different_values() -> None:
    first_list = Strings(["a", "b", "c"])
    second_list = Strings(["d", "e", "f"])

    expect(first_list).to_not(equal(second_list))


def test_should_not_be_equal_with_different_order() -> None:
    first_list = Strings(["a", "b", "c"])
    second_list = Strings(["c", "b", "a"])

    expect(first_list).to_not(equal(second_list))


def test_should_not_allow_to_modify_value() -> None:
    strings = Strings(["a", "b", "c"])

    def modify_value() -> None:
        strings._value = ["x", "y", "z"]

    expect(modify_value).to(raise_error(AttributeError))


def test_should_not_affect_original_list_when_modified() -> None:
    original_value = ["a", "b", "c"]
    strings = Strings(original_value)

    original_value.append("d")

    expect(strings.value).to(equal(original_value))


def test_should_evaluate_when_element_belongs_to_list() -> None:
    strings = Strings(["a", "b", "c", "d", "e"])

    expect("a" in strings).to(be_true)
    expect("x" in strings).to(be_false)


def test_should_support_membership_testing_with_empty_list() -> None:
    empty_strings = Strings([])

    expect(1 in empty_strings).to(be_false)


def test_should_support_iteration() -> None:
    strings = Strings(["a", "b", "c"])
    result = []

    for string in strings:
        result.append(string)

    expect(result).to(equal(["a", "b", "c"]))


def test_should_support_list_conversion() -> None:
    strings = Strings(["a", "b", "c"])

    expect(list(strings)).to(equal(["a", "b", "c"]))


def test_should_support_length_operation() -> None:
    value = ["a", "b", "c", "d", "e"]
    strings = Strings(value)

    expect(len(strings)).to(equal(len(value)))


def test_should_support_reversed_iteration() -> None:
    strings = Strings(["a", "b", "c"])

    expect(list(reversed(strings))).to(equal(["c", "b", "a"]))


def test_should_support_reversed_iteration_with_empty_list() -> None:
    empty_list = Strings([])

    expect(list(reversed(empty_list))).to(equal([]))


def test_should_be_hashable() -> None:
    strings = Strings(["a", "b", "c"])

    hash_value = hash(strings)
    expect(hash_value).to_not(be_none)


def test_should_have_same_hash_for_equal_lists() -> None:
    value = ["a", "b", "c"]
    first_list = Strings(value)
    second_list = Strings(value)

    expect(hash(first_list)).to(equal(hash(second_list)))


def test_should_have_different_hash_for_different_lists() -> None:
    first_list = Strings(["a", "b", "c"])
    second_list = Strings(["d", "e", "f"])

    expect(hash(first_list)).to_not(equal(hash(second_list)))


def test_should_be_usable_in_set() -> None:
    first_list = Strings(["a", "b", "c"])
    second_list = Strings(["d", "e", "f"])
    duplicated_list = Strings(["a", "b", "c"])

    strings_as_set = {first_list, second_list, duplicated_list}

    expect(len(strings_as_set)).to(equal(2))


def test_should_be_usable_as_dict_key() -> None:
    first_list = Strings(["a", "b", "c"])
    second_list = Strings(["d", "e", "f"])

    dict_with_list_keys = {first_list: "first", second_list: "second"}

    expect(dict_with_list_keys[first_list]).to(equal("first"))
    expect(dict_with_list_keys[second_list]).to(equal("second"))


def test_should_handle_nested_lists() -> None:
    class NestedList(List[list[int]]):
        pass

    nested_data = [[1, 2], [3, 4], [5, 6]]

    nested_list = NestedList(nested_data)

    expect(len(nested_list)).to(equal(3))
    expect(nested_list.value[0]).to(equal([1, 2]))


def test_should_work_with_list_comprehensions() -> None:
    class Integers(List[int]): ...

    numbers = Integers([1, 2, 3, 4, 5])

    doubled = [x * 2 for x in numbers]
    filtered = [x for x in numbers if x > 3]

    expect(doubled).to(equal([2, 4, 6, 8, 10]))
    expect(filtered).to(equal([4, 5]))


def test_should_support_unpacking() -> None:
    strings = Strings(["a", "b", "c"])

    first, second, third = strings

    expect(first).to(equal("a"))
    expect(second).to(equal("b"))
    expect(third).to(equal("c"))
