from enum import Enum
from typing import Any

import pytest
from expects import equal, expect, raise_error

from value_object.aggregate_root import AggregateRoot
from value_object.primitives.string import String
from value_object.value_object import ValueObject

pytestmark = pytest.mark.unit


class Order(AggregateRoot):
    def __init__(self, order_id: str, customer_id: int, total: float) -> None:
        self.order_id = order_id
        self.customer_id = customer_id
        self.total = total


class Category(AggregateRoot):
    def __init__(self, category_id: int, name: str) -> None:
        self.category_id = category_id
        self.name = name


class AggregateWithProtectedAttribute(AggregateRoot):
    def __init__(self, visible: str, protected: str) -> None:
        self.visible = visible
        self._protected = protected


class AggregateWithPrivateAttribute(AggregateRoot):
    def __init__(self, visible: str, private: str) -> None:
        self.visible = visible
        self.__private = private


class Customer(AggregateRoot):
    def __init__(self, customer_id: int, name: str, email: str | None = None) -> None:
        self.customer_id = customer_id
        self.name = name
        self.email = email


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class StatusValueObject(ValueObject[Status]):
    pass


class AggregateWithValueObjectAttribute(AggregateRoot):
    def __init__(self, name: String) -> None:
        self.name = name


class AggregateWithEnumAttribute(AggregateRoot):
    def __init__(self, status: Status) -> None:
        self.status = status


class AggregateWithValueObjectWrappingEnum(AggregateRoot):
    def __init__(self, status: StatusValueObject) -> None:
        self.status = status


class LineItem(AggregateRoot):
    def __init__(self, product_id: str, quantity: int) -> None:
        self.product_id = product_id
        self.quantity = quantity


class Cart(AggregateRoot):
    def __init__(self, item: LineItem, item_count: int) -> None:
        self.item = item
        self.item_count = item_count


class ObjectWithValueAttribute:
    def __init__(self, value: str) -> None:
        self.value = value


class ObjectWithToPrimitives:
    def to_primitives(self) -> dict[str, Any]:
        return {"ducked": True}


class AggregateWithDuckTypedValue(AggregateRoot):
    def __init__(self, duck_value: ObjectWithValueAttribute) -> None:
        self.duck_value = duck_value


class AggregateWithDuckTypedPrimitives(AggregateRoot):
    def __init__(self, duck_primitives: ObjectWithToPrimitives) -> None:
        self.duck_primitives = duck_primitives


def test_should_represent_aggregate_attributes_in_assignment_order() -> None:
    order = Order(order_id="ORD-001", customer_id=123, total=99.99)

    expect(repr(order)).to(equal("Order(order_id='ORD-001', customer_id=123, total=99.99)"))


def test_should_strip_leading_underscore_from_protected_attribute_in_repr() -> None:
    aggregate = AggregateWithProtectedAttribute(visible="public", protected="hidden")

    expect(repr(aggregate)).to(equal("AggregateWithProtectedAttribute(visible='public', protected='hidden')"))


def test_should_exclude_private_attribute_from_repr() -> None:
    aggregate = AggregateWithPrivateAttribute(visible="public", private="secret")

    expect(repr(aggregate)).to(equal("AggregateWithPrivateAttribute(visible='public')"))


def test_should_be_equal_when_same_class_and_same_attribute_values() -> None:
    first_order = Order(order_id="ORD-001", customer_id=123, total=99.99)
    second_order = Order(order_id="ORD-001", customer_id=123, total=99.99)

    expect(first_order).to(equal(second_order))


def test_should_not_be_equal_when_same_class_and_different_attribute_values() -> None:
    first_category = Category(category_id=1, name="Electronics")
    second_category = Category(category_id=2, name="Books")

    expect(first_category).to_not(equal(second_category))


def test_should_not_be_equal_when_different_classes() -> None:
    order = Order(order_id="ORD-001", customer_id=123, total=99.99)
    category = Category(category_id=1, name="Electronics")

    expect(order).to_not(equal(category))


