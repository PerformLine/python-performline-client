"""
Functions for working with lists
"""
from __future__ import absolute_import
from .types import isiterable


def flatten(value):
    if isiterable(value):
        out = []

        for i, v in enumerate(value):
            if isiterable(v):
                out += flatten(v)
            else:
                out.append(v)

        return out
    else:
        return value


def chunkwise(iterable, size=2):
    if size < 2:
        for v in iterable:
            yield v

    else:
        ilen = len(iterable)

        for i, _ in enumerate(iterable):
            if not (i % size):
                out = [iterable[i]]

                for j in xrange(size - 1):
                    if (i + j + 1) < ilen:
                        out.append(iterable[i + j + 1])
                    else:
                        out.append(None)

                yield tuple(out)
