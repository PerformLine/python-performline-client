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

    def test_get_campaign(self):
        c = list(self.client.campaigns())

        first_c = self.client.campaigns(1)

        self.assertIsInstance(first_c, Campaign)

        #Testing that the appropriate number of campaigns are returned
        self.assertEqual(len(c), 6)

        #Test attributes of first campaign against known campaign fixtures
        self.assertEqual(first_c.Id, 1)
        self.assertEqual(first_c.Name, "Web API Test Campaign, One")

    def test_campaign_endpoint_access(self):
        # Campaign 4 belongs to an agency which test client does not have access to
        # c should be empty list which should automatically create error

        c = self.client.campaigns(4)
        # print str(c)

        if len(list(c)) > 0:
            raise AssertionError('A campaign outside the scope of the test token was returned.')
        else:
            self.assertEqual(1, 1)

    def test_campaign_endpoint_offset(self):
        c = list(self.client.campaigns(offset=1))

        self.assertEqual(len(c), 5)
       
        c_names = [campaign.Id for campaign in c]

        self.assertEqual(c_names, [2, 3, 5, 6, 7])

    def test_campaign_endpoint_limit(self):
        c = list(self.client.campaigns(limit=2))

        self.assertEqual(len(c), 2)

        c_keys = [campaign.Id for campaign in c]

        self.assertEqual(c_keys, [1, 2])

