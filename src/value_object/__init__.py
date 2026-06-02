"""Public facade for value object implementations.

This module re-exports the most common value objects so they can be
imported directly from :mod:`value_objects`.
"""

__version__ = "0.1.0"

from value_object.aggregate import Aggregate
from value_object.decorators.validation import validate
from value_object.errors.sindri_validation_error import SindriValidationError
from value_object.identifiers.string_uuid import StringUuid
from value_object.primitives.boolean import Boolean
from value_object.primitives.float import Float
from value_object.primitives.integer import Integer
from value_object.primitives.list import List
from value_object.primitives.string import String
from value_object.value_object import ValueObject

__all__ = [
    "Aggregate",
    "validate",
    "StringUuid",
    "Boolean",
    "Float",
    "Integer",
    "List",
    "String",
    "ValueObject",
    "SindriValidationError",
]
