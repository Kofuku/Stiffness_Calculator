import unittest
from Stiffness import Stiffness


class StiffnessTest(unittest.TestCase):

    stiffness = Stiffness(10, 0.4, 0.8, 5, 0.02, 0.06, 31, 200, 5, {"2.0": 2, "3.5": 2, "7.0": 1},
                          {"3.0": 7, "7.0": -4}, 45)

    def test_uncracked_compressive_zone_height_calculation(self):
        self.stiffness.uncracked_compressive_zone_height_calculation()
        self.assertEqual(0.40529986, round(self.stiffness.uncracked_compressive_zone_height, 8))

    def test_cracked_compressive_zone_height_calculation(self):
        self.stiffness.cracked_compressive_zone_height_calculation()
        self.assertEqual(0.12484114, round(self.stiffness.cracked_compressive_zone_height, 8))

    def test_uncracked_moment_of_inertia_calculation(self):
        self.stiffness.uncracked_moment_of_inertia_calculation()
        self.assertEqual(0.01764329, round(self.stiffness.uncracked_moment_of_inertia, 8))

    def test_cracked_moment_of_inertia_calculation(self):
        self.stiffness.cracked_moment_of_inertia_calculation()
        self.assertEqual(0.00217691, round(self.stiffness.cracked_moment_of_inertia, 8))

    def test_stiffness_calculation(self):
        self.stiffness.uncracked_compressive_zone_height_calculation()
        self.stiffness.cracked_compressive_zone_height_calculation()
        self.stiffness.uncracked_moment_of_inertia_calculation()
        self.stiffness.cracked_moment_of_inertia_calculation()
        self.stiffness.stiffness_calculation()
        self.assertEqual(0.54694199, round(self.stiffness.stiffness_values[0], 8))
        self.assertEqual(0.54694199, round(self.stiffness.stiffness_values[9], 8))
        self.assertEqual(0.54694199, round(self.stiffness.stiffness_values[18], 8))
        self.assertEqual(0.09452004, round(self.stiffness.stiffness_values[27], 8))
        self.assertEqual(0.08159520, round(self.stiffness.stiffness_values[36], 8))
        self.assertEqual(0.08015769, round(self.stiffness.stiffness_values[45], 8))
        self.assertEqual(0.08012761, round(self.stiffness.stiffness_values[50], 8))
        self.assertEqual(0.08061219, round(self.stiffness.stiffness_values[55], 8))
        self.assertEqual(0.08319329, round(self.stiffness.stiffness_values[64], 8))
        self.assertEqual(0.09558674, round(self.stiffness.stiffness_values[73], 8))
        self.assertEqual(0.54694199, round(self.stiffness.stiffness_values[82], 8))
        self.assertEqual(0.54694199, round(self.stiffness.stiffness_values[91], 8))
        self.assertEqual(0.54694199, round(self.stiffness.stiffness_values[100], 8))
        print(self.stiffness.stiffness_values)

if __name__ == '__main__':
    unittest.main()
