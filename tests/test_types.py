"""
Tests for type-related matchers.
"""
import callee.types as __unit__
from tests import MatcherTestCase


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

    def test_class__inexact(self):
        self.assert_match(self.Class(), self.Class)
        self.assert_no_match(self.Class(), int)

    def test_class__exact(self):
        self.assert_match(self.Class(), self.Class, exact=True)
        self.assert_no_match(self.Class(), object, exact=True)

    def test_meta(self):
        self.assert_match(self.Class, type)
        self.assert_match(self.Class, type, exact=True)
        self.assert_match(type, type)
        self.assert_match(type, type, exact=True)

    # Utility code

    class Class(object):
        pass

    def assert_match(self, value, type_, exact=False):
        return super(InstanceOf, self) \
            .assert_match(__unit__.InstanceOf(type_, exact), value)

    def assert_no_match(self, value, type_, exact=False):
        return super(InstanceOf, self) \
            .assert_no_match(__unit__.InstanceOf(type_, exact), value)


class SubclassOf(MatcherTestCase):

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            __unit__.SubclassOf(object())

    def test_non_types(self):
        self.assert_no_match(None, object)
        self.assert_no_match(0, object)
        self.assert_no_match("Alice has a cat", object)
        self.assert_no_match((), object)
        self.assert_no_match([], object)

    def test_types(self):
        self.assert_match(self.Class, object)
        self.assert_match(self.Class, self.Class)
        self.assert_match(self.Class, object)
        self.assert_match(object, object)

    # Utility code

    class Class(object):
        pass

    def assert_match(self, value, type_):
        return super(SubclassOf, self) \
            .assert_match(__unit__.SubclassOf(type_), value)

    def assert_no_match(self, value, type_):
        return super(SubclassOf, self) \
            .assert_no_match(__unit__.SubclassOf(type_), value)
