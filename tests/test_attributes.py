"""
Tests for attribute-based matchers.
"""
import callee.attributes as __unit__
from tests import MatcherTestCase


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
