from __future__ import absolute_import
import unittest
from vector import Vector
from decimal import Decimal


class VectorTest(unittest.TestCase):

    def test_initialize(self):
        # test basic initialize
        coordinates = [1, 2, 3]
        v = Vector(coordinates)
        self.assertEqual(v.coordinates, tuple([Decimal(x) for x in coordinates]))

        # test initialize with empty value
        try:
            Vector(None)
            self.assertFalse(True, 'last line should throws an error')
        except ValueError as e:
            self.assertEqual(str(e.message), 'The coordinates must be nonempty')

        # test initialize with value not iterable
        try:
            Vector(2)
            self.assertFalse(True, 'last line should throws an error')
        except TypeError as e:
            self.assertEqual(str(e.message), 'The coordinates must be an iterable')

    def test_magnitude(self):
        v = Vector([3, 4])
        self.assertEqual(v.magnitude(), 5)

        w = Vector([3.6, 4.7, 8.6])
        self.assertEqual(round(w.magnitude(), 6), 10.440785)

    def test_normalized(self):
        v = Vector([3, 4])
        w = Vector([0.6, 0.8])
        self.assertTrue(v.normalized() == w)

        v = Vector([3, 4])
        w = Vector([30, 40])
        self.assertTrue(v.normalized() == w.normalized())
