import unittest
from calculators import calculate, harmony


class CalculatorTests(unittest.TestCase):
    def test_arithmetic(self):
        for expression, expected in [('2*2', 4), ('2/2', 1), ('(2+3)*4', 20), ('-2*3', -6), ('1,5+2.5', 4)]:
            self.assertEqual(calculate(expression), expected)

    def test_rejects_code_and_unbounded_values(self):
        for expression in ['__import__("os")', '2**100000', 'True', '1e999', '9'*201]:
            with self.assertRaises((ValueError, SyntaxError)):
                calculate(expression)
        with self.assertRaises(ZeroDivisionError):
            calculate('2/0')

    def test_harmonies(self):
        self.assertEqual(harmony('#FF0000', 'Complementar')[0], ['#FF0000', '#00FFFF'])
        self.assertEqual(harmony('#FF0000', 'Triádica')[0], ['#FF0000', '#00FF00', '#0000FF'])
        self.assertEqual(harmony('#808080', 'Complementar')[0], ['#808080', '#808080'])


if __name__ == '__main__':
    unittest.main()
