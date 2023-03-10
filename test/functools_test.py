import unittest
from unittest.mock import Mock
# import utils.functools as fntools
import lib.functools as fntools

class TestFunctools(unittest.TestCase):
    def test_after(self):
        mock = Mock(return_value=1)
        test_func = fntools.after(2, mock)

        test_func()
        mock.assert_not_called()
        test_func()
        mock.assert_called_once()
        test_func()
        self.assertEqual(mock.call_count, 2)

    def test_ary(self):
        # mock should only be called with first n args
        mock = Mock()
        test_func = fntools.ary(mock, 3)
        test_func(1, 2, 3, 4, 5)
        mock.assert_called_with(1,2,3)

    def test_before(self):
        i = 0
        def wrapped():
            nonlocal i
            i+=1
            return i

        mock = Mock(wraps=wrapped)
        test_func = fntools.before(3, mock)

        self.assertEqual(test_func(), 1)
        self.assertEqual(test_func(), 2)
        self.assertEqual(test_func(), 2)
        self.assertEqual(test_func(), 2)
        self.assertEqual(mock.call_count, 2)

    def test_bind(self):
        def fn(_self):
            _self.func()

        class MockClass:
            def __init__(self, func) -> None:
                self.func = func
        test_class = MockClass(Mock())
        test_func = fntools.bind(fn, test_class)

        test_func()
        test_class.func.assert_called_once()

    def test_attach(self):
        def fn(self=None):
            return "test-return-value"

        class MockClass:
            pass
        test_class = MockClass()
        test_func = fntools.attach(fn, test_class, "fn_test_name")

        test_func()
        self.assertTrue(hasattr(test_class, "fn_test_name"))
        self.assertEqual(fn(), test_class.fn_test_name())

    def test_curry(self):
        def fn(a, b, c):
            return a + b + c

        test_func = fntools.curry(fn)
        self.assertEqual(test_func(1)(2)(3), 6)
        self.assertEqual(test_func(1, 2)(3), 6)
        self.assertEqual(test_func(1, 2, 3), 6)

    def test_curryRight(self):
        def fn(a, b, c):
            return a + b + c

        test_func = fntools.curryRight(fn)
        self.assertEqual(test_func(3)(2)(1), 6)
        self.assertEqual(test_func(3, 2)(1), 6)
        self.assertEqual(test_func(3, 2, 1), 6)

    # def test_debounce(self):
    #     pass

    # def test_delay(self):
    #     pass
    
    # def test_flip(self):
    #     pass

    # def test_memoize(self):
    #     pass

    def test_negate(self):
        def fn(a, b):
            return a + b

        test_func = fntools.negate(fn)
        self.assertEqual(test_func(1, 2), False)

    def test_once(self):
        mock = Mock()
        test_func = fntools.once(mock)

        test_func()
        test_func()
        test_func()
        self.assertEqual(mock.call_count, 1)

    def test_overArgs(self):
        def fn(a, b):
            return a + b

        test_func = fntools.overArgs(fn, [lambda x: x*2, lambda x: x*3])
        self.assertEqual(test_func(1, 2), 8)

    def test_partial(self):
        def fn(a, b, c):
            return a + b + c

        test_func = fntools.partial(fn, 1, 2)
        self.assertEqual(test_func(3), 6)

    def test_partialRight(self):
        def fn(a, b, c):
            return a + b + c

        test_func = fntools.partialRight(fn, 3, 2)
        self.assertEqual(test_func(1), 6)

    def test_rearg(self):
        def fn(a, b, c):
            return a + b + c

        test_func = fntools.rearg(fn, [2, 0, 1])
        self.assertEqual(test_func(1, 2, 3), 6)

    def test_rest(self):
        def fn(a, b, args):
            return a + b + sum(args)

        test_func = fntools.rest(fn)
        # last two args should be passed to the last argument together
        self.assertEqual(test_func(1, 2, 3, 4), 10)

    def test_spread(self):
        def fn(a, b, c):
            return a + b + c

        test_func = fntools.spread(fn)
        self.assertEqual(test_func([1, 2, 3]), 6)

    def test_unary(self):
        def fn(a, b=None):
            return f"a: {a}, b: {b}"
        self.assertEqual(fn(1, 2), "a: 1, b: 2")

        test_func = fntools.unary(fn)
        self.assertEqual(test_func(1, 2), "a: 1, b: None")

    def test_wrap(self):
        def fn(a, b):
            return a + b

        def wrapper(func, a, b):
            return func(a, b) + 1

        test_func = fntools.wrap(fn, wrapper)
        self.assertEqual(test_func(1, 2), 4)

if __name__ == "__main__":
    unittest.main()
