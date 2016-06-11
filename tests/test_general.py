"""
Tests for general matchers.
"""
import sys

from taipan.testing import skipIf, skipUnless

import callee.general as __unit__
from tests import MatcherTestCase


IS_PY33 = sys.version_info >= (3, 3)


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


# Predicate matcher

class Matching(MatcherTestCase):
    EVEN = staticmethod(lambda x: x % 2 == 0)
    ODD = staticmethod(lambda x: x % 2 != 0)

    SHORTER_THAN_THREE = staticmethod(lambda x: len(x) < 3)
    LONGER_THAN_THREE = staticmethod(lambda x: len(x) > 3)

    def test_invalid_predicate(self):
        with self.assertRaises(TypeError):
            __unit__.Matching(object())

    def test_none(self):
        # Exceptions from the matcher's predicate should be let through.
        with self.assertRaises(TypeError):
            self.assert_no_match(None, self.EVEN)
        with self.assertRaises(TypeError):
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


class MatchingRepr(MatcherTestCase):
    """Tests for the __repr__ method of Matching."""

    def tesc_desc__empty(self):
        matcher = __unit__.Matching(bool, "")
        self.assertIn('""', repr(matcher))

    def test_desc__nonempty(self):
        desc = "Truthy"
        matcher = __unit__.Matching(bool, desc)
        self.assertIn(desc, repr(matcher))

    def test_desc__trimmed(self):
        desc = "Long description with extraneous characters: %s" % (
            "x" * __unit__.Matching.MAX_DESC_LENGTH,)
        matcher = __unit__.Matching(bool, desc)

        self.assertNotIn(desc, repr(matcher))
        self.assertIn("...", repr(matcher))

    def test_lambda(self):
        self.assert_lambda_repr(lambda _: True)

    @skipIf(IS_PY33, "requires Python 2.x or 3.2")
    def test_local_function__py2(self):
        def predicate(_):
            return True
        self.assert_named_repr('predicate', predicate)

    @skipUnless(IS_PY33, "requires Python 3.3+")
    def test_local_function__py33(self):
        def predicate(_):
            return True
        matcher = __unit__.Matching(predicate)
        self.assertIn('<locals>.predicate', repr(matcher))

    def test_function(self):
        self.assert_named_repr('predicate', predicate)

    def test_staticmethod__lambda(self):
        self.assert_lambda_repr(MatchingRepr.staticmethod_lambda)

    @skipIf(IS_PY33, "requires Python 2.x or 3.2")
    def test_staticmethod__function__py2(self):
        # In Python 2, static methods are exactly the same as global functions.
        self.assert_named_repr('staticmethod_function',
                               MatchingRepr.staticmethod_function)

    @skipUnless(IS_PY33, "requires Python 3.3+")
    def test_staticmethod__function__py33(self):
        self.assert_named_repr('MatchingRepr.staticmethod_function',
                               MatchingRepr.staticmethod_function)

    def test_classmethod__lambda(self):
        self.assert_lambda_repr(MatchingRepr.classmethod_lambda)

    @skipIf(IS_PY33, "requires Python 2.x or 3.2")
    def test_classmethod__function__py2(self):
        matcher = __unit__.Matching(MatchingRepr.classmethod_function)
        self.assertIn(' classmethod_function', repr(matcher))

    @skipUnless(IS_PY33, "requires Python 3.3+")
    def test_classmethod__function__py33(self):
        self.assert_named_repr('MatchingRepr.classmethod_function',
                               MatchingRepr.classmethod_function)

    def test_class(self):
        self.assert_named_repr('Class', Class)

    @skipIf(IS_PY33, "requires Python 2.x or 3.2")
    def test_inner_class__py2(self):
        self.assert_named_repr('Class', MatchingRepr.Class)

    @skipUnless(IS_PY33, "requires Python 3.3+")
    def test_inner_class__py33(self):
        self.assert_named_repr('MatchingRepr.Class', MatchingRepr.Class)

    @skipIf(IS_PY33, "requires Python 2.x or 3.2")
    def test_local_class__py2(self):
        class Class(object):
            def __call__(self, _):
                return True
        self.assert_named_repr('Class', Class)

    @skipUnless(IS_PY33, "requires Python 3.3+")
    def test_local_class__py33(self):
        class Class(object):
            def __call__(self, _):
                return True
        matcher = __unit__.Matching(Class)
        self.assertIn('<locals>.Class', repr(matcher))

    def test_callable_object(self):
        matcher = __unit__.Matching(Class())
        self.assertIn('object at', repr(matcher))

    # Utility functons

    def assert_lambda_repr(self, predicate):
        matcher = __unit__.Matching(predicate)
        self.assertIn('<lambda> ', repr(matcher))  # the space matters!

    def assert_named_repr(self, name, predicate):
        matcher = __unit__.Matching(predicate)
        self.assertIn(':' + name, repr(matcher))

    # Test predicates

    staticmethod_lambda = staticmethod(lambda _: True)

    @staticmethod
    def staticmethod_function(_):
        return True

    classmethod_lambda = classmethod(lambda cls, _: True)

    @classmethod
    def classmethod_function(cls, _):
        return True

    class Class(object):
        def __call__(self, _):
            return True


