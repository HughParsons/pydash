import unittest
from unittest.mock import Mock
from lib import misc
import inspect

class TestMisc(unittest.TestCase):
    def test_parameters(self):
        def fn(a, b, c=1, *args, d, e=2, **kwargs):
            pass

        expected_parameters = {
            "a": inspect._empty,
            "b": inspect._empty,
            "c": 1,
            "args": inspect._empty,
            "d": inspect._empty,
            "e": 2,
            "kwargs": inspect._empty,
        }
        actual_parameters = misc.parameters(fn)
        
        for k in actual_parameters:
            self.assertEqual(actual_parameters.get(k).default, expected_parameters[k])

if __name__ == "__main__":
    unittest.main()