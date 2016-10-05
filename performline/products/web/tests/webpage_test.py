from __future__ import unicode_literals
import unittest
from ....testing import client


class TestPages(unittest.TestCase):
    def setUp(self):
        self.client = client()

    def test_get_all_pages(self):
        pages = self.client.webpages()

        self.assertIsInstance(pages, list)
