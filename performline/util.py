from __future__ import unicode_literals
from __future__ import absolute_import
import re

CAMEL_OMIT = r'[\W\s\_\-]+'
CAMEL_SPLIT = re.compile(r'(?:([A-Z][^A-Z]*)|'+CAMEL_OMIT+')')
CAMEL_STRIP = re.compile(CAMEL_OMIT)
DATA_ELEMENT_SEPARATOR = '/'


class MissingKeyException(Exception):
    pass


def must_get(data, path):
    if not isinstance(data, dict):
        raise Exception("Response data is unavailable")

    current = data
    parts = path.split(DATA_ELEMENT_SEPARATOR)

    for i in range(0, len(parts)):
        if isinstance(current, dict) and parts[i] in current:
            current = current[parts[i]]
        else:
            raise MissingKeyException("Cannot retrieve data element '%s'", path)

    return current


def get(data, path, fallback=None):
    try:
        return must_get(data, path)
    except MissingKeyException:
        return fallback


def camelize(value, upperFirst=False):
    # split on word-separating characters (and discard them), or on capital
    # letters (preserving them)
    value = CAMEL_SPLIT.split(value)

    # filter out None and empty/only-whitespace strings from the list
    value = [x for x in value if x is not None and not x.strip() == '']

    # capitalize each word
    value = ''.join(x.title() for x in value)

    # do a final pass removing omitted characters from the value
    value = re.sub(CAMEL_STRIP, '', value)

    if upperFirst:
        # return PascalCase
        return value
    else:
        # return camelCase
        return value[0].lower() + value[1:]
