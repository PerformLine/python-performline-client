from __future__ import absolute_import
import httpretty
import json
from unittest import TestCase
from .models import RestModel
from . import StandardRestClient
from .utils import make_response


class TestGetAllModel(RestModel):
    rest_root = '/get-all/'


class TestGetByIdModel(RestModel):
    rest_root = '/get-by-id/'


class RestModelTest(TestCase):
    def test_formatted_path(self):
        model = RestModel(None, {
            'Id': 4,
        }, rest_root='/test/')

        self.assertEqual(model.formatted_path(), '/test/4/')

        self.assertEqual(model.formatted_path({
            'Id': 5,
        }), '/test/4/')

        self.assertEqual(model.formatted_path({
            'id': 6,
        }), '/test/6/')

        model.primary_key = 'Id'

        self.assertEqual(model.formatted_path({
            'Id': 5,
        }), '/test/5/')

        with self.assertRaises(KeyError):
            self.assertEqual(model.formatted_path(), '/test/5/')

    def test_get_all(self):
        httpretty.enable()
        httpretty.register_uri(httpretty.GET,
                               "http://test-rest-getall/get-all/",
                               content_type='application/json',
                               body=json.dumps(make_response([{
                                   'Id': 1,
                               }, {
                                   'Id': 2,
                               }, {
                                   'Id': 3,
                               }])))

        httpretty.register_uri(httpretty.GET,
                               "http://test-rest-getall/get-all/1/",
                               content_type='application/json',
                               body=json.dumps(make_response({
                                   'Id': 1,
                                   'Name': 'First',
                               })))

        httpretty.register_uri(httpretty.GET,
                               "http://test-rest-getall/get-all/2/",
                               content_type='application/json',
                               body=json.dumps(make_response({
                                   'Id': 2,
                                   'Name': 'Second',
                               })))

        httpretty.register_uri(httpretty.GET,
                               "http://test-rest-getall/get-all/3/",
                               content_type='application/json',
                               body=json.dumps(make_response({
                                   'Id': 3,
                                   'Name': 'Third',
                               })))

        client = StandardRestClient(url='http://test-rest-getall')

        items = TestGetAllModel.all(client)

        httpretty.disable()

        self.assertEqual(len(items), 3)

        self.assertIsInstance(items[0], TestGetAllModel)
        self.assertEqual(items[0].id, 1)
        self.assertEqual(items[0].Id, 1)
        self.assertEqual(items[0].name, 'First')
        self.assertEqual(items[0].Name, 'First')

        self.assertIsInstance(items[1], TestGetAllModel)
        self.assertEqual(items[1].id, 2)
        self.assertEqual(items[1].Id, 2)
        self.assertEqual(items[1].name, 'Second')
        self.assertEqual(items[1].Name, 'Second')

        self.assertIsInstance(items[2], TestGetAllModel)
        self.assertEqual(items[2].id, 3)
        self.assertEqual(items[2].Id, 3)
        self.assertEqual(items[2].name, 'Third')
        self.assertEqual(items[2].Name, 'Third')

    def test_get_by_id(self):
        httpretty.enable()

        httpretty.register_uri(httpretty.GET,
                               "http://test-rest-getbyid/get-by-id/12345/",
                               content_type='application/json',
                               body=json.dumps(make_response({
                                   'Id': 12345,
                                   'Name': 'Test Data',
                               })))

        client = StandardRestClient(url='http://test-rest-getbyid')

        item = TestGetByIdModel.get(client, 12345)

        httpretty.disable()

        self.assertIsInstance(item, TestGetByIdModel)
        self.assertEqual(item.id, 12345)
        self.assertEqual(item.Id, 12345)
        self.assertEqual(item.name, 'Test Data')
        self.assertEqual(item.Name, 'Test Data')
