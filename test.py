#!/usr/bin/env python3

# File: tests.py

import unittest
from mileage import convert_as_needed

class HelperFunctionTest(unittest.TestCase):

    def test_handles_int_as_text(self):
        self.assertEqual(convert_as_needed('20'), 20.0)

    def test_handles_float_as_text(self):
        self.assertEqual(convert_as_needed('20.4'), 20.4)

    def test_handles_conversion_of_int(self):
        self.assertEqual(convert_as_needed('20l', ('L', 'l'), 0.5), 10.0)

    def test_handles_conversion_of_float(self):
        self.assertEqual(convert_as_needed('20.8K', ('K', 'k'), 0.5), 10.4)


if __name__ == "__main__":
    unittest.main()

