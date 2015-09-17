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
        return super(Any, self).assert_match(__unit__.Any(), value)


class Matching(MatcherTestCase):
    EVEN = staticmethod(lambda x: x % 2 == 0)
    ODD = staticmethod(lambda x: x % 2 != 0)

    SHORTER_THAN_THREE = staticmethod(lambda x: len(x) < 3)
    LONGER_THAN_THREE = staticmethod(lambda x: len(x) > 3)

    def test_invalid_predicate(self):
        with self.assertRaises(TypeError):
            __unit__.Matching(object())

    def test_none(self):
        self.assert_no_match(None, self.EVEN)
        self.assert_no_match(None, self.ODD)

    def test_zero(self):
        self.assert_match(0, self.EVEN)
        self.assert_no_match(0, self.ODD)

    def test_empty_string(self):
        self.assert_match('', self.SHORTER_THAN_THREE)
        self.assert_no_match('', self.LONGER_THAN_THREE)

    def test_empty_list(self):
        self.assert_match([], self.SHORTER_THAN_THREE)
        self.assert_no_match([], self.LONGER_THAN_THREE)

    def test_empty_tuple(self):
        self.assert_match((), self.SHORTER_THAN_THREE)
        self.assert_no_match((), self.LONGER_THAN_THREE)

    def test_some_string(self):
        s = "Alice has a cat"
        self.assert_no_match(s, self.SHORTER_THAN_THREE)
        self.assert_match(s, self.LONGER_THAN_THREE)

    # Assertion functions

    def assert_match(self, value, predicate):
        return super(Matching, self) \
            .assert_match(__unit__.Matching(predicate), value)

    def assert_no_match(self, value, predicate):
        return super(Matching, self) \
            .assert_no_match(__unit__.Matching(predicate), value)


class InstanceOf(MatcherTestCase):

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            __unit__.InstanceOf(object())

    def test_none(self):
        self.assert_match(None, object)
        self.assert_no_match(None, self.Class)

    def test_zero(self):
        self.assert_match(0, int)
        self.assert_no_match(0, self.Class)

    def test_string(self):
        s = "Alice has a cat"
        self.assert_match(s, str)
        self.assert_no_match(s, self.Class)

    def test_class(self):
        self.assert_match(self.Class(), self.Class)
        self.assert_no_match(self.Class(), int)

    def test_meta(self):
        self.assert_match(self.Class, type)
        self.assert_match(type, type)

    # Utility code

    class Class(object):
        pass

    def assert_match(self, value, type_):
        return super(InstanceOf, self) \
            .assert_match(__unit__.InstanceOf(type_), value)

    def assert_no_match(self, value, type_):
        return super(InstanceOf, self) \
            .assert_no_match(__unit__.InstanceOf(type_), value)
