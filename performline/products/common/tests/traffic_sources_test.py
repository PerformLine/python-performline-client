
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
from performline.products.common.models import TrafficSource
from performline.testing import client


class TestTrafficSources(unittest.TestCase):
    def setUp(self):
        self.client = client()

    def test_get_traffic_source(self):
        ts = list(self.client.trafficsources())

        first_ts = self.client.trafficsources(1)

        self.assertIsInstance(first_ts, TrafficSource)

        # Testing that the appropriate number of traffic sources should be returned
        self.assertEqual(len(ts), 5)

        # Test attributes of first traffic source against known traffic source fixtures
        self.assertEqual(first_ts.Id, 1)
        self.assertEqual(first_ts.CompanyId, 10)

    def test_traffic_source_end_point_access(self):
        # Traffic source 6 belongs to agency test client does not have access to
        # ts should be empty list which should automatically create error

        ts = self.client.trafficsources(6)

        # try:
            # ts = list(self.client.trafficsources(6))
        # except AttributeError:
            # self.assertEqual(1, 1)

        if len(list(ts)) > 0:
            raise AssertionError('A traffic source outside the scope of the test token was returned.')
        else:
            self.assertEqual(1, 1)

    def test_traffic_source_endpoint_offset(self):
        ts = list(self.client.trafficsources(offset=1))

        self.assertEqual(len(ts), 4)
       
        ts_names = [traffic_source.Id for traffic_source in ts]

        self.assertEqual(ts_names, [2, 3, 4, 5])

    def test_traffic_source_endpoint_limit(self):
        ts = list(self.client.trafficsources(limit=3))

        self.assertEqual(len(ts), 3)

        ts_keys = [traffic_source.Id for traffic_source in ts]

        self.assertEqual(ts_keys, [1, 2, 3])

