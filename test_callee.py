"""
Unit tests.
"""
try:
    import unittest.mock as mock
except ImportError:
    import mock
import sys

from taipan.testing import TestCase, skipIf, skipUnless

import callee as __unit__


class MatcherTestCase(TestCase):
    """Base class for matcher test cases."""

    def assert_match(self, matcher, value):
        m = mock.Mock()
        m(value)
        m.assert_called_with(matcher)

    def assert_no_match(self, matcher, value):
        m = mock.Mock()
        m(value)
        with self.assertRaises(AssertionError):
            m.assert_called_with(matcher)

IS_PY3 = sys.version[0] == '3'


# General matchers

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


# String matchers

class String(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_empty_string = lambda self: self.assert_match('')
    test_some_string = lambda self: self.assert_match("Alice has a cat")

    @skipIf(IS_PY3, "requires Python 2.x")
    def test_some_bytes__py2(self):
        self.assert_match(bytes("Alice has a cat"))

    @skipUnless(IS_PY3, "requires Python 3.x")
    def test_some_bytes__py3(self):
        self.assert_no_match(bytes("Alice has a cat", 'ascii'))

    test_some_object = lambda self: self.assert_no_match(object())
    test_some_number = lambda self: self.assert_no_match(42)

    def assert_match(self, value):
        super(String, self).assert_match(__unit__.String(), value)

    def assert_no_match(self, value):
        super(String, self).assert_no_match(__unit__.String(), value)


class Unicode(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_empty_unicode = lambda self: self.assert_match(u'')
    test_some_unicode = lambda self: self.assert_match(u"Alice has a cat")

    @skipIf(IS_PY3, "requires Python 2.x")
    def test_some_string__py2(self):
        self.assert_no_match("Alice has a cat")

    @skipUnless(IS_PY3, "requires Python 3.x")
    def test_some_string__py3(self):
        self.assert_match("Alice has a cat")

    test_some_object = lambda self: self.assert_no_match(object())
    test_some_number = lambda self: self.assert_no_match(42)

    def assert_match(self, value):
        super(Unicode, self).assert_match(__unit__.Unicode(), value)

    def assert_no_match(self, value):
        super(Unicode, self).assert_no_match(__unit__.Unicode(), value)


class Bytes(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_empty_unicode = lambda self: self.assert_no_match(u'')
    test_some_unicode = lambda self: self.assert_no_match(u"Alice has a cat")

    @skipIf(IS_PY3, "requires Python 2.x")
    def test_some_string__py2(self):
        self.assert_match("Alice has a cat")

    @skipUnless(IS_PY3, "requires Python 3.x")
    def test_some_string__py3(self):
        self.assert_no_match("Alice has a cat")

    test_some_object = lambda self: self.assert_no_match(object())
    test_some_number = lambda self: self.assert_no_match(42)

    def assert_match(self, value):
        super(Bytes, self).assert_match(__unit__.Bytes(), value)

    def assert_no_match(self, value):
        super(Bytes, self).assert_no_match(__unit__.Bytes(), value)
