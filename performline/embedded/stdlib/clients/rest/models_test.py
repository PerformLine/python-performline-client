from __future__ import absolute_import
import requests
import requests_mock
from unittest import TestCase
from .models import RestModel
from . import StandardRestClient
from .utils import make_response


class MyCoolGetAllModel(RestModel):
    rest_root = '/get-all/'


class MyCoolGetByIdModel(RestModel):
    rest_root = '/get-by-id/'


class RestModelTest(TestCase):
    def setUp(self):
        self.session = requests.Session()
        self.adapter = requests_mock.Adapter()
        self.session.mount('mock', self.adapter)

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
        self.adapter.register_uri('GET', 'mock://test-rest-getall/get-all/',
                                  json=make_response([{
                                      'Id': 1,
                                  }, {
                                      'Id': 2,
                                  }, {
                                      'Id': 3,
                                  }]))

        self.adapter.register_uri('GET', 'mock://test-rest-getall/get-all/1/',
                                  json=make_response({
                                    'Id': 1,
                                    'Name': 'First',
                                  }))

        self.adapter.register_uri('GET', 'mock://test-rest-getall/get-all/2/',
                                  json=make_response({
                                      'Id': 2,
                                      'Name': 'Second',
                                  }))

        self.adapter.register_uri('GET', 'mock://test-rest-getall/get-all/3/',
                                  json=make_response({
                                      'Id': 3,
                                      'Name': 'Third',
                                  }))

        client = StandardRestClient(url='mock://test-rest-getall', session=self.session)

        items = MyCoolGetAllModel.all(client)

        self.assertEqual(len(items), 3)

        self.assertIsInstance(items[0], MyCoolGetAllModel)
        self.assertEqual(items[0].id, 1)
        self.assertEqual(items[0].Id, 1)
        self.assertEqual(items[0].name, 'First')
        self.assertEqual(items[0].Name, 'First')

        self.assertIsInstance(items[1], MyCoolGetAllModel)
        self.assertEqual(items[1].id, 2)
        self.assertEqual(items[1].Id, 2)
        self.assertEqual(items[1].name, 'Second')
        self.assertEqual(items[1].Name, 'Second')

        self.assertIsInstance(items[2], MyCoolGetAllModel)
        self.assertEqual(items[2].id, 3)
        self.assertEqual(items[2].Id, 3)
        self.assertEqual(items[2].name, 'Third')
        self.assertEqual(items[2].Name, 'Third')

    def test_get_all_no_autoload(self):
        self.adapter.register_uri('GET', 'mock://test-rest-getall/get-all/',
                                  json=make_response([{
                                       'Id': 1,
                                   }, {
                                       'Id': 2,
                                   }, {
                                       'Id': 3,
                                   }]))

        client = StandardRestClient(url='mock://test-rest-getall', session=self.session)

        items = MyCoolGetAllModel.all(client, autoload=False)

        self.assertEqual(len(items), 3)

        self.assertIsInstance(items[0], MyCoolGetAllModel)
        self.assertEqual(items[0].id, 1)
        self.assertEqual(items[0].Id, 1)
        self.assertIsNone(items[0].name)
        self.assertIsNone(items[0].Name)

        self.assertIsInstance(items[1], MyCoolGetAllModel)
        self.assertEqual(items[1].id, 2)
        self.assertEqual(items[1].Id, 2)
        self.assertIsNone(items[1].name)
        self.assertIsNone(items[1].Name)

        self.assertIsInstance(items[2], MyCoolGetAllModel)
        self.assertEqual(items[2].id, 3)
        self.assertEqual(items[2].Id, 3)
        self.assertIsNone(items[2].name)
        self.assertIsNone(items[2].Name)

    def test_get_by_id(self):
        self.adapter.register_uri('GET', 'mock://test-rest-getbyid/get-by-id/12345/',
                                  json=make_response({
                                        'Id': 12345,
                                        'Name': 'Test Data',
                                    }))

        client = StandardRestClient(url='mock://test-rest-getbyid', session=self.session)

        item = MyCoolGetByIdModel.get(client, 12345)

        self.assertIsInstance(item, MyCoolGetByIdModel)
        self.assertEqual(item.id, 12345)
        self.assertEqual(item.Id, 12345)
        self.assertEqual(item.name, 'Test Data')
        self.assertEqual(item.Name, 'Test Data')
