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
    'Integral', 'Integer', 'Long',
]


class Number(BaseMatcher):
    """Matches any number (integer, float, complex, etc.)."""

    def match(self, value):
        return isinstance(value, numbers.Number)


class NumericMatcher(BaseMatcher):
    """Matches some number type.
    This class shouldn't be used directly.
    """
    #: Abstract number class to match.
    #: If omitted, ``CONCRETE_TYPE`` is used exclusively instead.
    ABSTRACT_CLASS = None

    #: Concrete number type to match if strict matching was chosen.
    #: Must be overridden in subclases.
    CONCRETE_TYPE = None

    def __init__(self, strict=True):
        assert self.CONCRETE_TYPE, "must specify number type to match"

        self.type_ = self.ABSTRACT_CLASS
        if strict or not self.type_:
            self.type_ = self.CONCRETE_TYPE

    def match(self, value):
        return isinstance(value, self.type_)


class Complex(NumericMatcher):
    """Matches a complex number."""

    ABSTRACT_CLASS = numbers.Complex
    CONCRETE_TYPE = complex


class Real(NumericMatcher):
    """Matches a real (floating point) number."""

    ABSTRACT_CLASS = numbers.Real
    CONCRETE_TYPE = float

#: Alias for :class:`Real`.
Float = Real


class Rational(NumericMatcher):
    """Matches a rational number."""

    ABSTRACT_CLASS = numbers.Rational
    CONCRETE_TYPE = fractions.Fraction

#: Alias for :class:`Rational`.
Fraction = Rational


class Integral(NumericMatcher):
    """Matches any integer.
    This ignores the length of integer's internal representation on Python 2.
    """
    ABSTRACT_CLASS = numbers.Integral
    CONCRETE_TYPE = int if IS_PY3 else (int, long)


class Integer(NumericMatcher):
    """Matches a regular integer.

    On Python 3, there is no distinction between regular and long integer,
    making this matchers and :class:`Long` equivalent.

    On Python 2, this matches the :type:`int` integers exclusively.
    """
    CONCRETE_TYPE = int


class Long(NumericMatcher):
    """Matches a long integer.

    On Python 3, this is the same as regular integer, making this matcher
    and :class:`Integer` equivalent.

    On Python 2, this matches the :type:`long` integers exclusively.
    """
    CONCRETE_TYPE = int if IS_PY3 else long
