from __future__ import absolute_import
from unittest import TestCase
from .strings import camelize, underscore, u


class UtilsStringTest(TestCase):
    def test_strings_camelize(self):
        """
        Test if camelize actually camelizes various strings as expected
        """

        self.assertEqual(camelize('test_value'),       'testValue')
        self.assertEqual(camelize('test-Value'),       'testValue')
        self.assertEqual(camelize('test value'),       'testValue')
        self.assertEqual(camelize('TestValue'),        'testValue')
        self.assertEqual(camelize('testValue'),        'testValue')
        self.assertEqual(camelize('TeSt VaLue'),       'teStVaLue')

        self.assertEqual(camelize('test_value', True), 'TestValue')
        self.assertEqual(camelize('test-Value', True), 'TestValue')
        self.assertEqual(camelize('test value', True), 'TestValue')
        self.assertEqual(camelize('TestValue',  True), 'TestValue')
        self.assertEqual(camelize('testValue',  True), 'TestValue')
        self.assertEqual(camelize('TeSt VaLue', True), 'TeStVaLue')

    def test_strings_underscore(self):
        """
        Test if underscore actually underscores various strings as expected
        """

        self.assertEqual(underscore('test_value'),                   'test_value')
        self.assertEqual(underscore('test-Value'),                   'test_value')
        self.assertEqual(underscore('test value'),                   'test_value')
        self.assertEqual(underscore('TestValue'),                    'test_value')
        self.assertEqual(underscore('testValue'),                    'test_value')
        self.assertEqual(underscore('TeSt VaLue'),                   'te_st_va_lue')

        self.assertEqual(underscore('test_value', joiner='-'),       'test-value')
        self.assertEqual(underscore('test-Value', joiner='-'),       'test-value')
        self.assertEqual(underscore('test value', joiner='-'),       'test-value')
        self.assertEqual(underscore('TestValue', joiner='-'),        'test-value')
        self.assertEqual(underscore('testValue', joiner='-'),        'test-value')
        self.assertEqual(underscore('TeSt VaLue', joiner='-'),       'te-st-va-lue')

    def test_boy_am_i_tired_of_python23_compat_unicode_being_so_freakin_broken(self):
        """
        Test if the u() function solves EVERY UNICODE PROBLEM EVER
        """
        self.assertEqual(u('test'), u'test')
        self.assertEqual(u(str('test')), u'test')