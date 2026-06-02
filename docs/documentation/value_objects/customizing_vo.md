# Customizing Value Objects

To create domain-specific value objects, extend one of the [primitive base classes](built_in_vo.md) and add 
[custom validation methods](validation.md#custom-validations) decorated with `@validate`. The validation methods are executed 
in the order they are defined in the class or by the order you specify using the `order` parameter in 
the `@validate` decorator.

## Creating Value Objects through Subclassing

The main goal for creating custom value objects is to encapsulate domain-specific validation logic and
express the ubiquitous language of your domain.

The fastest way to create these types of value objects is by subclassing one of the [built-in primitive types](built_in_vo.md).

```python
from value_objects import String


class ProductCode(String):
    ...
```

With no additional logic, the `ProductCode` class behaves exactly like a `String` value object but 
expresses the ubiquitous language of the domain better.

You can also specialize a value object and add custom validation logic using the `@validate` decorator as 
seen in the [previous section](validation.md#custom-validations)

```python
from value_objects import Integer, validate, SindriValidationError


class NegativeIntegerError(SindriValidationError):
    def __init__(self) -> None:
        super().__init__("The integer must be positive")


class PositiveInteger(Integer):
    @validate
    def _must_be_positive(self) -> None:
        if self._value <= 0:
            raise NegativeIntegerError
```

## Creating Own Value Objects from Scratch

If you find yourself needing a value object that is not implemented as a built-in primitives type,
you can create your own value object from scratch by subclassing the `ValueObject` base class.

```python
from datetime import date
from value_objects import ValueObject, validate, SindriValidationError


class Date(ValueObject[date]):
    @validate
    def _must_be_a_date(self) -> None:
        if not isinstance(self._value, date):
            raise SindriValidationError("The value must be a date")
```