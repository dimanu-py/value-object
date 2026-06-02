# Validator Signature Migration Guide

## Overview

This guide helps you migrate your custom value object validators to the new signature introduced in sindripy v1.0.0. 
The change simplifies validator method signatures and reduces code repetition.

### What Changed?

**Before (Old Behavior):**

- Value was validated **before** being assigned to `_value`
- Validators received the value as a parameter: `method(self, value: T)`
- Value assignment happened only after all validators passed

**After (New Behavior):**

- Value is assigned to `_value` first, then validated
- Validators access the value directly via `self._value`: `method(self)`
- Cleaner signatures, no repetitive parameter passing

### Migration Benefits

✅ **Cleaner Code**: No need to pass `value` parameter to every validator  
✅ **Less Repetition**: Eliminates repetitive parameter passing in complex validation chains  
✅ **Better Readability**: Validators are more focused on their specific validation logic  
✅ **Maintained Safety**: Validators still execute immediately after value assignment  

---

## Step-by-Step Migration

### Step 1: Identify Validators to Update

Find all methods in your value objects decorated with `@validate`:

```python
class YourValueObject(ValueObject[str]):
    @validate
    def _your_validator(self, value: str) -> None:  # OLD - needs update
        pass
```

### Step 2: Update Method Signatures

Remove the `value` parameter from validator methods signatures:

**Before:**
```python
@validate
def _your_validator(self, value: str) -> None:
    if len(value) < 3:
        raise ValueError("Too short")
```
**After:**
```python
@validate
def _your_validator(self) -> None:
    if len(self._value) < 3:
        raise ValueError("Too short")
```

### Step 3: Update Validation Logic

Replace all `value` references with `self._value`:

```python
class ProductName(ValueObject[str]):
    @validate
    def _validate_not_empty(self) -> None:  # Changed signature
        if not self._value.strip():  # Changed from 'value'
            raise ValueError("Product name cannot be empty")

    @validate(order=2)
    def _validate_length(self) -> None:  # Changed signature
        if len(self._value) > 100:  # Changed from 'value'
            raise ValueError("Product name too long")
```

---

## Complete Migration Examples

### Example 1: Simple String Validation

**Before:**
```python
class Username(ValueObject[str]):
    @validate
    def _validate_not_empty(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Username cannot be empty")

    @validate(order=1)
    def _validate_length(self, value: str) -> None:
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters")
```

**After:**
```python
class Username(ValueObject[str]):
    @validate
    def _validate_not_empty(self) -> None:
        if not self._value.strip():
            raise ValueError("Username cannot be empty")

    @validate(order=1)
    def _validate_length(self) -> None:
        if len(self._value) < 3:
            raise ValueError("Username must be at least 3 characters")
```

### Example 2: Complex Validation with Order

**Before:**
```python
class Price(ValueObject[float]):
    @validate(order=1)
    def _validate_type(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise InvalidTypeError("Price must be numeric")

    @validate(order=2)
    def _validate_positive(self, value: float) -> None:
        if value < 0:
            raise ValueError("Price cannot be negative")

    @validate(order=3)
    def _validate_precision(self, value: float) -> None:
        if abs(value - round(value, 2)) > 0.0001:
            raise ValueError("Price cannot have more than 2 decimal places")
```

**After:**
```python
class Price(ValueObject[float]):
    @validate(order=1)
    def _validate_type(self) -> None:
        if not isinstance(self._value, (int, float)):
            raise InvalidTypeError("Price must be numeric")

    @validate(order=2)
    def _validate_positive(self) -> None:
        if self._value < 0:
            raise ValueError("Price cannot be negative")

    @validate(order=3)
    def _validate_precision(self) -> None:
        if abs(self._value - round(self._value, 2)) > 0.0001:
            raise ValueError("Price cannot have more than 2 decimal places")
```

### Example 3: Custom Exception Classes

**Before:**
```python
class NegativeAgeError(SindriValidationError):
    def __init__(self, value: int) -> None:
        super().__init__(f"Age cannot be negative, received {value}")

class Age(ValueObject[int]):
    @validate
    def _validate_positive(self, value: int) -> None:
        if value < 0:
            raise NegativeAgeError(value)
```

**After:**
```python
class NegativeAgeError(SindriValidationError):
    def __init__(self, value: int) -> None:
        super().__init__(f"Age cannot be negative, received {value}")

class Age(ValueObject[int]):
    @validate
    def _validate_positive(self) -> None:
        if self._value < 0:
            raise NegativeAgeError(self._value)
```

---

## Need Help?

- Check the [Validation Mechanism documentation](validation.md) for updated examples
- Review [Customizing Value Objects](customizing_vo.md) for more patterns
- Open an issue on GitHub for migration questions

---

## Backward Compatibility

For a transition period, `sindripy` provides an adapter that automatically detects and supports both old and new validator signatures. 
However, we recommend migrating to the new signature as soon as possible for cleaner code and future compatibility.