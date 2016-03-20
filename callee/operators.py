"""
Matchers based on Python operators.
"""
from __future__ import absolute_import

from numbers import Number
import operator

from callee.base import BaseMatcher, Eq, Is, IsNot


__all__ = [
    # those are defined elsewhere but they fit in this module, too
    'Eq', 'Is', 'IsNot',

    'Less', 'LessThan', 'Lt',
    'LessOrEqual', 'LessOrEqualTo', 'Le',
    'Greater', 'GreaterThan', 'Gt',
    'GreaterOrEqual', 'GreaterOrEqualTo', 'Ge',

    'Shorter', 'ShorterThan', 'ShorterOrEqual', 'ShorterOrEqualTo',
    'Longer', 'LongerThan', 'LongerOrEqual', 'LongerOrEqualTo',

    'Contains', 'In',
]


class OperatorMatcher(BaseMatcher):
    """Matches values based on comparison operator and a reference object.
    This class shouldn't be used directly.
    """
    #: Operator function to use for comparing a value with a reference object.
    #: Must be overridden in subclasses.
    OP = None

    #: Transformation function to apply to given value before comparison.
    TRANSFORM = None

    def __init__(self, *args, **kwargs):
        """Accepts a single argument: the reference object to compare against.

        It can be passed either as a single positional parameter,
        or as a single keyword argument -- preferably with a readable name,
        for example::

            some_mock.assert_called_with(Number() & LessOrEqual(to=42))
        """
        assert self.OP, "must specify comparison operator to use"

        # check that we've received exactly one argument,
        # either positional or keyword
        argcount = len(args) + len(kwargs)
        if argcount != 1:
            raise TypeError("a single argument expected, got %s" % argcount)
        if len(args) > 1:
            raise TypeError(
                "at most one positional argument expected, got %s" % len(args))
        if len(kwargs) > 1:
            raise TypeError(
                "at most one keyword argument expected, got %s" % len(kwargs))

        # extract the reference object from arguments
        ref = None
        if args:
            ref = args[0]
        elif kwargs:
            _, ref = kwargs.popitem()

        #: Reference object to compare given values to.
        self.ref = ref

    def match(self, value):
        # Note that any possible exceptions from either ``TRANSFORM`` or ``OP``
        # are intentionally let through, to make it easier to diagnose errors
        # than a plain "no match" response would.
        if self.TRANSFORM is not None:
            value = self.TRANSFORM(value)
        return self.OP(value, self.ref)

    def __repr__(self):
        """Provide an universal representation of the matcher."""
        # Mapping from operator functions to their symbols in Python.
        #
        # There is no point in including ``operator.contains`` due to lack of
        # equivalent ``operator.in_``.
        # These are handled by membership matchers directly.
        operator_symbols = {
            operator.eq: '==',
            operator.ge: '>=',
            operator.gt: '>',
            operator.le: '<=',
            operator.lt: '<',
        }

        # try to get the symbol for the operator, falling back to Haskell-esque
        # "infix function" representation
        op = operator_symbols.get(self.OP)
        if op is None:
            # TODO: convert CamelCase to either snake_case or kebab-case
            op = '`%s`' % (self.__class__.__name__.lower(),)

        return "<%s %s %r>" % (self._get_placeholder_repr(), op, self.ref)

    def _get_placeholder_repr(self):
        """Return the placeholder part of matcher's ``__repr__``."""
        placeholder = '...'
        if self.TRANSFORM is not None:
            placeholder = '%s(%s)' % (self.TRANSFORM.__name__, placeholder)
        return placeholder


# Simple comparisons

# TODO: AlmostEq() for approximate comparisons with epsilon

class Less(OperatorMatcher):
    """Matches values that are smaller (as per ``<`` operator)
    than given object.
    """
    OP = operator.lt

LessThan = Less

Lt = Less


class LessOrEqual(OperatorMatcher):
    """Matches values that are smaller than,
    or equal to (as per ``<=`` operator), given object.
    """
    OP = operator.le

LessOrEqualTo = LessOrEqual

Le = LessOrEqual


class Greater(OperatorMatcher):
    """Matches values that are greater (as per ``>`` operator)
    than given object.
    """
    OP = operator.gt

GreaterThan = Greater

Gt = Greater


class GreaterOrEqual(OperatorMatcher):
    """Matches values that are greater than,
    or equal to (as per ``>=`` operator), given object.
    """
    OP = operator.ge

GreaterOrEqualTo = GreaterOrEqual

Ge = GreaterOrEqual


# Length comparisons

class LengthMatcher(OperatorMatcher):
    """Matches values based on their length, as compared to a reference.
    This class shouldn't be used directly.
    """
    TRANSFORM = len

    def __init__(self, *args, **kwargs):
        super(LengthMatcher, self).__init__(*args, **kwargs)

        # allow the reference to be either a numeric length or another sequence
        # TODO: remember at least the sequence type to make it impossible
        # e.g. to accidentally compare strings and lists by length
        if not isinstance(self.ref, Number):
            self.ref = len(self.ref)


class Shorter(LengthMatcher):
    """Matches values that are shorter (as per ``<`` comparison on ``len``)
    than given value.
    """
    OP = operator.lt

ShorterThan = Shorter


class ShorterOrEqual(LengthMatcher):
    """Matches values that are shorter than,
    or equal in ``len``\ gth to (as per ``<=`` operator), given object.
    """
    OP = operator.le

ShorterOrEqualTo = ShorterOrEqual


class Longer(LengthMatcher):
    """Matches values that are longer (as per ``>`` comparison on ``len``)
    than given value.
    """
    OP = operator.gt

LongerThan = Longer


class LongerOrEqual(LengthMatcher):
    """Matches values that are longer than,
    or equal in ``len``\ gth to (as per ``>=`` operator), given object.
    """
    OP = operator.ge

LongerOrEqualTo = LongerOrEqual


# Membership tests

class Contains(OperatorMatcher):
    """Matches values that contain (as per the ``in`` operator)
    given reference object.
    """
    OP = operator.contains

    def __repr__(self):
        return "<%r in %s>" % (self.ref, self._get_placeholder_repr())


class In(OperatorMatcher):
    """Matches values that are within the reference object
    (as per the ``in`` operator).
    """
    # There is no ``operator.in_``, so we must define the function ourselves.
    OP = staticmethod(lambda value, ref: value in ref)

    def __repr__(self):
        return "<%s in %r>" % (self._get_placeholder_repr(), self.ref)
