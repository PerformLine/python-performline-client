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
from ..models import Brand
from ....testing import client


class TestBrands(unittest.TestCase):
    def setUp(self):
        self.client = client()

    def test_get_all_brands(self):
        brands = self.client.brands(params={
            'limit': 1
        })

        self.assertIsInstance(brands, list)
        self.assertTrue(len(brands) >= 3)

        self.assertIsInstance(brands[0], Brand)
        self.assertEqual(brands[0].id, 11)
        self.assertEqual(brands[0].name, 'A. Foo Industries')

        self.assertIsInstance(brands[1], Brand)
        self.assertEqual(brands[1].id, 12)
        self.assertEqual(brands[1].name, 'BAR, Inc.')

        self.assertIsInstance(brands[2], Brand)
        self.assertEqual(brands[2].id, 13)
        self.assertEqual(brands[2].name, 'Baz Media')

    def test_get_brand_11(self):
        brand = self.client.brands(11)

        self.assertIsInstance(brand, Brand)

        self.assertEqual(brand.Id, 11)
        self.assertEqual(brand.Name, 'A. Foo Industries')

        self.assertEqual(brand.id, 11)
        self.assertEqual(brand.name, 'A. Foo Industries')
