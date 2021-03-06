from math import sqrt, acos, pi
from decimal import Decimal, getcontext

from util import clip

getcontext().prec = 30


class Vector:

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    CANNOT_COMPUTE_ANGLE_WITH_ZERO_VECTOR_MSG = 'Cannot compute angle with zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'No unique parallel component for zero vector'
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'Only defined in two, three dimensions'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def magnitude(self):
        """Returns a Decimal object with value of magnitude."""
        coordinates_squared = [x ** 2 for x in self.coordinates]
        return Decimal(sqrt(sum(coordinates_squared)))

    def normalized(self):
        """Returns a normalized Vector of self.

                Raises:
                    Exception: Throws with msg 'Cannot normalize the zero vector'
                               when call this func on a zero vector
                """
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal('1.0') / magnitude)

        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def times_scalar(self, c):
        """Returns a new Vector with value of c times scalar self."""
        new_coordinates = [Decimal(c) * x for x in self.coordinates]
        return Vector(new_coordinates)

    def plus(self, v):
        """Returns a new Vector with value of v plus self."""
        new_coordinates = [x + y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        """Returns a new Vector with value of self minus v."""
        new_coordinates = [x - y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def dot(self, v):
        """Returns a new Vector with value of dot product of v and self."""
        return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])

    def angle_with(self, v, in_degrees=False):
        """Returns angle between v and self.

                Args:
                    v: vector to compute angle with.
                    in_degrees: specify return radians or degrees
                                True -> degrees
                                False -> radians (default)

                Returns:
                    in_degrees == True  -> angle in degrees
                    in_degrees == False -> angle in radians

                Raises:
                    Exception:
                        if catch Exception with msg 'Cannot normalize the zero vector'
                            Throws with msg 'Cannot compute angle with zero vector'
                        else
                            Throws caught Exception
                """
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angle_in_radians = Decimal(acos(clip(u1.dot(u2), 1.0, -1.0)))

            if in_degrees:
                degrees_per_radian = Decimal('180.0') / Decimal(pi)
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.CANNOT_COMPUTE_ANGLE_WITH_ZERO_VECTOR_MSG)
            else:
                raise e

    def component_parallel_to(self, basis):
        """Returns parallel component of self to basis Vector.

                Args:
                    basis: base vector to compute projection with.

                Returns:
                    A Vector which is a projection of self with basis as base vector

                Raises:
                    Exception:
                        if catch Exception with msg 'Cannot normalize the zero vector'
                           Throws with msg 'No unique parallel component for zero vector'
                        else
                            Throws caught Exception
                """
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.times_scalar(weight)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def component_orthogonal_to(self, basis):
        """Returns orthogonal component of self to basis Vector.

                Args:
                    basis: base vector to compute projection with.

                Returns:
                    A Vector with value of self minus a projection of self with basis as base vector

                Raises:
                    Exception:
                        if catch Exception with msg 'Cannot normalize the zero vector'
                           Throws with msg 'No unique parallel component for zero vector'
                        else
                            Throws caught Exception
                """
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def is_orthogonal_to(self, v, tolerance=1e-6):
        """Returns whether self is orthogonal to v.

                   Args:
                       v: vector to compare with.
                       tolerance: tolerance used in comparision (default 1e-6)."""
        return abs(self.dot(v)) < tolerance

    def is_parallel_to(self, v, tolerance=1e-6):
        """Returns whether self is parallel to v.

                   Args:
                       v: vector to compare with.
                       tolerance: tolerance used in comparision (default 1e-6)."""
        return (self.is_zero() or
                v.is_zero() or
                abs(self.angle_with(v) - Decimal('0')) < tolerance or
                abs(self.angle_with(v) - Decimal(pi)) < tolerance)

    def is_zero(self, tolerance=1e-10):
        """Returns whether self is zero vector.

                   Args:
                       tolerance: tolerance used in comparision (default 1e-6)."""
        return self.magnitude() < tolerance

    def area_of_triangle_with(self, v):
        """Returns area of triangle made up of self and v."""
        return self.area_of_parallelogram_with(v) / Decimal('2.0')

    def area_of_parallelogram_with(self, v):
        """Returns area of parallelogram made up of self and v."""
        cross_product = self.cross(v)
        return cross_product.magnitude()

    def cross(self, v):
        """Returns orthogonal component of self to basis Vector.

                        Args:
                            v: vector to compute cross product with.

                        Returns:
                            A Vector with value of cross product of self and v.

                        Raises:
                            ValueError:
                                if error with msg 'too many values to unpack' or 'need more than 1 value to unpack'
                                   Throws with msg 'Only defined in two, three dimensions'
                                else
                                    Throws caught Exception
                        """
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            new_coordinates = [y_1 * z_2 - y_2 * z_1,
                               -(x_1 * z_2 - x_2 * z_1),
                               x_1 * y_2 - x_2 * y_1]
            return Vector(new_coordinates)

        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                self_embedded_in_d3 = Vector(self.coordinates + ('0',))
                v_embedded_in_d3 = Vector(self.coordinates + ('0',))
                return self_embedded_in_d3.cross(v_embedded_in_d3)
            elif (msg == 'too many values to unpack' or
                    msg == 'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        if not isinstance(v, Vector):
            return False
        for x, y in zip(self.coordinates, v.coordinates):
            if x.quantize(Decimal('.001')) != y.quantize(Decimal('.001')):
                return False
        return True

    def __iter__(self):
        return self.coordinates.__iter__()

    def __getitem__(self, item):
        return self.coordinates[item]
