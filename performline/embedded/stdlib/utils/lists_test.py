from __future__ import absolute_import
from unittest import TestCase
from .lists import flatten, chunkwise


class UtilsListsTest(TestCase):
    def test_list_flatten(self):
        self.assertEqual(flatten([1, 2, 3]),       [1, 2, 3])
        self.assertEqual(flatten([1, [2, 3]]),     [1, 2, 3])
        self.assertEqual(flatten([[1], [2], [3]]), [1, 2, 3])
        self.assertEqual(flatten([[1, [2, [3]]]]), [1, 2, 3])

    def test_list_chunkwise_2(self):
        self.assertEqual(list(chunkwise([])),           [])
        self.assertEqual(list(chunkwise([1])),          [(1, None)])
        self.assertEqual(list(chunkwise([1, 2])),       [(1, 2)])
        self.assertEqual(list(chunkwise([1, 2, 3])),    [(1, 2), (3, None)])
        self.assertEqual(list(chunkwise([1, 2, 3, 4])), [(1, 2), (3, 4)])

    def test_list_chunkwise_3(self):
        self.assertEqual(list(chunkwise([], size=3)),                 [])
        self.assertEqual(list(chunkwise([1], size=3)),                [(1, None, None)])
        self.assertEqual(list(chunkwise([1, 2], size=3)),             [(1, 2, None)])
        self.assertEqual(list(chunkwise([1, 2, 3], size=3)),          [(1, 2, 3)])
        self.assertEqual(list(chunkwise([1, 2, 3, 4, 5], size=3)),    [(1, 2, 3), (4, 5, None)])
        self.assertEqual(list(chunkwise([1, 2, 3, 4, 5, 6], size=3)), [(1, 2, 3), (4, 5, 6)])
