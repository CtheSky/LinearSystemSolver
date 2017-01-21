from decimal import Decimal, getcontext
from copy import deepcopy

from vector import Vector
from plane import Plane

getcontext().prec = 30


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def swap_rows(self, row1, row2):
        self[row1], self[row2] = self[row2], self[row1]

    def multiply_coefficient_and_row(self, coefficient, row):
        n = self[row].normal_vector
        k = self[row].constant_term

        new_normal_vector = n.times_scalar(coefficient)
        new_constant_term = k * coefficient

        self[row] = Plane(normal_vector=new_normal_vector,
                          constant_term=new_constant_term)

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        n1 = self[row_to_add].normal_vector
        n2 = self[row_to_be_added_to].normal_vector
        k1 = self[row_to_add].constant_term
        k2 = self[row_to_be_added_to].constant_term

        new_normal_vector = n1.times_scalar(coefficient).plus(n2)
        new_constant_term = (k1 * coefficient) + k2

        self[row_to_be_added_to] = Plane(normal_vector=new_normal_vector,
                                         constant_term=new_constant_term)

    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices

    def compute_triangular_form(self):
        system = deepcopy(self)
        num_equations = len(system)

        for i in range(num_equations):
            # check whether coefficient is zero, when it is, swap with a row below with none zero coefficient
            indices = system.indices_of_first_nonzero_terms_in_each_row()
            if indices[i] != i:
                for j in range(i + 1, num_equations):
                    if indices[j] == i:
                        system.swap_rows(i, j)
                        break

            # eliminate the coefficient in column i underneath row i
            for j in range(i + 1, num_equations):
                c1 = system[i].normal_vector[i]
                c2 = system[j].normal_vector[i]

                coefficient = -c2 / c1
                system.add_multiple_times_row_to_row(coefficient=coefficient,
                                                     row_to_add=i,
                                                     row_to_be_added_to=j)
        return system

    def compute_rref(self):
        tf = self.compute_triangular_form()

        num_equations = len(tf)
        pivot_indices = tf.indices_of_first_nonzero_terms_in_each_row()

        for i in range(num_equations)[::-1]:
            col = pivot_indices[i]
            if col < 0:
                continue

            # scale to make coefficient equal 1
            n = tf[i].normal_vector
            times = Decimal('1.0') / n[col]
            tf.multiply_coefficient_and_row(times, i)

            # clear coefficient above
            for j in range(i):
                c1 = tf[i].normal_vector[col]
                c2 = tf[j].normal_vector[col]

                coefficient = -c2 / c1
                tf.add_multiple_times_row_to_row(coefficient=coefficient,
                                                 row_to_add=i,
                                                 row_to_be_added_to=j)

        return tf

    def compute_solution(self):
        try:
            return self.do_gaussian_elimination_and_extract_solution()

        except Exception as e:
            if (str(e) == self.NO_SOLUTIONS_MSG or
                    str(e) == self.INF_SOLUTIONS_MSG):
                return str(e)
            else:
                raise e

    def do_gaussian_elimination_and_extract_solution(self):
        rref = self.compute_rref()

        rref.raise_exception_if_contradictory_equation()
        rref.raise_exception_if_too_few_pivots()

        num_variables = rref.dimension
        solution_coordinates = [rref[i].constant_term for i in range(num_variables)]

        return Vector(solution_coordinates)

    def raise_exception_if_contradictory_equation(self):
        for p in self.planes:
            try:
                p.first_nonzero_index(p.normal_vector)

            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:

                    constant_term = MyDecimal(p.constant_term)
                    if not constant_term.is_near_zero():
                        raise Exception(self.NO_SOLUTIONS_MSG)

                else:
                    raise e

    def raise_exception_if_too_few_pivots(self):
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        num_pivots = sum([1 if index >= 0 else 0 for index in pivot_indices])
        num_variables = self.dimension

        if num_pivots < num_variables:
            raise Exception(self.INF_SOLUTIONS_MSG)

    def __len__(self):
        return len(self.planes)

    def __getitem__(self, i):
        return self.planes[i]

    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps
