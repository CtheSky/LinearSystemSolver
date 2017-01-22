import unittest
from vector_test import VectorTest
from line_test import LineTest
from plane_test import PlaneTest
from linear_system_test import LinearSystemTest
from linear_system_with_hyperplane_test import LinearSystemWithHyperplaneTest

all_tests = unittest.TestSuite([
    LineTest(),
    VectorTest(),
    PlaneTest(),
    LinearSystemTest(),
    LinearSystemWithHyperplaneTest()
])

all_tests.run(unittest.TestResult())
