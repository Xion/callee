"""
Tests for numeric matchers.
"""
from fractions import Fraction

from taipan.testing import skipIf, skipUnless

from callee._compat import IS_PY3
import callee.numbers as __unit__
from tests import MatcherTestCase


class Number(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_object = lambda self: self.assert_no_match(object())
    test_iterable = lambda self: self.assert_no_match([])
    test_integer = lambda self: self.assert_match(0)

    @skipIf(IS_PY3, "requires Python 2.x")
    def test_long(self):
        self.assert_match(eval('0l'))

    test_fraction = lambda self: self.assert_match(Fraction(3, 4))
    test_float = lambda self: self.assert_match(0.0)
    test_complex = lambda self: self.assert_match(complex(0, 1))

    def assert_match(self, value):
        return super(Number, self).assert_match(__unit__.Number(), value)

    def assert_no_match(self, value):
        return super(Number, self).assert_no_match(__unit__.Number(), value)


class Complex(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_object = lambda self: self.assert_no_match(object())
    test_iterable = lambda self: self.assert_no_match([])
    test_integer = lambda self: self.assert_match(0)

    @skipIf(IS_PY3, "requires Python 2.x")
    def test_long(self):
        self.assert_match(eval('0l'))

    test_fraction = lambda self: self.assert_match(Fraction(5, 7))
    test_float = lambda self: self.assert_match(0.0)
    test_complex = lambda self: self.assert_match(complex(0, 1))

    def assert_match(self, value):
        return super(Complex, self).assert_match(__unit__.Complex(), value)

    def assert_no_match(self, value):
        return super(Complex, self).assert_no_match(__unit__.Complex(), value)


class Real(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_object = lambda self: self.assert_no_match(object())
    test_iterable = lambda self: self.assert_no_match([])
    test_integer = lambda self: self.assert_match(0)

    @skipIf(IS_PY3, "requires Python 2.x")
    def test_long(self):
        self.assert_match(eval('0l'))

    test_fraction = lambda self: self.assert_match(Fraction(7, 9))
    test_float = lambda self: self.assert_match(0.0)
    test_complex = lambda self: self.assert_no_match(complex(0, 1))

    def assert_match(self, value):
        return super(Real, self).assert_match(__unit__.Real(), value)

    def assert_no_match(self, value):
        return super(Real, self).assert_no_match(__unit__.Real(), value)


class Float(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_object = lambda self: self.assert_no_match(object())
    test_iterable = lambda self: self.assert_no_match([])
    test_integer = lambda self: self.assert_no_match(0)

    @skipIf(IS_PY3, "requires Python 2.x")
    def test_long(self):
        self.assert_no_match(eval('0l'))

    test_fraction = lambda self: self.assert_no_match(Fraction(9, 11))
    test_float = lambda self: self.assert_match(0.0)
    test_complex = lambda self: self.assert_no_match(complex(0, 1))

    def assert_match(self, value):
        return super(Float, self).assert_match(__unit__.Float(), value)

    def assert_no_match(self, value):
        return super(Float, self).assert_no_match(__unit__.Float(), value)


class Integral(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_object = lambda self: self.assert_no_match(object())
    test_iterable = lambda self: self.assert_no_match([])
    test_integer = lambda self: self.assert_match(0)

    @skipIf(IS_PY3, "requires Python 2.x")
    def test_long(self):
        self.assert_match(eval('0l'))

    test_fraction = lambda self: self.assert_no_match(Fraction(7, 9))
    test_float = lambda self: self.assert_no_match(0.0)
    test_complex = lambda self: self.assert_no_match(complex(0, 1))

    def assert_match(self, value):
        return super(Integral, self).assert_match(__unit__.Integral(), value)

    def assert_no_match(self, value):
        return super(Integral, self) \
            .assert_no_match(__unit__.Integral(), value)


class Integer(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_object = lambda self: self.assert_no_match(object())
    test_iterable = lambda self: self.assert_no_match([])
    test_integer = lambda self: self.assert_match(0)

    @skipIf(IS_PY3, "requires Python 2.x")
    def test_long(self):
        self.assert_no_match(eval('0l'))

    test_fraction = lambda self: self.assert_no_match(Fraction(9, 11))
    test_float = lambda self: self.assert_no_match(0.0)
    test_complex = lambda self: self.assert_no_match(complex(0, 1))

    def assert_match(self, value):
        return super(Integer, self).assert_match(__unit__.Integer(), value)

    def assert_no_match(self, value):
        return super(Integer, self).assert_no_match(__unit__.Integer(), value)


class Long(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_object = lambda self: self.assert_no_match(object())
    test_iterable = lambda self: self.assert_no_match([])

    @skipIf(IS_PY3, "requires Python 2.x")
    def test_integer__py2(self):
        self.assert_no_match(0)

    @skipUnless(IS_PY3, "requires Python 3.x")
    def test_integer__py3(self):
        self.assert_match(0)

    @skipIf(IS_PY3, "requires Python 2.x")
    def test_long(self):
        self.assert_match(eval('0l'))

    test_fraction = lambda self: self.assert_no_match(Fraction(9, 11))
    test_float = lambda self: self.assert_no_match(0.0)
    test_complex = lambda self: self.assert_no_match(complex(0, 1))

    def assert_match(self, value):
        return super(Long, self).assert_match(__unit__.Long(), value)

    def assert_no_match(self, value):
        return super(Long, self).assert_no_match(__unit__.Long(), value)
