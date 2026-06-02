# Built-in Value Objects

The library provides several built-in value object types.

All primitive value objects inherit from the generic [`ValueObject[T]`](index.md#base-value-object-class) base class and 
implement a consistent validation pattern using the `@validate` decorator. 
Each primitive type wraps a specific Python built-in type and enforces two core 
validations: 

- Ensuring the value is not `None`, otherwise raising a `RequiredValueError`.
- Ensuring the value matches the expected annotated type, otherwise raising an `InvalidTypeError`.

!!! note "Each value object type can be [extended and customized as needed](customizing_vo.md)."

## Boolean

The Boolean class wraps Python `bool` values and provides the foundation for creating domain-specific boolean value objects.

```python
from value_object import Boolean

is_active = Boolean(True)

print(is_active)  # True
```

## Integer

The Integer class wraps Python `int` values and provides the foundation for creating domain-specific integer value objects.

```python
from value_object import Integer

quantity = Integer(25)

print(quantity)  # 25
```

## Float

The Float class wraps Python `float` values and provides the foundation for creating domain-specific float value objects.

```python
from value_object import Float

price = Float(19.99)

print(price)  # 19.99
```

## String

The String class wraps Python `str` values and provides the foundation for creating domain-specific string value objects.

```python
from value_object import String

username = String("john_doe")

print(username)  # john_doe
```

## List

The List class wraps Python `list` values and provides the foundation for creating domain-specific list value objects.

`List[T]` wraps a Python `list` and must be subclassed with a type parameter. It 
enforces list-level and element-level constraints at runtime.

Following the same pattern as other value objects, it ensures the value is not None and is of type `list`.
Additionally, it validates that the class is typed with a specific type parameter and
enforces at runtime that all elements in the list match the specified type.

You can use this value object to wrap lists of primitive types or other value objects.

```python
from value_object import List, String


class Strings(List[str]): ...


class Email(String): ...


class Emails(List[Email]): ...
```

When creating a new instance you can pass a list of values matching the specified type
or delegate the instantiation of the elements to the value object itself through the `from_primitives`
named constructor:

```python
emails = Emails([Email("johndoe@gmail.com"), Email("dimanupy@hotmail.com")])

emails = Emails.from_primitives(["johndoe@gmail.com", "dimanupy@hotmail.com"])
```

## String UUID

Identifier value objects provide type-safe, validated wrappers around entity identifiers. 
Unlike primitive [`String`](#string) value objects, identifiers enforce specific format constraints 
(such as UUID format) and communicate intent in the domain model. They prevent mixing different types 
of identifiers (e.g., using a UserId where an OrderId is expected) through the type system.

The library currently provides `StringUuid` as the base identifier type, which validates UUID format strings.

```python
from value_object import StringUuid

user_id = StringUuid("550e8400-e29b-41d4-a716-446655440000")

print(user_id)  # 550e8400-e29b-41d4-a716-446655440000
```
