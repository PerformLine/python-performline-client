# -*- coding: utf-8 -*-
from __future__ import absolute_import
import re
from requests_mock import NoMockAddress
from unittest import TestCase
from . import StandardRestClient
# from .utils import make_response

RX_MOCK_URL_UUID = re.compile(
  '^mock:\/\/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
)


class RestMockingTest(TestCase):
    def setUp(self):
        self.client = StandardRestClient()

    def test_init(self):
        self.client.mock_init()
        self.assertIsNotNone(RX_MOCK_URL_UUID.match(self.client.url))

    def test_init_with_hostname(self):
        self.client.mock_init(hostname='test-mocking-test')
        self.assertEqual(self.client.url, 'mock://test-mocking-test')

    def test_exception_on_unmocked_request(self):
        self.client.mock_init()

        self.client.mock_request('get', '/whaaaaaaa', [
            True
        ])

        self.assertEqual(self.client.get('/whaaaaaaa').payload, True)
        self.assertEqual(self.client.get('/whaaaaaaa').payload, True)

        with self.assertRaises(NoMockAddress):
            self.client.put('/whaaaaaaa')

        self.assertEqual(self.client.get('/whaaaaaaa').payload, True)

    def test_flags(self):
        self.client.mock_init(flags={
            'yes': True,
            'no': 2,
            'steve': u'╰( ͡° ͜ʖ ͡° )つ──☆*:・ﾟ',
        })

        self.assertEqual(self.client.mock_flag('yes'), True)
        self.assertEqual(self.client.mock_flag('no'), 2)
        self.assertEqual(self.client.mock_flag('nonexistent'), False)
        self.assertEqual(self.client.mock_flag('steve'), u'╰( ͡° ͜ʖ ͡° )つ──☆*:・ﾟ')
        self.assertEqual(self.client.mock_flag('nonexistent-fb', 42), 42)

    def test_repeating_get(self):
        self.client.mock_init()
        self.client.mock_request('get', '/test/mock/1', [
            {
                'just': 'a-test',
            }
        ])

        self.assertEqual(self.client.get('/test/mock/1').payload.get('just'), 'a-test')
        self.assertEqual(self.client.get('/test/mock/1/').payload.get('just'), 'a-test')

    def test_multiresponse(self):
        self.client.mock_init()
        self.client.mock_request('get', '/test/mock/2', [
            {
                'just': 'a-test',
            }, {
                'just': 'another-test',
            },
        ])

        self.assertEqual(self.client.get('/test/mock/2').payload.get('just'), 'a-test')
        self.assertEqual(self.client.get('/test/mock/2').payload.get('just'), 'another-test')
        self.assertEqual(self.client.get('/test/mock/2').payload.get('just'), 'another-test')

    def test_dynamic_response(self):
        self.client.mock_init()
        self.counter = -1

        def counter_response(request, context):
            self.counter += 1

            return {
                'count': self.counter,
            }

        self.client.mock_request('get', '/test/mock/3', [
            counter_response,
        ])

        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 0)
        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 1)
        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 2)
        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 3)
        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 4)
        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 5)

    def test_static_dynamic_multiresponse(self):
        self.client.mock_init()
        self.counter = -1

        def counter_response(request, context):
            self.counter += 1

            return {
                'count': self.counter,
            }

        self.client.mock_request('get', '/test/mock/3', [
            {
                'count': 'NaNaNaNaNaNaN',
            },
            counter_response,
        ])

        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 'NaNaNaNaNaNaN')
        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 0)
        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 1)
        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 2)
        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 3)
        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 4)
        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 5)

    def test_multidynamic_multiresponse(self):
        self.client.mock_init()
        self.counter = 0

        def add_5_response(request, context):
            self.counter += 5

            return {
                'count': self.counter,
            }

        def sub_5_response(request, context):
            self.counter -= 5

            return {
                'count': self.counter,
            }

        self.client.mock_request('get', '/test/mock/3', [
            add_5_response,
            sub_5_response,
            add_5_response,
        ])

        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 5)
        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 0)
        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 5)
        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 10)
        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 15)
        self.assertEqual(self.client.get('/test/mock/3').payload.get('count'), 20)
