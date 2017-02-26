# flake8: noqa
"""
Tests for matcher base classes.
"""
import callee.base as __unit__
from tests import MatcherTestCase, TestCase


class BaseMatcherMetaclass(TestCase):
    """Tests for the BaseMatcherMetaclass."""

    def test_validate_class_definition(self):
        """Test for BaseMatcherMetaclass._validate_class_definition."""
        vcd = __unit__.BaseMatcherMetaclass._validate_class_definition

        bases = (object,)
        method = lambda self: None

        vcd('BaseMatcher', bases, __unit__.BaseMatcher.__dict__)
        vcd('Foo', bases, {})  # OK, empty definition
        vcd('Foo', bases, {'foo': 42})  # OK, no methods at all
        vcd('Foo', bases, {'__foo__': 42})  # OK, magic name but not method
        vcd('Foo', bases, {'__foo__': method})  # OK, not BaseMatcher's method
        vcd('Foo', bases, {'__init__': method})  # OK, explicitly allowed
        with self.assertRaises(RuntimeError):
            vcd('Foo', bases, {'__eq__': method})  # trying to mess up!

    def test_is_base_matcher_class_definition(self):
        """Test for BaseMatcherMetaclass._is_base_matcher_class_definition."""
        is_bmcd = \
            __unit__.BaseMatcherMetaclass._is_base_matcher_class_definition

        self.assertFalse(is_bmcd('Foo', {}))  # wrong name
        self.assertFalse(is_bmcd('BaseMatcher', {}))  # needs members
        self.assertFalse(is_bmcd('BaseMatcher', {'foo': 1}))  # needs methods
        self.assertFalse(  # needs methods from same module
            is_bmcd('BaseMatcher', {'foo': lambda self: None}))

        self.assertTrue(is_bmcd('BaseMatcher', __unit__.BaseMatcher.__dict__))

    def test_list_magic_methods(self):
        """Test for BaseMatcherMetaclass._list_magic_methods."""
        lmm = __unit__.BaseMatcherMetaclass._list_magic_methods

        class Foo(object):
            pass
        self.assertItemsEqual([], lmm(Foo))

        class Bar(object):
            def method(self):
                pass
        self.assertItemsEqual([], lmm(Bar))

        class Baz(object):
            def __init__(self):
                pass
            def __rdiv__(self, other):
                return self
        self.assertItemsEqual(['init', 'rdiv'], lmm(Baz))

        class Qux(object):
            def __init__(self):
                pass
            def foo(self):
                pass
        self.assertItemsEqual(['init'], lmm(Qux))

        class Thud(object):
            def __bool__(self):
                return False
            __nonzero__ = __bool__
        self.assertItemsEqual(['bool', 'nonzero'], lmm(Thud))


class Matcher(TestCase):
    """Tests for the Matcher base class."""

    def test_match(self):
        """Test default match() is left to be implemented by subclasses."""
        class Custom(__unit__.Matcher):
            pass
        matcher = Custom()
        with self.assertRaises(NotImplementedError):
            matcher.match(None)

    def test_repr__no_ctor(self):
        """Test default __repr__ of Matcher subclass without a constructor."""
        class Custom(__unit__.Matcher):
            pass
        self.assertEquals("<Custom>", "%r" % Custom())

    def test_repr__argless_ctor__no_state(self):
        """Test default __repr__ of Matcher subclass with argless ctor."""
        class Custom(__unit__.Matcher):
            def __init__(self):
                pass
        self.assertEquals("<Custom>", "%r" % Custom())

    def test_repr__argless_ctor__with_state(self):
        """Test __repr__ of Matcher subclass with argless ctor & state."""
        class Custom(__unit__.Matcher):
            def __init__(self):
                self.foo = 42
        self.assertEquals("<Custom>", "%r" % Custom())

    def test_repr__argful_ctor__no_state(self):
        """Test __repr__ with argful constructor but no actual fields."""
        class Custom(__unit__.Matcher):
            def __init__(self, unused):
                pass
        self.assertEquals("<Custom(...)>", "%r" % Custom('unused'))

    def test_repr__argful_ctor__with_state_from_args(self):
        """Test __repr__ with argful constructor & object fields."""
        class Custom(__unit__.Matcher):
            def __init__(self, foo):
                self.foo = foo

        foo = 'bar'
        self.assertEquals("<Custom(foo=%r)>" % (foo,),
                          "%r" % Custom(foo='bar'))

    def test_repr__argful_ctor__with_unrelated_state(self):
        """Test __repr__ with argful ctor & unrelated object fields."""
        class Custom(__unit__.Matcher):
            def __init__(self, foo):
                self.bar = 42

        self.assertEquals("<Custom(bar=42)>", "%r" % Custom(foo='unused'))


