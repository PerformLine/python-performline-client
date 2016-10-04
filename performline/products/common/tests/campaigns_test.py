from __future__ import unicode_literals
import unittest
from ..models import Campaign
from ....testing import client


class TestCampaigns(unittest.TestCase):
    def setUp(self):
        self.client = client()

    def test_get_all_campaigns(self):
        campaigns = self.client.campaigns()

        self.assertIsInstance(campaigns, list)
        self.assertTrue(len(campaigns) >= 3)

        self.assertEqual(campaigns[0].id, 1)
        self.assertEqual(campaigns[0].name, 'A. Foo: Content')

        self.assertEqual(campaigns[1].id, 2)
        self.assertEqual(campaigns[1].name, 'A. Foo: Disclosure Page')

        self.assertEqual(campaigns[2].id, 3)
        self.assertEqual(campaigns[2].name, 'BAR, Inc.: Content')

    def test_get_campaign_1(self):
        campaign = self.client.campaigns(1)

        self.assertIsInstance(campaign, Campaign)

        self.assertEqual(campaign.Id, 1)
        self.assertEqual(campaign.Name, 'A. Foo: Content')

        self.assertEqual(campaign.id, 1)
        self.assertEqual(campaign.name, 'A. Foo: Content')
