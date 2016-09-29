import unittest
from performline.client import Client


def client():
    c = Client('00e4db7592541054d3791f42d62524f4139705c4', loglevel='DEBUG')
    c.url = 'http://localhost:8000'
    c.prefix = '/api/'
    return c


class TestBrands(unittest.TestCase):
    def setUp(self):
        self.client = client()

    def test_get_all_brands(self):
        brands = self.client.brands()

        self.assertIsInstance(brands, list)
        self.assertTrue(len(brands) > 0)

if __name__ == '__main__':
    unittest.main()
