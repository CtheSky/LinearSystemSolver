from __future__ import absolute_import
import unittest
from vector import Vector
from plane import Plane


class PlaneTest(unittest.TestCase):

    def test_is_parallel_to(self):
        p1 = Plane(Vector([1, 2, 3]), 0)
        p2 = Plane(Vector([2, 4, 6]), 2)
        self.assertTrue(p1.is_parallel_to(p2))

        p1 = Plane(Vector([1, 2, 0]), 0)
        p2 = Plane(Vector([2, 4, 6]), 0)
        self.assertFalse(p1.is_parallel_to(p2))

        p1 = Plane(Vector([-0.412, 3.806, 0.728]), -3.46)
        p2 = Plane(Vector([1.03, -9.515, -1.82]), 8.65)
        self.assertTrue(p1.is_parallel_to(p2))

    def test_equal(self):
        p1 = Plane(Vector([1, 2, 3]), 1)
        p2 = Plane(Vector([2, 4, 6]), 2)
        self.assertEqual(p1, p2)

        p1 = Plane(Vector([1, 2, 3]), 1)
        p2 = Plane(Vector([2, 4, 6]), 1)
        self.assertNotEqual(p1, p2)

        p1 = Plane(Vector([-0.412, 3.806, 0.728]), -3.46)
        p2 = Plane(Vector([1.03, -9.515, -1.82]), 8.65)
        self.assertEqual(p1, p2)
