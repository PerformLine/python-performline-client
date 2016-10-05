from __future__ import unicode_literals
import unittest
from ....testing import client


class TestChats(unittest.TestCase):
    def setUp(self):
        self.client = client()

    def test_get_all_chats(self):
        chats = self.client.chats()

        self.assertIsInstance(chats, list)