class Eq(MatcherTestCase):
    """Tests for the Eq matcher."""

    def test_regular_objects(self):
        """Test that Eq is a no-op for regular objects."""
        self.assert_match(__unit__.Eq(None), None)
        self.assert_match(__unit__.Eq(0), 0)
        self.assert_match(__unit__.Eq(""), "")
        self.assert_match(__unit__.Eq([]), [])
        self.assert_match(__unit__.Eq(()), ())

        # Arbitary objects are only equal in the `is` sense.
        obj = object()
        self.assert_match(__unit__.Eq(obj), obj)

    def test_matchers(self):
        """Test that Eq allows to treat matchers as values."""
        # Hypothetical objects that we want to check the equality of,
        # where one is by some accident a Matcher.
        eq_by_x = lambda this, other: this.x == getattr(other, 'x', object())
        class RegularValue(object):
            def __init__(self, x):
                self.x = x
            def __eq__(self, other):
                return eq_by_x(self, other)
        class MatcherValue(__unit__.Matcher):
            def __init__(self, x):
                self.x = x
            def match(self, value):
                return eq_by_x(self, value)

        # Matching against a matcher object is an error if Eq isn't used.
        with self.assertRaises(TypeError) as r:
            self.assert_match(MatcherValue(42), MatcherValue(42))
        self.assertIn("incorrect use of matcher object", str(r.exception))

        # It's fine with Eq, though.
        self.assert_match(__unit__.Eq(RegularValue(42)), MatcherValue(42))

    def test_repr(self):
        """Test for the __repr__ method."""
        value = 42
        eq = __unit__.Eq(value)
        self.assert_repr(eq, value)


