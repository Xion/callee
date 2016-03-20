"""
Matchers for numbers.
"""
from __future__ import absolute_import

import fractions
import numbers

from callee._compat import IS_PY3
from callee.base import BaseMatcher


__all__ = [
    'Number',
    'Complex', 'Real', 'Float', 'Rational', 'Fraction',
    'Integral', 'Integer', 'Int', 'Long',
]


class NumericMatcher(BaseMatcher):
    """Matches some number type.
    This class shouldn't be used directly.
    """
    #: Number class to match.
    #: Must be overridden in subclasses.
    CLASS = None

    def __init__(self):
        assert self.CLASS, "must specify number type to match"

    def match(self, value):
        return isinstance(value, self.CLASS)

    def __repr__(self):
        return "<%s>" % (self.__class__.__name__,)


class Number(NumericMatcher):
    """Matches any number
    (integer, float, complex, custom number types, etc.).
    """
    CLASS = numbers.Number


class Complex(NumericMatcher):
    """Matches any complex number.

    This *includes* all real, rational, and integer numbers as well,
    which in Python translates to `float`\ s, fractions, and `int`\ egers.
    """
    CLASS = numbers.Complex


# TODO: consider adding a dedicated matcher for the ``complex`` type;
# right now, though, ``IsA(complex)`` and ``Complex() & ~Real()`` are probably
# acceptable workarounds


class Real(NumericMatcher):
    """Matches any real number.

    This includes all rational and integer numbers as well, which in Python
    translates to fractions, and `int`\ egers.
    """
    CLASS = numbers.Real


class Float(NumericMatcher):
    """Matches a floating point number."""

    CLASS = float


class Rational(NumericMatcher):
    """Matches a rational number.
    This includes all `int`\ eger numbers as well.
    """
    CLASS = numbers.Rational


class Fraction(NumericMatcher):
    """Matches a fraction object."""

    CLASS = fractions.Fraction


class Integral(NumericMatcher):
    """Matches any integer.
    This ignores the length of integer's internal representation on Python 2.
    """
    CLASS = int if IS_PY3 else (int, long)


class Integer(NumericMatcher):
    """Matches a regular integer.

    On Python 3, there is no distinction between regular and long integer,
    making this matcher and :class:`Long` equivalent.

    On Python 2, this matches the :class:`int` integers exclusively.
    """
    CLASS = int

#: Alias for :class:`Integer`.
Int = Integer


class Long(NumericMatcher):
    """Matches a long integer.

    On Python 3, this is the same as regular integer, making this matcher
    and :class:`Integer` equivalent.

    On Python 2, this matches the :class:`long` integers exclusively.
    """
    CLASS = int if IS_PY3 else long
