# Copyright (c) 2016, PerformLine, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the company nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL PERFORMLINE, INC. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
