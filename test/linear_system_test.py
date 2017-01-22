from __future__ import absolute_import
from decimal import Decimal

from vector import Vector
from plane import Plane
from linear_system import LinearSystem

import unittest


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

    def test_rref(self):
        p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
        p2 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='2')
        s = LinearSystem([p1, p2])
        r = s.compute_rref()
        self.assertTrue(r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term='-1') and
                        r[1] == p2)

        p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
        p2 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='2')
        s = LinearSystem([p1, p2])
        r = s.compute_rref()
        self.assertTrue(r[0] == p1 and
                        r[1] == Plane(constant_term='1'))

        p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
        p2 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
        p3 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
        p4 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
        s = LinearSystem([p1, p2, p3, p4])
        r = s.compute_rref()
        self.assertTrue(r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term='0') and
                        r[1] == p2 and
                        r[2] == Plane(normal_vector=Vector(['0', '0', '-2']), constant_term='2') and
                        r[3] == Plane())

        p1 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1')
        p2 = Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2')
        p3 = Plane(normal_vector=Vector(['1', '2', '-5']), constant_term='3')
        s = LinearSystem([p1, p2, p3])
        r = s.compute_rref()
        self.assertTrue(r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term=Decimal('23') / Decimal('9')) and
                        r[1] == Plane(normal_vector=Vector(['0', '1', '0']),
                                      constant_term=Decimal('7') / Decimal('9')) and
                        r[2] == Plane(normal_vector=Vector(['0', '0', '1']),
                                      constant_term=Decimal('2') / Decimal('9')))

    def test_compute_solution(self):
        p1 = Plane(normal_vector=Vector(['5.862', '1.178', '-10.366']), constant_term='-8.15')
        p2 = Plane(normal_vector=Vector(['-2.931', '-0.589', '5.183']), constant_term='-4.075')
        s = LinearSystem([p1, p2])
        self.assertEqual(s.compute_solution(), LinearSystem.NO_SOLUTIONS_MSG)

        p1 = Plane(normal_vector=Vector(['8.631', '5.112', '-1.816']), constant_term='-5.113')
        p2 = Plane(normal_vector=Vector(['4.315', '11.132', '-5.27']), constant_term='-6.775')
        p3 = Plane(normal_vector=Vector(['-2.158', '3.01', '-1.727']), constant_term='-0.831')
        s = LinearSystem([p1, p2, p3])
        self.assertNotEqual(len(s.compute_solution().direction_vectors), 0)

        p1 = Plane(normal_vector=Vector(['5.262', '2.739', '-9.878']), constant_term='-3.441')
        p2 = Plane(normal_vector=Vector(['5.111', '6.358', '7.638']), constant_term='-2.152')
        p3 = Plane(normal_vector=Vector(['2.016', '-9.924', '-1.367']), constant_term='-9.278')
        p4 = Plane(normal_vector=Vector(['2.167', '-13.543', '-18.883']), constant_term='-10.567')
        s = LinearSystem([p1, p2, p3, p4])
        self.assertEqual(s.compute_solution().basepoint, Vector(['-1.177', '0.707', '-0.083']))

    def test_parametrization(self):
        p1 = Plane(normal_vector=Vector([0.786, 0.786, 0.588]), constant_term=-0.714)
        p2 = Plane(normal_vector=Vector([-0.131, -0.131, 0.244]), constant_term=0.319)
        s = LinearSystem([p1, p2])
        solution = s.compute_solution()
        self.assertEqual(solution.basepoint, Vector(['-1.346', '0', '0.585']))
        self.assertEqual(len(solution.direction_vectors), 1)
        self.assertEqual(solution.direction_vectors[0], Vector(['-1.0', '1.0', '0']))

        p1 = Plane(Vector([8.631, 5.112, -1.816]), -5.113)
        p2 = Plane(Vector([4.315, 11.132, -5.27]), -6.775)
        p3 = Plane(Vector([-2.158, 3.01, -1.727]), -0.831)
        s = LinearSystem([p1, p2, p3])
        solution = s.compute_solution()
        self.assertEqual(solution.basepoint, Vector(['-0.301', '-0.492', '0']))
        self.assertEqual(len(solution.direction_vectors), 1)
        self.assertEqual(solution.direction_vectors[0], Vector(['-0.091', '0.509', '1.0']))

        p1 = Plane(Vector([0.935, 1.76, -9.365]), -9.955)
        p2 = Plane(Vector([0.187, 0.352, -1.873]), -1.991)
        p3 = Plane(Vector([0.374, 0.704, -3.746]), -3.982)
        p4 = Plane(Vector([-0.561, -1.056, 5.619]), 5.973)
        s = LinearSystem([p1, p2, p3, p4])
        solution = s.compute_solution()
        self.assertEqual(solution.basepoint, Vector(['-10.647', '0', '0']))
        self.assertEqual(len(solution.direction_vectors), 2)
        self.assertEqual(solution.direction_vectors[0], Vector(['-1.882', '1.0', '0']))
        self.assertEqual(solution.direction_vectors[1], Vector(['10.016', '0', '1.0']))

