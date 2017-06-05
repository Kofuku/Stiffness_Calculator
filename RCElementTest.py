import unittest
from RCElement import RCElement


class RCElementTest(unittest.TestCase):

    rc_element = RCElement(10, 0.4, 0.8, 5, 0.02, 0.06, 31, 200, 5, {"2.0": 2, "3.5": 2, "7.0": 1},
                           {"3.0": 7, "7.0": -4}, 45)

    def test_geometric_additional(self):
        self.assertEqual(0.0007853982, round(self.rc_element.steel_area, 10))
        self.assertEqual(6.45161290, round(self.rc_element.concrete_steel_ratio_coefficient, 8))
        self.assertEqual(0.005067085, round(self.rc_element.substitute_steel_area, 9))
        self.assertEqual(0.74, round(self.rc_element.compressive_height, 2))

    def test_support_reaction_calculation(self):
        self.assertEqual(27.9, round(self.rc_element.support_reaction_a, 1))
        self.assertEqual(27.1, round(self.rc_element.support_reaction_b, 1))

    def test_bending_moment_calculation(self):
        self.assertEqual(0, round(self.rc_element.moments_values[0], 3))
        self.assertEqual(23.085, round(self.rc_element.moments_values[9], 3))
        self.assertEqual(42.120, round(self.rc_element.moments_values[18], 3))
        self.assertEqual(55.705, round(self.rc_element.moments_values[27], 3))
        self.assertEqual(71.640, round(self.rc_element.moments_values[36], 3))
        self.assertEqual(74.925, round(self.rc_element.moments_values[45], 3))
        self.assertEqual(75, round(self.rc_element.moments_values[50], 3))
        self.assertEqual(73.825, round(self.rc_element.moments_values[55], 3))
        self.assertEqual(68.560, round(self.rc_element.moments_values[64], 3))
        self.assertEqual(54.945, round(self.rc_element.moments_values[73], 3))
        self.assertEqual(40.680, round(self.rc_element.moments_values[82], 3))
        self.assertEqual(22.365, round(self.rc_element.moments_values[91], 3))
        self.assertEqual(0, round(self.rc_element.moments_values[100], 3))

    print(rc_element.moments_values)

if __name__ == '__main__':
    unittest.main()
