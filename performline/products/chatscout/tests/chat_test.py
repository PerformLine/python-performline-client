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
from ....testing import client
from ..models import Chat


class TestChats(unittest.TestCase):
    def setUp(self):
        self.client = client()

    def test_get_all_chats(self):
        chats = list(self.client.chats())
        self.assertIsInstance(chats, list)
        self.assertEqual(len(chats), 3)

        chat = chats[0]

        self.assertIsInstance(chat, Chat)
        self.assertEqual(chat.Id, 6)
        self.assertEqual(chat.Type, 'chat')
        self.assertEqual(chat.Score, 80)
        self.assertEqual(chat.TrafficSourceId, 1)
        self.assertEqual(chat.CampaignId, 9)
        self.assertEqual(chat.BrandId, 15)
        self.assertEqual(chat.CompanyId, 10)
        self.assertEqual(chat.CreatedAt, '2018-07-24T00:00:00-04:00')
        self.assertEqual(chat.LastScoredAt, '2018-07-24T00:00:00-04:00')


    def test_chat_endpoint_access(self):
        # Company token does not have access to page_id = 9 
        chat = list(self.client.chats(9))   
        
        self.assertIsInstance(chat, list)
        self.assertTrue(len(chat) == 0)

    def test_get_chat_by_id(self):
        #Wil test that all attributes are returned for page id = 7
        chat = self.client.chats(7)

        self.assertIsInstance(chat, Chat)

        self.assertEqual(chat.Id, 7)
        self.assertEqual(chat.Type, 'chat')
        self.assertEqual(chat.Score, 70)
        self.assertEqual(chat.TrafficSourceId, 1)
        self.assertEqual(chat.CampaignId, 9)
        self.assertEqual(chat.BrandId, 15)
        self.assertEqual(chat.CompanyId, 10)
        self.assertEqual(chat.CreatedAt, '2018-07-24T00:00:00-04:00')
        self.assertEqual(chat.LastScoredAt, '2018-08-24T00:00:00-04:00')

    def test_get_chat_in(self):
        #Will test parameters
        chats = list(self.client.chats()) # this has 3 chats

        chats_in_limit = list(self.client.chats(limit=2))

        self.assertEqual(len(chats_in_limit), 2)
        self.assertEqual(chats_in_limit[0].id, 6)
        self.assertEqual(chats_in_limit[1].id, 7)

        chats_in_offset = list(self.client.chats(offset=1))

        self.assertEqual(len(chats_in_offset), 2)
        self.assertEqual(chats_in_offset[0].id, 7)
        self.assertEqual(chats_in_offset[1].id, 8)

        chats_in_campaign = list(self.client.chats(campaign=9))

        self.assertEqual(len(chats_in_campaign), 2)
        self.assertEqual(chats_in_campaign[0].id, 6)
        self.assertEqual(chats_in_campaign[1].id, 7)

        chats_in_brand = list(self.client.chats(brand=15))

        self.assertEqual(len(chats_in_brand), 3)
        self.assertEqual(chats_in_brand[0].id, 6)
        self.assertEqual(chats_in_brand[1].id, 7)
    
