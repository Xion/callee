"""
Tests for string matchers.
"""
from taipan.testing import skipIf, skipUnless

from callee._compat import IS_PY3
import callee.strings as __unit__
from tests import MatcherTestCase


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
