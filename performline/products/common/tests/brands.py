import unittest
from ..models import Brand
from ....testing import client


class TestBrands(unittest.TestCase):
    def setUp(self):
        self.client = client()

    def test_get_all_brands(self):
        brands = self.client.brands()

        self.assertIsInstance(brands, list)
        self.assertTrue(len(brands) >= 3)

        self.assertEqual(brands[0].id, 11)
        self.assertEqual(brands[0].name, u'A. Foo Industries')

        self.assertEqual(brands[1].id, 12)
        self.assertEqual(brands[1].name, u'BAR, Inc.')

        self.assertEqual(brands[2].id, 13)
        self.assertEqual(brands[2].name, u'Baz Media')

    def test_get_brand_11(self):
        brand = self.client.brands(11)

        self.assertIsInstance(brand, Brand)

        self.assertEqual(brand.Id, 11)
        self.assertEqual(brand.Name, u'A. Foo Industries')

        self.assertEqual(brand.id, 11)
        self.assertEqual(brand.name, u'A. Foo Industries')
