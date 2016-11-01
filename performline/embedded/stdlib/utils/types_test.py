from __future__ import absolute_import
from unittest import TestCase
from .types import isprimitive
import six


class UtilsTypesTest(TestCase):
    def test_isprimitive(self):
        self.assertTrue(isprimitive(True))
        self.assertTrue(isprimitive(False))
        self.assertTrue(isprimitive(int(1)))
        self.assertTrue(isprimitive(float(1.0)))
        self.assertTrue(isprimitive(5j))
        self.assertTrue(isprimitive('1'))
        self.assertTrue(isprimitive([1]))
        self.assertTrue(isprimitive((1,)))
        self.assertTrue(isprimitive({1: True}))

        if six.PY2:
            self.assertTrue(isprimitive(long(1)))
            self.assertTrue(isprimitive(u'1'))

        self.assertFalse(isprimitive(Exception("1")))
        self.assertFalse(isprimitive(self))
        self.assertFalse(isprimitive(TestCase))
