"""
Tests for general matchers.
"""
from tests import MatcherTestCase
import callee.general as __unit__


class Any(MatcherTestCase):
    test_none = lambda self: self.assert_match(None)
    test_zero = lambda self: self.assert_match(0)
    test_empty_string = lambda self: self.assert_match('')
    test_empty_list = lambda self: self.assert_match([])
    test_empty_tuple = lambda self: self.assert_match(())
    test_some_object = lambda self: self.assert_match(object())
    test_some_string = lambda self: self.assert_match("Alice has a cat")
    test_some_number = lambda self: self.assert_match(42)
    test_some_list = lambda self: self.assert_match([1, 2, 3, 5, 8, 13])
    test_some_tuple = lambda self: self.assert_match(('foo', -1, ['bar']))

    def assert_match(self, value):
        super(Any, self).assert_match(__unit__.Any(), value)
