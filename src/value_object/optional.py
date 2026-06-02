"""Optional value object pattern.

This module provides an :class:`Optional` wrapper that follows the value object
pattern. It is immutable, hashable, and supports pattern matching.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Generic, NoReturn, TypeVar

from value_object._compat import Self

_EMPTY: object = object()

T = TypeVar("T")
U = TypeVar("U")

__all__ = [
    "Optional",
    "raise_error",
]


def raise_error(exception: Exception) -> NoReturn:
    """Raise an exception, useful in match expressions for the absent branch."""
    raise exception


class Optional(Generic[T]):
    """Immutable wrapper for optional values.

    Can hold a value of any type, or be empty.

    Example:
        .. code-block:: python

            maybe_name: Optional[str] = Optional.of("Alice")
            maybe_name.unwrap()  # "Alice"
    """

    __slots__ = ("_value",)
    __match_args__ = ("_value",)

    _value: object

    def __init__(self, value: object = _EMPTY) -> None:
        object.__setattr__(self, "_value", value)

    @classmethod
    def of(cls, value: T) -> Self:
        if value is None:
            raise ValueError("of(None) is not valid. Use empty() instead.")
        return cls(value)

    @classmethod
    def empty(cls) -> Self:
        return cls(_EMPTY)

    @classmethod
    def lift(cls, value: U | None, mapper: Callable[[U], T]) -> Self:
        if value is None:
            return cls.empty()
        return cls.of(mapper(value))

    @classmethod
    def from_nullable(cls, value: T | None) -> Self:
        if value is not None:
            return cls.of(value)
        return cls.empty()

    def is_present(self) -> bool:
        return self._value is not _EMPTY

    def is_empty(self) -> bool:
        return self._value is _EMPTY

    def map(self, func: Callable[[T], U]) -> Optional[U]:
        if self.is_empty():
            return type(self).empty()  # type: ignore[return-value]
        return type(self).of(func(self._value))  # type: ignore[arg-type, return-value]

    def match(self, of: Callable[[T], U], empty: Callable[[], U]) -> U:
        if self.is_empty():
            return empty()
        return of(self._value)  # type: ignore[arg-type]

    def unwrap(self) -> T:
        if self.is_empty():
            raise ValueError("Cannot unwrap an empty Optional")
        return self._value  # type: ignore[return-value]

    def unwrap_or_raise(self, error_builder: Callable[[], Exception]) -> T:
        if self.is_empty():
            raise error_builder()
        return self._value  # type: ignore[return-value]

    def __repr__(self) -> str:
        if self.is_empty():
            return f"{self.__class__.__name__}.empty"
        return f"{self.__class__.__name__}({self._value!r})"

    def __str__(self) -> str:
        if self.is_empty():
            return "empty"
        return str(self._value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __setattr__(self, name: str, value: object) -> None:
        if name in self.__slots__:
            raise AttributeError("Cannot modify the value of an Optional")
        public_name = name.replace("_", "")
        public_slots = [slot.replace("_", "") for slot in self.__slots__]
        if public_name in public_slots:
            raise AttributeError("Cannot modify the value of an Optional")
        raise AttributeError(f"Class {self.__class__.__name__} object has no attribute '{name}'")
