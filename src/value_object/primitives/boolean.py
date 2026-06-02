from value_object.decorators.validation import validate
from value_object.errors.incorrect_value_type_error import IncorrectValueTypeError
from value_object.errors.required_value_error import RequiredValueError
from value_object.value_object import ValueObject


class Boolean(ValueObject[bool]):
    """
    A value object that wraps boolean values with validation.

    This class provides a base implementation for creating value objects that
    represent boolean values in the domain. It ensures that the wrapped value
    is a valid boolean and not None.

    The class includes built-in validation for:
    - Required value (not None)
    - Type checking (must be a boolean)

    Inherits all functionality from ValueObject including immutability,
    equality comparison, string representation, and hashing.

    Example:
        ```python
        class IsActive(Boolean):
             @validate
             def _validate_true_for_premium(self) -> None:
                 # Custom business logic can be added here
                 pass

        is_active = IsActive(True)
        is_active.value  # True
        str(is_active)  # 'True'
        ```
    """

    @validate
    def _ensure_has_value(self) -> None:
        if self._value is None:
            raise RequiredValueError

    @validate
    def _ensure_value_is_boolean(self) -> None:
        if not isinstance(self._value, bool):
            raise IncorrectValueTypeError(self._value, bool)
