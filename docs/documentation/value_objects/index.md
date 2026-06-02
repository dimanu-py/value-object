# Value Objects

This document provides a comprehensive overview of the Value Object pattern implementation 
in the `value-object-sindri` library. 

For detailed information on specific value object types, see:

- [Built-in value objects](built_in_vo.md)
- [Validation framework and custom rules](validation.md)
- [Creating custom value objects](customizing_vo.md)
- [Domain aggregates and entities](aggregate_roots.md)
- [Migration Guide for validator signature changes](migration_guide.md)

## Pattern Overview

Value object pattern is a design pattern that emphasizes the use of immutable objects to represent
values in a system. It encourages the creation of small, focused classes that encapsulate domain logic.

They act as behavior magnets and try to avoid the code smells of anemic domain models and primitive obsession among others.

Value objects are characterized by:

- **Immutability**: Once created, a value object's state cannot be changed
- **Value** equality: Two value objects are equal if their values are equal, regardless of identity
- **Self**-validation: Value objects validate their state upon construction
- **Domain** semantics: They represent meaningful concepts in the domain rather than primitive types

In this implementation, all value objects inherit from the generic `ValueObject[T]` base class, 
where `T` represents the underlying primitive type being wrapped.

## Base Value Object Class

The `ValueObject[T]` base class provides core functionality for all value objects in the library:

| Feature               | Description                                           | Implementation                           |
|-----------------------|-------------------------------------------------------|------------------------------------------|
| Type Parameter        | Generic type `T` specifies the wrapped primitive type | `class ValueObject[T]`                   |
| Value Storage         | Internal `_value` attribute stores the wrapped value  | Private attribute `_value: T`            |
| Immutability          | Prevents modification after construction              | No public setters, frozen internal state |
| Equality              | Value-based equality comparison                       | `__eq__` compares `_value` attributes    |
| Hashing               | Hashable for use in sets and as dict keys             | `__hash__` based on `_value`             |
| String Representation | Human-readable and debug representations              | `__str__` and `__repr__` methods         |
| Value Access          | Read-only access to the wrapped value                 | `value` property                         |
| Validation            | Hooks for custom validation logic                     | `@validate` decorator                    |

!!! note "Subclassing"
    The `ValueObject` class is designed to be subclassed for specific value object types.
    It provides a solid foundation for building domain-specific value objects with consistent behavior.

## Value Object Features

### Immutability

Value objects in this library are **immutable** by design:

- The internal `_value` attribute is set once during construction
- No public methods modify the internal state
- Methods that appear to modify return new instances instead

This immutability ensures:

- Thread safety
- Predictable behavior in concurrent contexts
- Safe use as dictionary keys
- Prevention of unintended side effects

### Equality

Equality between two value objects is based on their values. This comparison is made
by overriding the `__eq__` method and comparing the wrapped `_value` attributes:

- Two value objects are equal if their `_value` attributes are equal
- Identity (memory address) is not considered in equality checks
- This allows for meaningful comparisons based on domain semantics

### Hashing

As immutable objects, value objects can also be hashed based on their values. The `__hash__` method
is overridden to compute the hash based on the `_value` attribute, allowing value objects to be
used in sets and as dictionary keys.

### String Representation

Value objects provide human-readable and debug-friendly string representations by overriding
the `__str__` and `__repr__` methods. This makes it easier to inspect value objects during debugging
and logging.

### Validation

Value objects can include custom validation logic to ensure that their values meet specific
domain constraints. This is achieved using the `@validate` decorator, which allows you to define
validation methods that are automatically called after the value is assigned to `_value` during construction.

For more details on validation, see the [Validation Mechanism](validation.md) section.

### Value Access

Value objects provide read-only access to their wrapped values through the `value` property.

This property returns the internal `_value` attribute, allowing you to retrieve the underlying
primitive value without exposing the internal state for modification.

```python
from value_object import String

username = String("john_doe")
print(username.value)  # john_doe
```
