from __future__ import absolute_import
from unittest import TestCase
import json
import pytest
import httpretty
from . import StandardRestClient
from .utils import make_response


class RestRequestTest(TestCase):
    def setUp(self):
        httpretty.enable()
        self.client = StandardRestClient(url='http://test-rest-service')

    def tearDown(self):
        httpretty.disable()

    @pytest.mark.skip(reason=("moto and httpretty are incompatible"))
    def test_request_until(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://test-rest-service/request_until_test/?limit=1&offset=0",
            content_type='application/json',
            responses=[
                httpretty.Response(body=json.dumps(make_response({
                    'Id': 1,
                }, total=3, limit=1))),
                httpretty.Response(body=json.dumps(make_response({
                    'Id': 2,
                }, total=3, limit=1, offset=1))),
                httpretty.Response(body=json.dumps(make_response({
                    'Id': 3,
                }, total=3, limit=1, offset=2))),
            ]
        )

        responses = self.client.get_until('/request_until_test/', params={
            'limit': 1,
        })

        self.assertEqual(len(responses), 3)

        self.assertEqual(responses[0].results(0)['Id'], 1)
        self.assertEqual(responses[0].limit, 1)
        self.assertEqual(responses[0].offset, 0)

        self.assertEqual(responses[1].results(0)['Id'], 2)
        self.assertEqual(responses[1].limit, 1)
        self.assertEqual(responses[1].offset, 1)

        self.assertEqual(responses[2].results(0)['Id'], 3)
        self.assertEqual(responses[2].limit, 1)
        self.assertEqual(responses[2].offset, 2)
