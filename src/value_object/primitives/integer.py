from value_object.decorators.validation import validate
from value_object.errors.incorrect_value_type_error import IncorrectValueTypeError
from value_object.errors.required_value_error import RequiredValueError
from value_object.value_object import ValueObject


class Integer(ValueObject[int]):
    """
    A value object that wraps integer values with validation.

    This class provides a base implementation for creating value objects that
    represent integer values in the domain. It ensures that the wrapped value
    is a valid integer and not None.

    The class includes built-in validation for:
    - Required value (not None)
    - Type checking (must be an integer)

    Inherits all functionality from ValueObject including immutability,
    equality comparison, string representation, and hashing.

    Example:
        ```python
        class Age(Integer):
            @validate
            def _validate_positive(self) -> None:
                if self._value < 0:
                    raise ValueError("Age cannot be negative")

        age = Age(25)
        age.value  # 25
        str(age)  # '25'
        ```
    """

    @validate
    def _ensure_has_value(self) -> None:
        if self._value is None:
            raise RequiredValueError

    @validate
    def _ensure_value_is_integer(self) -> None:
        if not isinstance(self._value, int):
            raise IncorrectValueTypeError(self._value, int)