class LogicalCombinators(MatcherTestCase):
    """Tests for the logical combinators (Not, And, etc.)."""

    def test_not(self):
        test_strings = ['', 'a', '42', 'a13', '99b', '!', '22 ?']
        not_no_digits = ~self.NoDigits()  # i.e. HasDigits
        has_digits = self.HasDigits()
        for s in test_strings:
            self.assertEquals(
                has_digits.match(s), not_no_digits.match(s),
                msg="expected `%r` and `%r` to match %r equivalently" % (
                    has_digits, not_no_digits, s))

    def test_not__repr(self):
        not_all_digits = ~self.AllDigits()
        self.assert_repr(not_all_digits)

    def test_and__impossible(self):
        test_strings = ['', 'a', '42', 'a13', '99b']
        impossible = self.AllDigits() & self.NoDigits()
        for s in test_strings:
            self.assertFalse(
                impossible.match(s),
                msg="%r matched an impossible matcher %r" % (s, impossible))

    def test_and__idempotent(self):
        test_strings = ['', 'a', '42', 'a13', '99b', '!', '22 ?']
        all_digits_and_all_digits = self.AllDigits() & self.AllDigits()
        all_digits = self.AllDigits()
        for s in test_strings:
            self.assertEquals(
                all_digits.match(s), all_digits_and_all_digits.match(s),
                msg="expected `%r` and `%r` to match %r equivalently" % (
                    all_digits, all_digits_and_all_digits, s))

    def test_and__regular(self):
        test_strings = ['', '42', '31337', 'abcdef', 'a42', '22?']
        short_and_digits = self.Short() & self.AllDigits()
        short_digits = self.ShortDigits()
        for s in test_strings:
            self.assertEquals(
                short_digits.match(s), short_and_digits.match(s),
                msg="expected `%r` and `%r` to match %r equivalently" % (
                    short_digits, short_and_digits, s))

    def test_and__repr(self):
        short_and_digits = self.Short() & self.AllDigits()
        self.assert_repr(short_and_digits)

    def test_or__trivially_true(self):
        test_strings = ['', 'abc', '123456789', 'qwerty?', '!!!!one']
        true = self.Short() | self.Long()
        for s in test_strings:
            self.assertTrue(
                true.match(s),
                msg="%r didn't match a trivially true matcher %r" % (s, true))

    def test_or__idempotent(self):
        test_strings = ['', '42', '31337', 'abcdef', 'a42', '22?']
        short_or_short = self.Short() | self.Short()
        short = self.Short()
        for s in test_strings:
            self.assertEquals(
                short.match(s), short_or_short.match(s),
                msg="expected `%r` and `%r` to match %r equivalently" % (
                    short, short_or_short, s))

    def test_or__regular(self):
        test_strings = ['', '42', '31337', 'abcdef', 'qwerty55', 'a42', '22?']
        has_digits_or_long = self.HasDigits() | self.Long()
        long_or_has_digits = self.LongOrHasDigits()
        for s in test_strings:
            self.assertEquals(
                long_or_has_digits.match(s), has_digits_or_long.match(s),
                msg="expected `%r` and `%r` to match %r equivalently" % (
                    long_or_has_digits, has_digits_or_long, s))

    def test_or__repr(self):
        has_digits_or_short = self.HasDigits() | self.Short()
        self.assert_repr(has_digits_or_short)

    def test_xor__impossible(self):
        test_strings = ['', 'a', '42', 'a13', '99b', '!', '22 ?']
        impossible = self.HasDigits() ^ self.HasDigits()  # a^a <=> ~a
        for s in test_strings:
            self.assertFalse(
                impossible.match(s),
                msg="%r matched an impossible matcher" % (s,))

    def test_xor__trivially_true(self):
        test_strings = ['', 'abc', '123456789', 'qwerty?', '!!!!one']
        true = self.NoDigits() ^ self.HasDigits()
        for s in test_strings:
            self.assertTrue(
                true.match(s),
                msg="%r didn't match a trivially true matcher %r" % (s, true))

    def test_xor__as_and_not(self):
        test_strings = ['', '42', '31337', 'abcdef', 'a42', '22?']
        any_xor_all_digits = self.HasDigits() ^ self.AllDigits()
        only_some_digits = self.HasDigits() & ~self.AllDigits()
        for s in test_strings:
            # Note that the truth of assertion is specific to those predicates:
            # the second one implies the first one.
            self.assertEquals(
                only_some_digits.match(s), any_xor_all_digits.match(s),
                msg="expected `%r` and `%r` to match %r equivalently" % (
                    only_some_digits, any_xor_all_digits, s))

    def test_xor__repr(self):
        all_digits_xor_short = self.AllDigits() ^ self.Short()
        self.assert_repr(all_digits_xor_short)

    # Utility code

    class NoDigits(__unit__.Matcher):
        def match(self, value):
            return all(not c.isdigit() for c in value)

    class HasDigits(__unit__.Matcher):
        def match(self, value):
            return any(c.isdigit() for c in value)

    class AllDigits(__unit__.Matcher):
        def match(self, value):
            return value.isdigit()

    class Short(__unit__.Matcher):
        def match(self, value):
            return len(value) < 5

    class ShortDigits(__unit__.Matcher):
        def match(self, value):
            return value.isdigit() and len(value) < 5

    class Long(__unit__.Matcher):
        def match(self, value):
            return len(value) >= 5

    class LongOrHasDigits(__unit__.Matcher):
        def match(self, value):
            return len(value) >= 5 or any(c.isdigit() for c in value)
