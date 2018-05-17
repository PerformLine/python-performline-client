"""
Functions for performing thread-safe operations.
"""
from __future__ import absolute_import
from multiprocessing import RawValue, Lock


class Counter(object):
    def __init__(self, value=0):
        self.val = RawValue('i', value)
        self.lock = Lock()

    def increment(self, amount=1):
        with self.lock:
            self.val.value += amount

    @property
    def value(self):
        with self.lock:
            return self.val.value

    def __int__(self):
        return int(self.value)
