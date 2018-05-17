"""
String formatting and manipulation functions.
"""
from __future__ import absolute_import
import re
import six


WORD_OMIT = r'[\W\s\_\-]+'
WORD_SPLIT = re.compile(r'(?:([A-Z][^A-Z]*)|' + WORD_OMIT + ')')
CAMEL_STRIP = re.compile(WORD_OMIT)


def camelize(value, upperFirst=False):
    """
    Convert a string into "camelCase" or "PascalCase".

    Args:
        value (str): The string to convert.

        upperFirst (bool, optional): Whether to produce "camelCase" or
            "PascalCase" (first letter capitalized).

    Returns:
        str
    """

    # split on word-separating characters (and discard them), or on capital
    # letters (preserving them)
    value = WORD_SPLIT.split(value)

    # filter out None and empty/only-whitespace strings from the list
    value = [x for x in value if x is not None and not x.strip() == '']

    # capitalize each word
    value = ''.join(x.title() for x in value)

    # do a final pass removing omitted characters from the value
    value = re.sub(WORD_OMIT, '', value)

    if upperFirst:
        # return PascalCase
        return value
    else:
        # return camelCase
        return value[0].lower() + value[1:]


def underscore(value, joiner='_'):
    """
    Convert a string into "snake_case" (words separated by underscores).

    Args:
        value (str): The string to convert.

        joiner (str, optional): The string to use when joining individual words
            if underscore (_) is not desired.

    Returns:
        str
    """
    # split on word-separating characters (and discard them), or on capital
    # letters (preserving them)
    value = WORD_SPLIT.split(value)

    # filter out None and empty/only-whitespace strings from the list
    value = [x for x in value if x is not None and not x.strip() == '']

    # lowercase each word and join
    return joiner.join(x.strip().lower() for x in value)


def autotype(value):
    if isinstance(value, basestring):
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        elif value.lower() == 'null':
            return None
        else:
            try:
                return int(value)
            except ValueError:
                pass

            try:
                return float(value)
            except ValueError:
                pass

    return value


def u(value):
    try:
        return six.u(value)
    except TypeError:
        return value