def predicate(_):
    return True


class Class(object):
    def __call__(self, _):
        return True


# Argument captor

class Captor(MatcherTestCase):
    ARG = object()
    FALSE_MATCHER = __unit__.Matching(lambda _: False)

    def test_ctor__no_args(self):
        captor = __unit__.Captor()
        self.assertIsInstance(captor.matcher, __unit__.Any)

    def test_ctor__invalid_matcher(self):
        not_matcher = object()
        with self.assertRaisesRegexp(TypeError, r'expected'):
            __unit__.Captor(not_matcher)

    def test_ctor__matcher(self):
        matcher = __unit__.Matching(bool)
        captor = __unit__.Captor(matcher)
        self.assertIs(matcher, captor.matcher)

    def test_ctor__captor(self):
        captor = __unit__.Captor()
        with self.assertRaisesRegexp(TypeError, r'captor'):
            __unit__.Captor(captor)

    def test_has_value__initial(self):
        captor = __unit__.Captor()
        self.assertFalse(captor.has_value())

    def test_has_value__not_captured(self):
        # When the argument fails the matcher test, it should not be captured.
        captor = __unit__.Captor(self.FALSE_MATCHER)
        captor.match(self.ARG)
        self.assertFalse(captor.has_value())

    def test_has_value__captured(self):
        captor = __unit__.Captor()
        captor.match(self.ARG)
        self.assertTrue(captor.has_value())

    def test_arg__initial(self):
        captor = __unit__.Captor()
        with self.assertRaisesRegexp(ValueError, r'no value'):
            captor.arg

    def test_arg__not_captured(self):
        # When the argument fails the matcher test, it should not be captured.
        captor = __unit__.Captor(self.FALSE_MATCHER)
        captor.match(self.ARG)
        with self.assertRaisesRegexp(ValueError, r'no value'):
            captor.arg

    def test_arg__captured(self):
        captor = __unit__.Captor()
        captor.match(self.ARG)
        self.assertIs(self.ARG, captor.arg)

    def test_match__captured(self):
        captor = __unit__.Captor()
        self.assertTrue(captor.match(self.ARG))

    def test_match___not_captured(self):
        captor = __unit__.Captor(self.FALSE_MATCHER)
        self.assertFalse(captor.match(self.ARG))

    def test_match__double_capture(self):
        captor = __unit__.Captor()
        captor.match(self.ARG)
        with self.assertRaisesRegexp(ValueError, r'already'):
            captor.match(self.ARG)

    def test_repr__not_captured(self):
        captor = __unit__.Captor()
        self.assertNotIn("(*)", repr(captor))

    def test_repr__captured(self):
        captor = __unit__.Captor()
        captor.match(self.ARG)
        self.assertIn("(*)", repr(captor))


# Type-related matchers

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


# Attribute-related matchers

