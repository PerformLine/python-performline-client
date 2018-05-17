"""
Functions for retrieving data from and manipulating dictionaries.
"""
from __future__ import absolute_import
from copy import deepcopy
from .strings import camelize, underscore

DATA_ELEMENT_SEPARATOR = '/'


class MissingKeyException(Exception):
    pass


def must_deep_get(data, path):
    """
    Retrieve a deeply-nested dict key, raise an exception if it does not exist.

    Args:
        path (str): A slash (/) separated string that is used to locate a given deeply
            nested dict key.

    Returns:
        The requested dict key value.

    Raises:
        :class:`~performline.utils.dicts.MissingKeyException`
    """
    if not isinstance(data, dict):
        raise Exception("Response data is unavailable")

    current = data
    parts = path.split(DATA_ELEMENT_SEPARATOR)

    for i in range(0, len(parts)):
        if isinstance(current, dict) and parts[i] in current:
            current = current[parts[i]]
        else:
            raise MissingKeyException("Cannot retrieve dict element '%s'" % path)

    return current


def deep_get(data, path, fallback=None):
    """
    Retrieve a deeply-nested dict key, return ``fallback`` if it does not exist.

    Args:
        path (str): A slash (/) separated string that is used to locate a given deeply
            nested dict key.

        fallback (object, optional): A value to return if the specified path does not exist.

    Returns:
        The requested dict key value, or ``fallback``.
    """
    try:
        return must_deep_get(data, path)
    except MissingKeyException:
        return fallback


def camelize_dict(inValue, upperFirst=False):
    """
    Recursively applies the :func:`~performline.utils.strings.camelize` function to all key names
    in the given dictionary.

    Args:

        upperFirst (bool, optional): Whether the first letter in the camelized output should
            be capitalized (i.e. "PascalCase"), or should be lower case (i.e. "camelCase").

    Returns:
        The `dict` with changes applied.
    """

    return mutate_dict(inValue,
                       keyFn=camelize,
                       keyTypes=(str, unicode),
                       upperFirst=upperFirst)


def underscore_dict(inValue, joiner='_'):
    """
    Recursively applies the :func:`~performline.utils.strings.underscore` function to all key names
    in the given dictionary.

    Args:

        joiner (str, optional): The string used to join individual words in key names.

    Returns:
        The `dict` with changes applied.
    """

    return mutate_dict(inValue,
                       keyFn=underscore,
                       keyTypes=(str, unicode),
                       joiner=joiner)


def mutate_dict(inValue,
                keyFn=lambda k: k,
                valueFn=lambda v: v,
                keyTypes=None,
                valueTypes=None,
                **kwargs):
    """
    Takes an input dict or list-of-dicts and applies ``keyfn`` function to all of the keys in
    both the top-level and any nested dicts or lists, and ``valuefn`` to all

    If the input value is not of type `dict` or `list`, the value will be returned as-is.

    Args:
        inValue (any): The dict to mutate.

        keyFn (lambda): The function to apply to keys.

        valueFn (lambda): The function to apply to values.

        keyTypes (tuple, optional): If set, only keys of these types will be mutated
            with ``keyFn``.

        valueTypes (tuple, optional): If set, only values of these types will be mutated
            with ``valueFn``.

    Returns:
        A recursively mutated dict, list of dicts, or the value as-is (described above).
    """

    # this is here as a way of making sure that the various places where recursion is done always
    # performs the same call, preserving all arguments except for value (which is what changes
    # between nested calls).
    def recurse(value):
        return mutate_dict(value,
                           keyFn=keyFn,
                           valueFn=valueFn,
                           keyTypes=keyTypes,
                           valueTypes=valueTypes,
                           **kwargs)

    # handle dicts
    if isinstance(inValue, dict):
        # create the output dict
        outputDict = dict()

        # for each dict item...
        for k, v in inValue.items():
            # apply the keyFn to some or all of the keys we encounter
            if keyTypes is None or (isinstance(keyTypes, tuple) and isinstance(k, keyTypes)):
                # prepare the new key
                k = keyFn(k, **kwargs)

            # apply the valueFn to some or all of the values we encounter
            if valueTypes is None or (isinstance(valueTypes, tuple) and isinstance(v, valueTypes)):
                v = valueFn(v)

            # recurse depending on the value's type
            #
            if isinstance(v, dict):
                # recursively call mutate_dict() for nested dicts
                outputDict[k] = recurse(v)
            elif isinstance(v, list):
                # recursively call mutate_dict() for each element in a list
                outputDict[k] = [recurse(i) for i in v]
            else:
                # set the value straight up
                outputDict[k] = v

        # return the now-populated output dict
        return outputDict

    # handle lists-of-dicts
    elif isinstance(inValue, list) and len(inValue) > 0:
        return [recurse(i) for i in inValue]

    else:
        # passthrough non-dict value as-is
        return inValue


def compact(inDict, keep_if=lambda k, v: v is not None):
    """
    Takes a dictionary and returns a copy with elements matching a given lambda removed. The
    default behavior will remove any values that are `None`.

    Args:
        inDict (dict): The dictionary to operate on.

        keep_if (lambda(k,v), optional): A function or lambda that will be called for each
            (key, value) pair.  If the function returns truthy, the element will be left alone,
            otherwise it will be removed.
    """
    if isinstance(inDict, dict):
        return {
            k: v for k, v in inDict.items() if keep_if(k, v)
        }

    raise ValueError("Expected: dict, got: {0}".format(type(inDict)))


def merge(inDict, newDict):
    """
    Takes an input dictionary and updates a deep copy of it with the values from another
    dictionary, then returns the copy.

    Args:
        inDict (dict): The dictionary to copy.

        newDict (dict): The dictionary to merge into the copy.

    Returns:
        dict
    """

    d = deepcopy(inDict)
    d.update(newDict)
    return d


class dotdict(dict):
    """
    Provides dot.notation access to dictionary attributes
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
