from uuid import UUID

from value_object.decorators.validation import validate
from value_object.errors.incorrect_value_type_error import IncorrectValueTypeError
from value_object.errors.invalid_id_format_error import InvalidIdFormatError
from value_object.errors.required_value_error import RequiredValueError
from value_object.value_object import ValueObject


class StringUuid(ValueObject[str]):
    """
    A value object that wraps UUID (Universally Unique Identifier) string values with validation.

    This class provides a specialized implementation for creating value objects that
    represent UUID values in the domain. It ensures that the wrapped value is a
    valid UUID string format and not None.

    The class includes built-in validation for:
    - Required value (not None)
    - Type checking (must be a string)
    - UUID format validation (must be a valid UUID format)

    Inherits all functionality from ValueObject including immutability,
    equality comparison, string representation, and hashing.

    Example:
        ```python
        class UserId(StringUuid):
            @validate
            def _validate_version(self) -> None:
                parsed_uuid = UUID(self._value)
                if parsed_uuid.version != 4:
                    raise ValueError("Only UUID version 4 allowed")

        user_id = UserId("123e4567-e89b-12d3-a456-426614174000")
        user_id.value  # '123e4567-e89b-12d3-a456-426614174000'
        ```
    """

    @validate
    def _ensure_has_value(self) -> None:
        if self._value is None:
            raise RequiredValueError

    @validate
    def _ensure_value_is_string(self) -> None:
        if not isinstance(self._value, str):
            raise IncorrectValueTypeError(self._value, str)

    @validate
    def _ensure_value_has_valid_uuid_format(self) -> None:
        try:
            UUID(self._value)
        except ValueError as error:
            raise InvalidIdFormatError from error
