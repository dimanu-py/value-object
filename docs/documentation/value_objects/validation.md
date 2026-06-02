# Validation Mechanism

The Validation System provides a decorator-based framework for ensuring data integrity across all [value objects](built_in_vo.md) 
in the library. It defines a consistent approach for validating input values, enforcing type safety, and raising 
meaningful error messages when validation fails. This system is the foundation that allows value objects to maintain 
their invariants and guarantees domain correctness.

The validation system is built on three core components:

- [`@validate` Decorator](#the-validate-decorator): a decorator that registers validation functions to be executed during value object 
initialization
- [Error Hierarchy](#error-hierarchy): a structured set of exception classes for different validation failure scenarios
- [Custom Validations](#custom-validations): specific validation logic implemented in each value object class

All validation occurs during value object construction after the value is assigned to the internal `_value` attribute, ensuring 
that invalid objects cannot exist in the system. 

!!! note "Extensibility"
    The framework is designed to be extensible, allowing developers to add custom validation rules 
    while maintaining consistency across the codebase.

## The `@validate` Decorator

This decorator is the central mechanism for defining validation functions. It can be applied to any method within a value
object class.

### Validation Method Signature

The decorator is applied to instance methods that access the value via `self._value`. Each decorated
method:

- Accesses the value being validated through `self._value`
- Performs a specific validation check
- Raises an appropriate exception if validation fails
- Returns None if validation passes

```python
from value_objects import ValueObject, validate


class YourValueObject(ValueObject[int]):
    @validate
    def _ensure_value_is_positive(self) -> None:
        # Your validation logic here - access value via self._value
        ...
```

### Handling Validation Order

When the value object is instantiated, the value is first assigned to `_value` and then all methods decorated with `@validate` are executed. 
The order of execution can be controlled in two ways:

1. **Definition Order**: By default, validation methods are executed in the order they are defined in the class.

    ```python
    from value_objects import ValueObject, validate, SindriValidationError
   
    class Integer(ValueObject[int]):
        @validate
        def _ensure_has_value(self) -> None:
            if self._value is None:
                raise SindriValidationError("Value is required")
    
        @validate
        def _ensure_value_is_integer(self) -> None:
            if not isinstance(self._value, int):
                raise SindriValidationError("Invalid type, expected int")
    ```

2. **Explicit Order**: You can specify an `order` parameter in the `@validate` decorator to control the sequence explicitly.

    ```python
    from value_objects import ValueObject, validate, SindriValidationError
    
    class Integer(ValueObject[int]):
        @validate(order=1)
        def _ensure_value_is_integer(self) -> None:
            if not isinstance(self._value, int):
                raise SindriValidationError("Invalid type, expected int")
   
        @validate(order=0)
        def _ensure_has_value(self) -> None:
            if self._value is None:
                raise SindriValidationError("Value is required")
    ```

## Error Hierarchy

The validation system defines a hierarchy of exception classes to represent different scenarios. All
validation errors inherit from the base `ValueObjectValidationError` class to be able to catch all
validation-related exceptions in a single except block if needed or in an error handler in a `FastAPI` applications.

### Built-in Validation Errors

All [built-in value objects](built_in_vo.md) raise specific exceptions to provide
more context about the type of failure:

- `RequiredValueError`: Raised when a required value is missing (e.g., `None`).
- `InvalidTypeError`: Raised when the value does not match the expected type.
- `InvalidIdFormatError`: Raised when an identifier value does not conform to the expected format.

These errors cannot be used directly in [custom value objects](customizing_vo.md), but you can create your own exceptions
and build your own hierarchy that inherits from `ValueObjectValidationError`.

## Custom validations

When creating [custom value object](customizing_vo.md), consider creating your own validation
methods and exceptions that inherit from `ValueObjectValidationError` to provide more specific error 
handling in your domain. 

You can still use directly `ValueObjectValidationError` for general validation errors, but custom exceptions can 
enhance clarity and maintainability.

```python
from value_objects import Float, validate, SindriValidationError


class NegativePriceError(SindriValidationError):
    def __init__(self, value: float) -> None:
        super().__init__(f"Price cannot have negative value, received '{value}'.")


class Price(Float):
    @validate
    def _ensure_value_is_positive(self) -> None:
        if self._value < 0:
            raise NegativePriceError(self._value)
```

!!! tip "Best Practices"
    - Use specific exception classes for different validation failures to improve error handling.
    - Provide clear and informative error messages to aid debugging and user feedback.
    - Keep validation methods focused on a single responsibility for clarity and maintainability.
