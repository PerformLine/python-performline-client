from __future__ import absolute_import
from unittest import TestCase
from .convert import convert_to


class UtilsConvertTest(TestCase):
    def test_convert_size(self):
        self.assertEqual(convert_to(1, ''), '1B')
        self.assertEqual(convert_to(1024, ''), '1024B')
        self.assertEqual(convert_to(1024**2, ''), '%dB' % 1024**2)
        self.assertEqual(convert_to(1024**3, ''), '%dB' % 1024**3)
        self.assertEqual(convert_to(1024**4, ''), '%dB' % 1024**4)
        self.assertEqual(convert_to(1024**5, ''), '%dB' % 1024**5)
        self.assertEqual(convert_to(1024**6, ''), '%dB' % 1024**6)
        self.assertEqual(convert_to(1024**7, ''), '%dB' % 1024**7)
        self.assertEqual(convert_to(1024**8, ''), '%dB' % 1024**8)
        self.assertEqual(convert_to(1024**9, ''), '%dB' % 1024**9)

        self.assertEqual(convert_to(1, 'K'), '0KB')
        self.assertEqual(convert_to(1024, 'K'), '1KB')
        self.assertEqual(convert_to(1024**2, 'K'), '%dKB' % 1024**1)
        self.assertEqual(convert_to(1024**3, 'K'), '%dKB' % 1024**2)
        self.assertEqual(convert_to(1024**4, 'K'), '%dKB' % 1024**3)
        self.assertEqual(convert_to(1024**5, 'K'), '%dKB' % 1024**4)
        self.assertEqual(convert_to(1024**6, 'K'), '%dKB' % 1024**5)
        self.assertEqual(convert_to(1024**7, 'K'), '%dKB' % 1024**6)
        self.assertEqual(convert_to(1024**8, 'K'), '%dKB' % 1024**7)
        self.assertEqual(convert_to(1024**9, 'K'), '%dKB' % 1024**8)
