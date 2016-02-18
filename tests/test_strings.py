"""
Tests for string matchers.
"""
from itertools import combinations
import re

from taipan.testing import skipIf, skipUnless

from callee._compat import IS_PY3
import callee.strings as __unit__
from tests import MatcherTestCase


# String type matchers

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
        return super(String, self).assert_match(__unit__.String(), value)

    def assert_no_match(self, value):
        return super(String, self).assert_no_match(__unit__.String(), value)


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
        return super(Unicode, self).assert_match(__unit__.Unicode(), value)

    def assert_no_match(self, value):
        return super(Unicode, self).assert_no_match(__unit__.Unicode(), value)


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
        return super(Bytes, self).assert_match(__unit__.Bytes(), value)

    def assert_no_match(self, value):
        return super(Bytes, self).assert_no_match(__unit__.Bytes(), value)


# Infix matchers

class StartsWith(MatcherTestCase):

    def test_exact(self):
        self.assert_match('', '')
        self.assert_match(' ', ' ')
        self.assert_match('foo', 'foo')

    def test_prefix(self):
        self.assert_match('foo', '')  # empty string is a prefix of everything
        self.assert_match('foo', 'f')
        self.assert_match('foo', 'fo')
        self.assert_match(' foo', ' ')

    def test_no_match(self):
        self.assert_no_match('foo', 'b')
        self.assert_no_match(' foo', 'f')
        self.assert_no_match('', 'foo')

    @skipIf(IS_PY3, "requires Python 2.x")
    def test_unicode(self):
        self.assert_match(u'', u'')
        self.assert_match(u' ', u' ')
        self.assert_match(u'foo', u'foo')
        self.assert_match(u'foo', u'')
        self.assert_match(u'foo', u'f')
        self.assert_match(u'foo', u'fo')
        self.assert_match(u' foo', u' ')
        self.assert_no_match(u' foo', u'f')
        self.assert_no_match(u'foo', u'b')
        self.assert_no_match(u'', u'foo')

    # Assertion functions

    def assert_match(self, value, prefix):
        return super(StartsWith, self) \
            .assert_match(__unit__.StartsWith(prefix), value)

    def assert_no_match(self, value, prefix):
        return super(StartsWith, self) \
            .assert_no_match(__unit__.StartsWith(prefix), value)


class EndsWith(MatcherTestCase):

    def test_exact(self):
        self.assert_match('', '')
        self.assert_match(' ', ' ')
        self.assert_match('bar', 'bar')

    def test_suffix(self):
        self.assert_match('bar', '')  # empty string is a suffix of everything
        self.assert_match('bar', 'r')
        self.assert_match('bar', 'ar')
        self.assert_match('bar ', ' ')

    def test_no_match(self):
        self.assert_no_match('bar', 'o')
        self.assert_no_match('bar ', 'r')
        self.assert_no_match('', 'bar')

    @skipIf(IS_PY3, "requires Python 2.x")
    def test_unicode(self):
        self.assert_match(u'', u'')
        self.assert_match(u' ', u' ')
        self.assert_match(u'bar', u'bar')
        self.assert_match(u'bar', u'')
        self.assert_match(u'bar', u'r')
        self.assert_match(u'bar', u'ar')
        self.assert_match(u'bar ', u' ')
        self.assert_no_match(u'bar', u'o')
        self.assert_no_match(u'bar ', u'r')
        self.assert_no_match(u'', u'bar')

    # Assertion functions

    def assert_match(self, value, suffix):
        return super(EndsWith, self) \
            .assert_match(__unit__.EndsWith(suffix), value)

    def assert_no_match(self, value, suffix):
        return super(EndsWith, self) \
            .assert_no_match(__unit__.EndsWith(suffix), value)


# Pattern matchers

class PatternTestCase(MatcherTestCase):
    ALPHABET = 'abcdefghijklmnopqrstvuwxyz'

    # Some tests is O(2^N) wrt to size of this set, so keep it short.
    LETTERS = 'abcdef'

    def suffixes(self):
        for l in range(len(self.LETTERS)):
            for suffix in combinations(self.LETTERS, l):
                return ''.join(suffix)


class Glob(PatternTestCase):

    def test_exact(self):
        self.assert_match('', '')
        self.assert_match(' ', ' ')
        self.assert_match('foo', 'foo')
        self.assert_match('foo!', 'foo!')  # ! is not special outside of []

    def test_escaping(self):
        self.assert_match('foo?', 'foo[?]')
        self.assert_match('foo*', 'foo[*]')

    def test_question_mark(self):
        text = 'foo'
        for char in self.ALPHABET:
            self.assert_match(text + char, text + '?')

    def test_asterisk(self):
        text = 'foo'
        for suffix in self.suffixes():
            self.assert_match(text + suffix, text + '*')

    def test_square_brackets(self):
        text = 'foo'
        for suffix in self.suffixes():
            square_pattern = ''.join('[%s]' % char for char in suffix)
            self.assert_match(text + suffix, text + square_pattern)

    def test_case_sensitive(self):
        self.assert_match('', '', case=True)
        self.assert_match(' ', ' ', case=True)
        self.assert_match('foo', 'foo', case=True)
        self.assert_no_match('foo', 'Foo', case=True)
        self.assert_no_match('Foo', 'foo', case=True)

    def test_case_insensitive(self):
        self.assert_match('', '', case=False)
        self.assert_match(' ', ' ', case=False)
        self.assert_match('foo', 'foo', case=False)
        self.assert_match('foo', 'Foo', case=False)
        self.assert_match('FoO', 'fOo', case=False)

    # Assertion functions

    def assert_match(self, value, pattern, case=__unit__.Glob.DEFAULT_CASE):
        return super(Glob, self) \
            .assert_match(__unit__.Glob(pattern, case), value)

    def assert_no_match(self, value, pattern, case=__unit__.Glob.DEFAULT_CASE):
        return super(Glob, self) \
            .assert_no_match(__unit__.Glob(pattern, case), value)


class Regex(PatternTestCase):

    def test_exact(self):
        self.assert_match('', '')
        self.assert_match(' ', ' ')
        self.assert_match('foo', 'foo')
        self.assert_match('foo^', 'foo')  # ^ is not special outside of []

    def test_escaping(self):
        self.assert_match('foo(', r'foo\(')
        self.assert_match('foo.', r'foo\.')

    def test_dot(self):
        text = 'foo'
        for char in self.ALPHABET:
            self.assert_match(text + char, re.escape(text) + '.')

    def test_dots(self):
        text = 'foo'
        for suffix in self.suffixes():
            self.assert_match(text + suffix, re.escape(text) + '.*')

    def test_square_brackets(self):
        text = 'foo'
        for suffix in self.suffixes():
            square_pattern = ''.join('[%s]' % char for char in suffix)
            self.assert_match(text + suffix, re.escape(text) + square_pattern)

    # Assertion functions

    def assert_match(self, value, pattern):
        return super(Regex, self).assert_match(__unit__.Regex(pattern), value)

    def assert_no_match(self, value, pattern):
        return super(Regex, self) \
            .assert_no_match(__unit__.Regex(pattern), value)
