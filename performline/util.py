# Copyright (c) 2016, PerformLine, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the company nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL PERFORMLINE, INC. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
    """
    Retrieve a value from the given dict, or raise a MissingKeyException if the path is not
    present. ``path`` can also retrieve values in nested dictionaries by specifying it as
    a slash (/) separated path:

    e.g.: "path/to/key" would return 1.5 from the following dict:

    {
        "path": {
            "to": {
                "key": 1.5,
            },
        },
    }

    Args:
        data (dict): A dictionary to retrieve a value from.

        path (str): A key or slash-separated key path to retrieve from ``data``.

    Returns:
        The value pointed to by ``path``.

    Raises:
        MissingKeyException
    """
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
    """
    Operates identically to :func:`performline.util.must_get()`, but will catch a
    MissingKeyException and return a ``fallback`` value instead.

    Args:
        data (dict): A dictionary to retrieve a value from.

        path (str): A key or slash-separated key path to retrieve from ``data``.

    Returns:
        The value pointed to by ``path``, or ``fallback`` if the given path does not exist.

    """
    try:
        return must_get(data, path)
    except MissingKeyException:
        return fallback


def camelize(value, upperFirst=False):
    """
    Convert a given string to a "camelCase" or "PascalCase" string.

    Args:
        value (str): The string to reformat.

        upperFirst (bool): Whether to return the string formatted in "camelCase" (False) or
            as "PascalCase" (True).

    Returns:
        The formatted version of ``value``.
    """
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
