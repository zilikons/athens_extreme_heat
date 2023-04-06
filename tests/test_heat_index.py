import unittest
from extreme_heat.real_time_processing.nws_heat_index import heat_index

# Include the heat_index function and the required conversion functions here


class TestHeatIndex(unittest.TestCase):

    def test_invalid_units(self):
        with self.assertRaises(ValueError):
            heat_index(30, 70, "invalid_unit")

    def test_celsius_input(self):
        self.assertAlmostEqual(heat_index(30, 70), 35.038017, places=5)
        self.assertAlmostEqual(heat_index(10, 70), 8.8833333, places=5)

    def test_kelvin_input(self):
        self.assertAlmostEqual(heat_index(303.15, 70, "kelvin"), 308.1880175868, places=5)
        self.assertAlmostEqual(heat_index(283.15, 70, "kelvin"), 282.03333, places=5)

    def test_fahrenheit_input(self):
        self.assertAlmostEqual(heat_index(86, 70, "fahrenheit"), 95.06843159, places=5)
        self.assertAlmostEqual(heat_index(50, 70, "fahrenheit"), 47.99, places=5)

    def test_adjustment_conditions(self):
        self.assertAlmostEqual(heat_index(90, 10, "fahrenheit"), 85.2789683642, places=5)
        self.assertAlmostEqual(heat_index(84, 90, "fahrenheit"), 98.34250213, places=5)


if __name__ == "__main__":
    unittest.main()
