from __future__ import absolute_import
from unittest import TestCase
from .responses import Response, SuccessResponse
from ...utils.dicts import MissingKeyException
from .utils import make_response


class RestResponseTest(TestCase):
    def test_response_data_access(self):
        response = Response(None, make_response([{
                'Id': 1,
                'Name': 'First',
                'Nested': {
                    'Here': 123,
                },
            }, {
                'Id': 2,
                'Name': 'Second',
            }],
            metadata={
                'this': {
                    'is': True,
                },
            },
            limit=10))

        self.assertIsInstance(response.payload, dict)
        self.assertEqual(response.response_status, 'success')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.haserror())
        self.assertEqual(response.deep_get('ResultCount/Total'), 2)
        self.assertEqual(response.deep_get('ResultCount/Limit'), 10)
        self.assertEqual(response.deep_get('ResultCount/Offset'), 0)

        with self.assertRaises(MissingKeyException):
            response.must_deep_get('Nothing')

        with self.assertRaises(MissingKeyException):
            response.must_deep_get('Nothing/Offset')

        self.assertIsInstance(response.metadata, dict)
        self.assertEqual(response.metadata_get('this/is'), True)
        self.assertEqual(response.metadata_get('this/is/not'), None)
        self.assertEqual(response.metadata_get('this'), {
            'is': True,
        })

    def test_success_response_data_access(self):
        response = SuccessResponse(None, make_response([{
            'Id': 1,
            'Name': 'First',
            'Nested': {
                'Here': 123,
            },
        }, {
            'Id': 2,
            'Name': 'Second',
        }], metadata={
            'this': {
                'is': True,
            },
        }, total=25, limit=2, offset=4))

        self.assertEqual(response.total_length, 25)
        self.assertEqual(response.length, 2)
        self.assertEqual(response.limit, 2)
        self.assertEqual(response.offset, 4)
        self.assertEqual(response.total_pages, 13)
        self.assertEqual(response.current_page, 3)
        self.assertIsInstance(response.results(), list)
