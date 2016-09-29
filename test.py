import unittest
from performline.client import Client


def client():
    return Client('b0c777ac2a6018186fed2b0a6b55a62345a973d8', loglevel='DEBUG')


class TestBrands(unittest.TestCase):
    def setUp(self):
        self.client = client()

    def test_get_all_brands(self):
        brands = self.client.brands()

        self.assertIsInstance(brands, list)
        self.assertTrue(len(brands) > 0)

if __name__ == '__main__':
    unittest.main()
