from __future__ import unicode_literals
import unittest
from ....testing import client


class TestCalls(unittest.TestCase):
    def setUp(self):
        self.client = client()

    def test_get_all_calls(self):
        calls = self.client.calls()

        self.assertIsInstance(calls, list)
