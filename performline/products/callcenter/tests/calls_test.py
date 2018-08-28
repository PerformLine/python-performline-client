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
from ..models import Call


class TestCalls(unittest.TestCase):
    def setUp(self):
        self.client = client()

    def test_get_all_calls(self):
        # Testing that we retrieve all the calls for this token
        # and that the first call is the correct call
        c = list(self.client.calls())

        first_c = self.client.calls(1)

        self.assertEqual(len(c), 4)
        self.assertIsInstance(first_c, Call)

        self.assertEqual(first_c.Id, 1)
        self.assertEqual(first_c.unique_hash, '3f076c5ef9351e9197b499926955d8d4')

    def test_call_endpoint_access(self):
        # Call with id 5 should belong to an agency which we don't have access to
        c = list(self.client.calls(5))

        self.assertTrue(len(c) == 0)

    def test_call_endpoint_brand(self):
        # We will have access to two CCM test brands: id 13 and id 14
        # id 13 will have 2 campaigns (ids 5 and 6) with 2 calls in 4 and 1 call in 5 (3 calls total)
        # and id 14 will only have 1 campaign (id 6) with 1 call

        c = list(self.client.calls(brand=13))

        self.assertEqual(len(c), 4)

    def test_call_endpoint_campaign(self):
        # Campaign 4 should have 2 calls associated with it
        c=list(self.client.calls(campaign=5))

        self.assertEqual(len(c), 2)

    def test_call_endpoint_offset(self):

        c = list(self.client.calls(offset=1))
        self.assertEqual(len(c), 3)

        c_keys = [call.Id for call in c]
        self.assertEqual(c_keys, [2, 3, 4])

    def test_call_endpoint_limit(self):
        c = list(self.client.calls(limit=2))

        self.assertEqual(len(c), 2)

        c_keys = [call.Id for call in c]

        self.assertEqual(c_keys, [1, 2])