def test_should_not_be_equal_to_an_unrelated_type() -> None:
    order = Order(order_id="ORD-001", customer_id=123, total=99.99)

    expect(order == 5).to(equal(False))


def test_should_ignore_private_attribute_when_comparing_equality() -> None:
    first_aggregate = AggregateWithPrivateAttribute(visible="public", private="first_secret")
    second_aggregate = AggregateWithPrivateAttribute(visible="public", private="second_secret")

    expect(first_aggregate).to(equal(second_aggregate))


def test_should_create_aggregate_from_primitives() -> None:
    customer = Customer.from_primitives({"customer_id": 42, "name": "Alice Smith"})

    expect(customer).to(equal(Customer(customer_id=42, name="Alice Smith")))


def test_should_create_aggregate_from_primitives_overriding_default_parameter() -> None:
    customer = Customer.from_primitives({"customer_id": 42, "name": "Alice Smith", "email": "alice@example.com"})

    expect(customer.email).to(equal("alice@example.com"))


def test_should_raise_error_when_primitives_is_not_a_dictionary() -> None:
    expect(lambda: Customer.from_primitives(["not", "a", "dict"])).to(raise_error(TypeError))  # type: ignore[arg-type]


def test_should_raise_error_when_primitives_has_non_string_keys() -> None:
    expect(lambda: Customer.from_primitives({1: "Alice"})).to(raise_error(TypeError))  # type: ignore[dict-item]


def test_should_raise_error_when_required_parameter_is_missing() -> None:
    expect(lambda: Customer.from_primitives({"name": "Bob"})).to(raise_error(ValueError))


def test_should_raise_error_when_extra_parameter_is_provided() -> None:
    primitives = {"customer_id": 1, "name": "Charlie", "age": 30}

    expect(lambda: Customer.from_primitives(primitives)).to(raise_error(ValueError))


def test_should_convert_plain_attributes_to_primitives() -> None:
    order = Order(order_id="ORD-001", customer_id=123, total=99.99)

    expect(order.to_primitives()).to(equal({"order_id": "ORD-001", "customer_id": 123, "total": 99.99}))


def test_should_unwrap_value_object_attribute_to_primitives() -> None:
    aggregate = AggregateWithValueObjectAttribute(name=String("hello"))

    expect(aggregate.to_primitives()).to(equal({"name": "hello"}))


def test_should_convert_enum_attribute_to_its_value_in_primitives() -> None:
    aggregate = AggregateWithEnumAttribute(status=Status.ACTIVE)

    expect(aggregate.to_primitives()).to(equal({"status": "active"}))


def test_should_recursively_convert_nested_aggregate_to_primitives() -> None:
    cart = Cart(item=LineItem(product_id="SKU-1", quantity=2), item_count=1)

    expect(cart.to_primitives()).to(equal({"item": {"product_id": "SKU-1", "quantity": 2}, "item_count": 1}))


def test_should_exclude_private_attribute_from_primitives() -> None:
    aggregate = AggregateWithPrivateAttribute(visible="public", private="secret")

    expect(aggregate.to_primitives()).to(equal({"visible": "public"}))


def test_should_convert_duck_typed_object_with_to_primitives_method() -> None:
    aggregate = AggregateWithDuckTypedPrimitives(duck_primitives=ObjectWithToPrimitives())

    expect(aggregate.to_primitives()).to(equal({"duck_primitives": {"ducked": True}}))


def test_should_unwrap_duck_typed_object_with_value_attribute() -> None:
    aggregate = AggregateWithDuckTypedValue(duck_value=ObjectWithValueAttribute(value="ducked"))

    expect(aggregate.to_primitives()).to(equal({"duck_value": "ducked"}))


def test_should_double_unwrap_value_object_wrapping_an_enum() -> None:
    aggregate = AggregateWithValueObjectWrappingEnum(status=StatusValueObject(Status.ACTIVE))

    expect(aggregate.to_primitives()).to(equal({"status": "active"}))
