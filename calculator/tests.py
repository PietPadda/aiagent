# tests.py

import unittest
from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator() # all tests use this obj

    def test_addition(self):
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8) # 3+5 should give 8

    def test_subtraction(self):
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6) # 10-4 should give 6

    def test_multiplication(self):
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12) # 3*4 should give 12

    def test_division(self):
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5) # 10/2 should give 5

    def test_nested_expression(self):
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17) # 3*4 + 5 should give 17 (12+5)

    def test_complex_expression(self):
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7) # 2*3 - 8/2 + 5 should give 7 (6-4+5)

    def test_empty_expression(self):
        result = self.calculator.evaluate("")
        self.assertIsNone(result) # no input should give none

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5") # $ is invalid oper

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3") # need no with +


if __name__ == "__main__":
    unittest.main()