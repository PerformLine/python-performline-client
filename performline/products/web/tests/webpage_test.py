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
from ..models import WebPage
from ....testing import client


class TestPages(unittest.TestCase):
    def setUp(self):
        self.client = client()

    def test_get_all_pages(self):
        pages = list(self.client.webpages())
        self.assertIsInstance(pages, list)
        self.assertTrue(len(pages) == 3)

        page = pages[0]

        self.assertIsInstance(page, Webpage)
        self.assertEqual(page.Id, 10)
        self.assertEqual(page.Type, 'web')
        self.assertEqual(page.Score, 80)
        self.assertEqual(page.TrafficSourceId, 1)
        self.assertEqual(page.CampaignId, 3)
        self.assertEqual(page.BrandId, 12)
        self.assertEqual(page.CompanyId, 10)
        self.assertEqual(page.CreatedAt, '2018-7-24T00:00:00')
        self.assertEqual(page.Url, "https://www.wsj.com")
        self.assertEqual(page.CreatedAt, '2018-7-25T00:00:00')

    def test_webpage_endpoint_access(self):
        # Company token does not have access to page_id = 13  
        page = list(self.client.webpages(13))

        self.assertIsInstance(page, list)
        self.assertTrue(len(page) == 0)

    def test_get_webpage_by_id(self):
        #Wil test that all attributes are returned for page id = 11
        page = self.client.webpages(11)

        self.assertIsInstance(page, Webpage)

        self.assertEqual(page.Id, 11)
        self.assertEqual(page.Type, 'web')
        self.assertEqual(page.Score, 70)
        self.assertEqual(page.TrafficSourceId, 1)
        self.assertEqual(page.CampaignId, 3)
        self.assertEqual(page.BrandId, 12)
        self.assertEqual(page.CompanyId, 10)
        self.assertEqual(page.CreatedAt, '2018-7-24T00:00:00')
        self.assertEqual(page.Url, "https://www.washingtonpost.com")
        self.assertEqual(page.CreatedAt, '2018-7-25T00:00:00')

    def test_get_webpage_in(self):
        #Will test parameters
        pages = list(self.client.webpages()) # this has 3 pages

        pages_in_limit = list(self.client.webpages(limit=2))

        self.assertEqual(len(pages_in_limit, 2))
        self.assertEqual(pages_in_limit[0], 10)
        self.assertEqual(pages_in_limit[1], 11)

        pages_in_offset = list(self.client.webpages(offset=1))

        self.assertEqual(len(pages_in_offset, 2))
        self.assertEqual(pages_in_limit[0], 11)
        self.assertEqual(pages_in_limit[1], 12)

        pages_in_campaign = list(self.client.webpages(campaign=3))

        self.assertEqual(len(pages_in_campaign, 2))
        self.assertEqual(pages_in_limit[0], 10)
        self.assertEqual(pages_in_limit[1], 11)

        pages_in_brand = list(self.client.webpages(brand=12))

        self.assertEqual(len(pages_in_brand, 2))
        self.assertEqual(pages_in_limit[0], 11)
        self.assertEqual(pages_in_limit[1], 12)
