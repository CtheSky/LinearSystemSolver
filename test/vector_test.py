from __future__ import absolute_import
import unittest
from vector import Vector
from decimal import Decimal


class VectorTest(unittest.TestCase):

    def runTest(self):
        self.test_initialize()
        self.test_magnitude()
        self.test_normalized()
        self.test_plus()
        self.test_minus()
        self.test_times_scalar()
        self.test_dot()
        self.test_angle_with()
        self.test_is_parallel_to()
        self.test_is_orthogonal_to()
        self.test_component_parallel_to()
        self.test_component_orthogonal_to()
        self.test_projection()
        self.test_cross_product()
        self.test_area_of_parallelogram_with()
        self.test_area_of_triangle_with()

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

        w = Vector([-0.221, 7.437])
        self.assertEqual(round(w.magnitude(), 3), 7.440)

        w = Vector([3.6, 4.7, 8.6])
        self.assertEqual(round(w.magnitude(), 6), 10.440785)

        w = Vector([8.813, -1.331, -6.247])
        self.assertEqual(round(w.magnitude(), 3), 10.884)

    def test_normalized(self):
        v = Vector([3, 4])
        w = Vector([0.6, 0.8])
        self.assertTrue(v.normalized() == w)

        v = Vector([3, 4])
        w = Vector([30, 40])
        self.assertTrue(v.normalized() == w.normalized())

        v = Vector([5.581, -2.136])
        w = Vector([0.934, -0.357])
        self.assertTrue(v.normalized() == w)

        v = Vector([1.996, 3.108, -4.554])
        w = Vector([0.340, 0.530, -0.777])
        self.assertTrue(v.normalized() == w)

    def test_plus(self):
        v = Vector([3, 4])
        w = Vector([6, 8])
        self.assertTrue(v.plus(v) == w)

        v = Vector([8.218, -9.341])
        w = Vector([-1.129, 2.111])
        self.assertTrue(v.plus(w) == Vector([7.089, -7.230]))

    def test_minus(self):
        v = Vector([3, 4])
        w = Vector([6, 8])
        self.assertTrue(w.minus(v) == v)

        v = Vector([7.119, 8.215])
        w = Vector([-8.223, 0.878])
        self.assertTrue(v.minus(w) == Vector([15.342, 7.337]))

    def test_times_scalar(self):
        v = Vector([3, 4]).times_scalar(2)
        self.assertTrue(v == Vector([6, 8]))

        v = Vector([3, 4]).times_scalar(0)
        self.assertTrue(v.is_zero())

        v = Vector([1.671, -1.012, -0.318]).times_scalar(7.41)
        self.assertTrue(v == Vector([12.382, -7.499, -2.356]))

    def test_dot(self):
        v = Vector([7.887, 4.138])
        w = Vector([-8.802, 6.776])
        self.assertEqual(round(v.dot(w), 3), -41.382)

        v = Vector([-5.955, -4.904, -1.874])
        w = Vector([-4.496, -8.755, 7.103])
        self.assertEqual(round(v.dot(w), 3), 56.397)

    def test_angle_with(self):
        v = Vector([3.183, -7.627])
        w = Vector([-2.668, 5.319])
        self.assertEqual(round(v.angle_with(w), 3), 3.072)

        v = Vector([7.35, 0.221, 5.188])
        w = Vector([2.751, 8.259, 3.985])
        self.assertEqual(round(v.angle_with(w), 3), 1.052)

    def test_is_parallel_to(self):
        v = Vector([1, 0])
        self.assertTrue(v.is_parallel_to(v))

        v = Vector([-7.579, -7.88])
        w = Vector([22.737, 23.64])
        self.assertTrue(v.is_parallel_to(w))

        # zero vector is parallel to any vector
        self.assertTrue(v.is_parallel_to(Vector([0])))

    def test_is_orthogonal_to(self):
        # zero vector is orthogonal to itself
        v = Vector([0])
        self.assertTrue(v.is_orthogonal_to(v))

        v = Vector([-2.328, -7.284, -1.214])
        w = Vector([-1.821, 1.072, -2.94])
        self.assertTrue(v.is_orthogonal_to(w))

        # zero vector is parallel to any vector
        self.assertTrue(v.is_orthogonal_to(Vector([0])))

    def test_component_parallel_to(self):
        v = Vector([3.039, 1.879])
        w = Vector([0.825, 2.036])
        self.assertEqual(v.component_parallel_to(w), Vector([1.083, 2.672]))

    def test_component_orthogonal_to(self):
        v = Vector([-9.88, -3.264, -8.159])
        w = Vector([-2.155, -9.353, -9.473])
        self.assertEqual(v.component_orthogonal_to(w), Vector([-8.350, 3.376, -1.434]))

    def test_projection(self):
        v = Vector([3.009, -6.172, 3.692, -2.51])
        w = Vector([6.404, -9.144, 2.7509, 8.718])
        self.assertEqual(v, v.component_orthogonal_to(w).plus(v.component_parallel_to(w)))

    def test_cross_product(self):
        v = Vector([8.462, 7.893, -8.187])
        w = Vector([6.984, -5.975, 4.778])
        self.assertEqual(v.cross(w), Vector([-11.205, -97.609, -105.685]))

    def test_area_of_parallelogram_with(self):
        v = Vector([-8.987, -9.838, 5.031])
        w = Vector([-4.268, -1.861, -8.866])
        self.assertEqual(round(v.area_of_parallelogram_with(w), 3), 142.122)

    def test_area_of_triangle_with(self):
        v = Vector([1.5, 9.547, 3.691])
        w = Vector([-6.007, 0.124, 5.772])
        self.assertEqual(round(v.area_of_triangle_with(w), 3), 42.565)
