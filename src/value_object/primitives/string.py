from value_object.decorators.validation import validate
from value_object.errors.incorrect_value_type_error import IncorrectValueTypeError
from value_object.errors.required_value_error import RequiredValueError
from value_object.value_object import ValueObject


class String(ValueObject[str]):
    """
    A value object that wraps string values with validation.

    This class provides a base implementation for creating value objects that
    represent string values in the domain. It ensures that the wrapped value
    is a valid string and not None.

    The class includes built-in validation for:
    - Required value (not None)
    - Type checking (must be a string)

    Inherits all functionality from ValueObject including immutability,
    equality comparison, string representation, and hashing.

    Example:
        ```python
        class Email(String):
            @validate
            def _validate_email_format(self) -> None:
                if "@" not in self._value:
                    raise ValueError("Invalid email format")

        email = Email("user@example.com")
        email.value  # 'user@example.com'
        ```
    """

    @validate
    def _ensure_has_value(self) -> None:
        if self._value is None:
            raise RequiredValueError

    @validate
    def _ensure_is_string(self) -> None:
        if not isinstance(self._value, str):
            raise IncorrectValueTypeError(self._value, str)