class Attrs(MatcherTestCase):
    VALUE = 42

    def test_match__invalid(self):
        with self.assertRaises(TypeError):
            self.assert_match('unused')

    def test_match__names_only__one(self):
        foo = self.Object(foo=self.VALUE)
        self.assert_match(foo, 'foo')
        self.assert_no_match(foo, 'bar')

    def test_match__names_only__several(self):
        foo_bar = self.Object(foo=self.VALUE, bar=self.VALUE * 2)

        self.assert_match(foo_bar, 'foo')
        self.assert_match(foo_bar, 'bar')
        self.assert_match(foo_bar, 'foo', 'bar')

        self.assert_no_match(foo_bar, 'baz')
        self.assert_no_match(foo_bar, 'foo', 'baz')

    def test_match__values_only__one(self):
        foo = self.Object(foo=self.VALUE)

        self.assert_match(foo, foo=self.VALUE)

        self.assert_no_match(foo, foo=self.VALUE + 1)
        self.assert_no_match(foo, bar=self.VALUE)

    def test_match__values_only__several(self):
        foo_bar = self.Object(foo=self.VALUE, bar=self.VALUE * 2)

        self.assert_match(foo_bar, foo=self.VALUE)
        self.assert_match(foo_bar, bar=self.VALUE * 2)
        self.assert_match(foo_bar, foo=self.VALUE, bar=self.VALUE * 2)

        self.assert_no_match(foo_bar, foo=self.VALUE + 1, bar=self.VALUE)
        self.assert_no_match(foo_bar, foo=self.VALUE, baz=self.VALUE * 2)

    def test_match__both__one_each(self):
        foo_bar = self.Object(foo=self.VALUE, bar=self.VALUE * 2)

        self.assert_match(foo_bar, 'foo', bar=self.VALUE * 2)
        self.assert_match(foo_bar, 'bar', foo=self.VALUE)

        self.assert_no_match(foo_bar, 'foo', baz=self.VALUE * 2)
        self.assert_no_match(foo_bar, 'baz', foo=self.VALUE)

    def test_match__both__mix(self):
        attrs = dict(foo=self.VALUE,
                     bar=self.VALUE * 2,
                     baz=self.VALUE * 2 + 1)
        foo_bar_baz = self.Object(**attrs)

        self.assert_match(foo_bar_baz, 'bar', 'baz', foo=self.VALUE)
        self.assert_match(foo_bar_baz, 'baz',
                          foo=self.VALUE, bar=self.VALUE * 2)
        self.assert_match(foo_bar_baz, **attrs)

        self.assert_no_match(foo_bar_baz, 'qux', **attrs)
        self.assert_no_match(foo_bar_baz, 'foo', 'bar', baz='wrong value')

    def test_repr__names_only__one(self):
        attrs = __unit__.Attrs('foo')

        r = "%r" % attrs
        self.assertIn("foo", r)
        self.assertNotIn("=", r)  # because no value was given

    def test_repr__names_only__several(self):
        attrs = __unit__.Attrs('foo', 'bar')

        r = "%r" % attrs
        self.assertIn("foo", r)
        self.assertIn("bar", r)
        self.assertNotIn("=", r)

    def test_repr__values_only__one(self):
        attrs = __unit__.Attrs(foo=self.VALUE)

        r = "%r" % attrs
        self.assertIn("foo=", r)
        self.assertIn("%r" % self.VALUE, r)

    def test_repr__values_only__several(self):
        attrs = __unit__.Attrs(foo=self.VALUE, bar=self.VALUE * 2)

        r = "%r" % attrs
        self.assertIn("foo=", r)
        self.assertIn("bar=", r)
        self.assertIn("%r" % self.VALUE, r)

    def test_repr__both__one_each(self):
        attrs = __unit__.Attrs('bar', foo=self.VALUE)

        r = "%r" % attrs
        self.assertIn("bar", r)
        self.assertNotIn("bar=", r)  # because this one doesn't have a value
        self.assertIn("foo=", r)
        self.assertIn("%r" % self.VALUE, r)

    def test_repr__both__mix(self):
        attrs = __unit__.Attrs('bar', 'baz', foo=self.VALUE)

        r = "%r" % attrs
        self.assertIn("bar", r)
        self.assertNotIn("bar=", r)
        self.assertIn("baz", r)
        self.assertNotIn("baz=", r)
        self.assertIn("%r" % self.VALUE, r)

    # Utility code

    class Object(object):
        def __init__(self, **attrs):
            for name, value in attrs.items():
                setattr(self, name, value)

    def assert_match(self, value, *args, **kwargs):
        return super(Attrs, self) \
            .assert_match(__unit__.Attrs(*args, **kwargs), value)

    def assert_no_match(self, value, *args, **kwargs):
        return super(Attrs, self) \
            .assert_no_match(__unit__.Attrs(*args, **kwargs), value)
