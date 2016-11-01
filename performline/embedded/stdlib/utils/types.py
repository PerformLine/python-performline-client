"""
Python type system extensions and utilities.
"""
import six


PRIMITIVE_TYPES = (bool, int, float, complex, str, list, tuple, dict)

if six.PY2:
    PRIMITIVE_TYPES += (long, unicode)


def isprimitive(value):
    """
    Returns whether a given value is a primitive type or not.

    Args:
        value (any): The value to test.

    Returns:
        bool
    """

    if value is None or isinstance(value, PRIMITIVE_TYPES):
        return True

    return False
