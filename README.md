# LinearSystemSolver
A linear algebra lib build through 
[Linear Algebra Refresher Course on Udacity](https://cn.udacity.com/course/linear-algebra-refresher-course--ud953).  

It provides functionality to:
  1. Solve linear system
  2. Common manipulations on vector, line, plane and hyperplane
  
# Usage
#### Manipulation on Vector
```python
# Vector constructor receives an Iterable
# create 3-dimension vectors
v = Vector([1, 2, 3])

# create n-dimension vector
n = 3
w = Vector(range(n))

# dimension and coordinates
v.dimension    # 3
v.coordinates  # [Decimal('1'), Decimal('2'), Decimal('3')]

# plus and minus
v_plus_w = v.plus(w)
v_minus_w = v.minus(w)

# times scalar
v_times_3 = v.times_scalar(3)

# check parallel,orthogonal and zero (optional parameter tolerance)
v.is_parallel_to(w)
v.is_orthogonal_to(w, tolerance=1e-8)
v.is_zero(tolerance=1e-10)

# magnitude and normalized vector
v.magnitude()
v.normalized()  # returns a vector

# dot product
v.dot(w)

# angle (optional parameter in_degrees, default False)
v.angle_with(w)                   # returns in radians
v.angle_with(w, in_degrees=True)  # returns in degrees

# cross product (returns a vector)
v.cross(w)

# area of triangle and parallelogram made up by two vectors
v.area_of_triangle_with(w)
v.area_of_parallelogram_with(w)

```
#### Solve Linear System
```python
# Linear System is made up of equations
# Each equation is represented by a hyperplane

# Each hyperplane is made up of a normal vector and a constant term
p1 = Hyperplane(normal_vector=Vector(['0', '1', '1']), constant_term='1')   # y + z = 1
p2 = Hyperplane(normal_vector=Vector(['1', '-1', '1']), constant_term='2')  # x - y + z = 2
p3 = Hyperplane(normal_vector=Vector(['1', '2', '-5']), constant_term='3')  # 1 + 2y - 5z = 3

# Linear system receives an Iterable of Hyperplanes
system = LinearSystem([p1, p2, p3])

# get solution
solution = system.compute_solution()
print(solution)
# output:
# x_1 = 2.556
# x_2 = 0.778
# x_3 = 0.222

# if there is no solution
p1 = Hyperplane(normal_vector=Vector(['1', '1', '1']), constant_term='1')  # x + y + z = 1
p2 = Hyperplane(normal_vector=Vector(['1', '1', '1']), constant_term='2')  # x + y + z = 2
system = LinearSystem([p1, p2])
solution = system.compute_solution()
print(solution)
# output:
# No solutions

# if there is infinite solutions
p1 = Hyperplane(normal_vector=Vector(['0', '1', '1']), constant_term='1')   # y + z = 1
p2 = Hyperplane(normal_vector=Vector(['1', '-1', '1']), constant_term='2')  # x - y + z = 2
system = LinearSystem([p1, p2])
solution = system.compute_solution()
print(solution)
# output:
# x_1 = 3.0 + -2.0 t_1
# x_2 = 1.0 + -1.0 t_1
# x_3 = 0.0 + 1.0 t_1

# solution is a Parametrization Object
# Goal of Parametrization is to represent infinite solutions
# For linear system:
#   y + z = 1
#   x - y + z = 2
# Reduce to reduced row-echelon form:
#   x = 3 - 2z
#   y = 1 - z
#   z = 0 + z (make up to 3 dimension)
# Solution is a line : [3, 1, 0] + z * [-2, -1, 1]
# x,y are pivot variables and z is the free variable
# Parametrization is made up of a basepoint and a list of direction vectors representing free variables
solution.basepoint          # Vector(Decimal(3), Decimal(1), Decimal(0))
solution.direction_vectors  # [Vector(Decimal(-2), Decimal(-1), Decimal(1))]
```
#### Line and Plane
Line are Plane are just hyperplane with fixed dimension, somehow redundant, see more in documentation.
