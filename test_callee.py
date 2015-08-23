"""
Unit tests.
"""
try:
    import unittest.mock as mock
except ImportError:
    import mock

from taipan.testing import TestCase

import callee as __unit__


class Any(TestCase):
    test_none = lambda self: self._test(None)
    test_zero = lambda self: self._test(0)
    test_empty_string = lambda self: self._test('')
    test_empty_list = lambda self: self._test([])
    test_empty_tuple = lambda self: self._test(())
    test_some_object = lambda self: self._test(object())
    test_some_string = lambda self: self._test("Alice has a cat")
    test_some_number = lambda self: self._test(42)
    test_some_list = lambda self: self._test([1, 2, 3, 5, 8, 13])
    test_some_tuple = lambda self: self._test(('foo', -1, ['bar']))

    def _test(self, *args, **kwargs):
        m = mock.Mock()
        m(*args, **kwargs)
        m.assert_called_with(__unit__.Any())
