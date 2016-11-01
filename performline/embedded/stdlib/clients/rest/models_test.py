from __future__ import absolute_import
from unittest import TestCase
from .models import RestModel


class RestModelTest(TestCase):
    def test_formatted_path(self):
        model = RestModel(None, {
            'Id': 4,
        }, rest_path='/test/{id}/')

        self.assertEqual(model.formatted_path(), '/test/4/')

        self.assertEqual(model.formatted_path({
            'Id': 5,
        }), '/test/4/')

        self.assertEqual(model.formatted_path({
            'id': 6,
        }), '/test/6/')

        model.rest_path = '/test/{Id}/'

        self.assertEqual(model.formatted_path({
            'Id': 5,
        }), '/test/5/')

        with self.assertRaises(KeyError):
            self.assertEqual(model.formatted_path(), '/test/5/')
