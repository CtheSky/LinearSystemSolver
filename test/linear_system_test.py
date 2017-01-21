from __future__ import absolute_import
import unittest
from vector import Vector
from plane import Plane
from linear_system import LinearSystem


class LinearSystemTest(unittest.TestCase):

    def test_row_operations(self):
        p0 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
        p1 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
        p2 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
        p3 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')

        s = LinearSystem([p0, p1, p2, p3])

        s.swap_rows(0, 1)
        self.assertTrue(s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3)

        s.swap_rows(1, 3)
        self.assertTrue(s[0] == p1 and s[1] == p3 and s[2] == p2 and s[3] == p0)

        s.swap_rows(3, 1)
        self.assertTrue(s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3)

        s.multiply_coefficient_and_row(1, 0)
        self.assertTrue(s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3)

        s.multiply_coefficient_and_row(-1, 2)
        self.assertTrue(s[0] == p1 and
                        s[1] == p0 and
                        s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
                        s[3] == p3)

        s.multiply_coefficient_and_row(10, 1)
        self.assertTrue(s[0] == p1 and
                        s[1] == Plane(normal_vector=Vector(['10', '10', '10']), constant_term='10') and
                        s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
                        s[3] == p3)

        s.add_multiple_times_row_to_row(0, 0, 1)
        self.assertTrue(s[0] == p1 and
                        s[1] == Plane(normal_vector=Vector(['10', '10', '10']), constant_term='10') and
                        s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
                        s[3] == p3)

        s.add_multiple_times_row_to_row(1, 0, 1)
        self.assertTrue(s[0] == p1 and
                        s[1] == Plane(normal_vector=Vector(['10', '11', '10']), constant_term='12') and
                        s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
                        s[3] == p3)

        s.add_multiple_times_row_to_row(-1, 1, 0)
        self.assertTrue(s[0] == Plane(normal_vector=Vector(['-10', '-10', '-10']), constant_term='-10') and
                        s[1] == Plane(normal_vector=Vector(['10', '11', '10']), constant_term='12') and
                        s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
                        s[3] == p3)

    def test_compute_triangular_form(self):
        p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
        p2 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='2')
        s = LinearSystem([p1, p2])
        t = s.compute_triangular_form()
        self.assertTrue(t[0] == p1 and
                        t[1] == p2)

        p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
        p2 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='2')
        s = LinearSystem([p1, p2])
        t = s.compute_triangular_form()
        self.assertTrue(t[0] == p1 and
                        t[1] == Plane(constant_term='1'))

        p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
        p2 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
        p3 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
        p4 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
        s = LinearSystem([p1, p2, p3, p4])
        t = s.compute_triangular_form()
        self.assertTrue(t[0] == p1 and
                        t[1] == p2 and
                        t[2] == Plane(normal_vector=Vector(['0', '0', '-2']), constant_term='2') and
                        t[3] == Plane())

        p1 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1')
        p2 = Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2')
        p3 = Plane(normal_vector=Vector(['1', '2', '-5']), constant_term='3')
        s = LinearSystem([p1, p2, p3])
        t = s.compute_triangular_form()
        self.assertTrue(t[0] == Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2') and
                        t[1] == Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1') and
                        t[2] == Plane(normal_vector=Vector(['0', '0', '-9']), constant_term='-2'))
