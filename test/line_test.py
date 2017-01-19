from __future__ import absolute_import
import unittest
from vector import Vector
from line import Line


class LineTest(unittest.TestCase):

    def test_is_parallel_to(self):
        l = Line(Vector([2, 3]), 0)
        el = Line(Vector([-4, -6]), 9)
        self.assertTrue(l.is_parallel_to(el))

        l = Line(Vector([1.182, 5.562]), 6.744)
        el = Line(Vector([1.773, 8.343]), 9.525)
        self.assertTrue(l.is_parallel_to(el))

    def test_equal(self):
        l = Line(Vector([2, 3]), 0)
        el = Line(Vector([-4, -6]), 0)
        self.assertEqual(l, el)

        l = Line(Vector([2, 3]), 0)
        el = Line(Vector([-4, -6]), 1)
        self.assertTrue(l != el)

        l = Line(Vector([4.046, 2.836]), 1.21)
        el = Line(Vector([10.115, 7.09]), 3.025)
        self.assertEqual(l, el)

        # normal vector is zero
        l = Line(Vector([0]), 1)
        el = Line(Vector([0]), 1)
        self.assertEqual(l, el)

        l = Line(Vector([0]), 0)
        el = Line(Vector([0]), 1)
        self.assertNotEqual(l, el)

    def test_intersection_with(self):
        # return None for parallel lines
        l = Line(Vector([2, 3]), 0)
        el = Line(Vector([4, 6]), 1)
        self.assertIsNone(l.intersection_with(el))

        l = Line(Vector([7.204, 3.182]), 8.68)
        el = Line(Vector([8.172, 4.114]), 9.883)
        self.assertEqual(l.intersection_with(el), Vector([1.173, 0.073]))

        # return line for same lines
        self.assertTrue(l.intersection_with(l) == l)
