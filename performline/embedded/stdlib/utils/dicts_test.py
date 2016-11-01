from __future__ import absolute_import
from unittest import TestCase
from .dicts import mutate_dict, \
                   camelize_dict, \
                   underscore_dict, \
                   compact


class UtilsDictTest(TestCase):
    def test_mutate_dict_identity(self):
        self.assertEqual(mutate_dict({
            'A': 1,
            u'b': True,
            False: 3.0,
            3.5: {
                7.0: [4, 5, 6],
            },
        }), {
            'A': 1,
            u'b': True,
            False: 3.0,
            3.5: {
                7.0: [4, 5, 6],
            },
        })

    def test_mutate_dict_keys_and_values(self):
        inval = {
            'aaa': 1,
            'bbb': 2,
            'ccc': 3.0,
            'ddd': [{
                'e': 4,
                'f': 5,
            }],
        }

        self.assertEqual(mutate_dict(inval, keyFn=lambda k: k.title()), {
            'Aaa': 1,
            'Bbb': 2,
            'Ccc': 3.0,
            'Ddd': [{
                'E': 4,
                'F': 5,
            }],
        })

        inval[1.0] = 9

        self.assertEqual(mutate_dict(inval,
                                     keyFn=lambda k: k.title(),
                                     keyTypes=(str, unicode)), {
            'Aaa': 1,
            'Bbb': 2,
            'Ccc': 3.0,
            'Ddd': [{
                'E': 4,
                'F': 5,
            }],
            1.0: 9,
        })

        inval['ddd'][0]['g'] = [6, 7, 8]

        self.assertEqual(mutate_dict(inval,
                                     valueFn=lambda v: (v*10),
                                     valueTypes=(int, long)), {
            'aaa': 10,
            'bbb': 20,
            'ccc': 3.0,
            'ddd': [{
                'e': 40,
                'f': 50,
                'g': [6, 7, 8],
            }],
            1.0: 90,
        })

        self.assertEqual(mutate_dict(inval,
                                     valueFn=lambda v: (v*10.0),
                                     valueTypes=(float,)), {
            'aaa': 1,
            'bbb': 2,
            'ccc': 30.0,
            'ddd': [{
                'e': 4,
                'f': 5,
                'g': [6, 7, 8],
            }],
            1.0: 9,
        })

    def test_camelize_dict(self):
        self.assertEqual(camelize_dict({
            'id':      1,
            'first_name': 'Fred',
            'last_name': 'Johnson',
            'list Of numbers': [1, 4, 7],
            'Things that-are': {
                'active': True,
                'to': [{
                    'be': 'done',
                }]
            },
            True: 'yep',
            5: '2+2',
        }, True), {
            'Id':      1,
            'FirstName': 'Fred',
            'LastName': 'Johnson',
            'ListOfNumbers': [1, 4, 7],
            'ThingsThatAre': {
                'Active': True,
                'To': [{
                    'Be': 'done',
                }]
            },
            True: 'yep',
            5: '2+2',
        })

    def test_camelize_dict_unicode_keys(self):
        self.assertEqual(camelize_dict({
            u'id':      1,
            u'first_name': 'Fred',
            u'last_name': 'Johnson',
            u'list Of numbers': [1, 4, 7],
            u'Things that-are': {
                u'active': True,
                u'to': [{
                    u'be': 'done',
                }]
            },
            True: 'yep',
            5: '2+2',
        }, True), {
            'Id':      1,
            'FirstName': 'Fred',
            'LastName': 'Johnson',
            'ListOfNumbers': [1, 4, 7],
            'ThingsThatAre': {
                'Active': True,
                'To': [{
                    'Be': 'done',
                }]
            },
            True: 'yep',
            5: '2+2',
        })

    def test_camelize_dict_list_of_dicts(self):
        self.assertEqual(camelize_dict([
            {'primary_key': 1},
            {'primary_key': 2},
            {'primary_key': 3},
        ]), [
            {'primaryKey': 1},
            {'primaryKey': 2},
            {'primaryKey': 3},
        ])

    def test_camelize_dict_passthrough(self):
        self.assertEqual(camelize_dict(1), 1)
        self.assertEqual(camelize_dict(True), True)
        self.assertEqual(camelize_dict(False), False)
        self.assertEqual(camelize_dict(3.14), 3.14)
        self.assertEqual(camelize_dict('lol'), 'lol')
        self.assertEqual(camelize_dict([]), [])

    def test_underscore_dict(self):
        self.assertEqual(underscore_dict({
            'Id':      1,
            'FirstName': 'Fred',
            'LastName': 'Johnson',
            'ListOfNumbers': [1, 4, 7],
            'ThingsThatAre': {
                'Active': True,
                'To': [{
                    'Be': 'done',
                }]
            },
            True: 'yep',
            5: '2+2',
        }), {
            'id':      1,
            'first_name': 'Fred',
            'last_name': 'Johnson',
            'list_of_numbers': [1, 4, 7],
            'things_that_are': {
                'active': True,
                'to': [{
                    'be': 'done',
                }]
            },
            True: 'yep',
            5: '2+2',
        })

    def test_underscore_dict_unicode_keys(self):
        self.assertEqual(underscore_dict({
            u'Id':      1,
            u'FirstName': 'Fred',
            u'LastName': 'Johnson',
            u'ListOfNumbers': [1, 4, 7],
            u'ThingsThatAre': {
                u'Active': True,
                u'To': [{
                    u'Be': 'done',
                }]
            },
            True: 'yep',
            5: '2+2',
        }), {
            u'id':      1,
            u'first_name': 'Fred',
            u'last_name': 'Johnson',
            u'list_of_numbers': [1, 4, 7],
            u'things_that_are': {
                u'active': True,
                u'to': [{
                    u'be': 'done',
                }]
            },
            True: 'yep',
            5: '2+2',
        })

    def test_underscore_dict_list_of_dicts(self):
        self.assertEqual(underscore_dict([
            {'primaryKey': 1},
            {'primaryKey': 2},
            {'primaryKey': 3},
        ]), [
            {'primary_key': 1},
            {'primary_key': 2},
            {'primary_key': 3},
        ])

    def test_underscore_dict_passthrough(self):
        self.assertEqual(underscore_dict(1), 1)
        self.assertEqual(underscore_dict(True), True)
        self.assertEqual(underscore_dict(False), False)
        self.assertEqual(underscore_dict(3.14), 3.14)
        self.assertEqual(underscore_dict('lol'), 'lol')
        self.assertEqual(underscore_dict([]), [])

    def test_compact_default(self):
        self.assertEqual(compact({
            'a': 1,
            'b': 2,
            'c': 3,
        }), {
            'a': 1,
            'b': 2,
            'c': 3,
        })

        self.assertEqual(compact({
            'a': 1,
            'b': None,
            'c': 3,
        }), {
            'a': 1,
            'c': 3,
        })

        self.assertEqual(compact({
            'a': None,
            'b': None,
            'c': None,
        }), {})

    def test_compact_custom(self):
        self.assertEqual(compact({
            'a': 1,
            'b': 2,
            'c': 3,
        }, lambda k, v: v > 0), {
            'a': 1,
            'b': 2,
            'c': 3,
        })

        self.assertEqual(compact({
            'a': 1,
            'b': None,
            'c': 3,
        }, lambda k, v: v > 1), {
            'c': 3,
        })

        self.assertEqual(compact({
            'a': 1,
            'b': 2,
            'c': 3,
        }, lambda k, v: v > 2), {
            'c': 3,
        })
