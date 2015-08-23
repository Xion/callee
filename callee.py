"""
callee
"""
__version__ = "0.0.1"
__description__ = "Argument matcher for unittest.mock"
__author__ = "Karol Kuczmarski"
__license__ = "Simplified BSD"


import sys


__all__ = [
    'Any', 'Not', 'And', 'Or',
    'String', 'Unicode', 'Bytes',
]


IS_PY3 = sys.version[0] == '3'


class Matcher(object):
    """Base class for argument matchers."""

    def __eq__(self, other):
        raise NotImplementedError("matching not implemented")

    def __invert__(self):
        return Not(self)

    def __and__(self, other):
        matchers = other._matchers if isinstance(other, And) else [self]
        return And(self, *matchers)

    def __or__(self, other):
        matchers = other._matchers if isinstance(other, Or) else [self]
        return Or(self, *matchers)


# General matchers

class Any(Matcher):
    """Matches any object."""

    # TODO(xion): add a constructor that may optionally accept at type
    # to perform an `isinstance` check against

    def __eq__(self, other):
        return True


class Not(Matcher):
    """Negates given matcher.

    :param matcher: Matcher object to negate the semantics of
    """
    def __init__(self, matcher):
        assert isinstance(matcher, Matcher), "Not() expects a matcher"
        self._matcher = matcher

    def __eq__(self, other):
        return not self._matcher.__eq__(other)

    def __invert__(self):
        return self._matcher


class And(Matcher):
    """Matches the argument only if all given matchers do."""

    def __init__(self, *matchers):
        assert matchers, "And() expects at least one matcher"
        assert all(isinstance(m, Matcher)
                   for m in matchers), "And() expects matchers"
        self._matchers = list(matchers)

    def __eq__(self, other):
        return all(matcher.__eq__(other) for matcher in self._matchers)


class Or(Matcher):
    """Matches the argument only if at least one given matcher does."""

    def __init__(self, *matchers):
        assert matchers, "Or() expects at least one matcher"
        assert any(isinstance(m, Matcher)
                   for m in matchers), "Or() expects matchers"
        self._matchers = list(matchers)

    def __eq__(self, other):
        return any(matcher.__eq__(other) for matcher in self._matchers)


# String matchers

class StringMatcher(Matcher):
    """Matches some string type."""

    #: String class to match.
    #: Must be overridden in subclasses.
    CLASS = None

    def __init__(self):
        assert self.CLASS, "must specify string type to match"

    def __eq__(self, other):
        return isinstance(other, self.CLASS)


class String(StringMatcher):
    """Matches any string.

    On Python 2, this means either :type:`str` or :type:`unicode` objects.
    On Python 3, this means :type:`str` objects exclusively.
    """
    CLASS = str if IS_PY3 else basestring


class Unicode(StringMatcher):
    """Matches a Unicode string.

    On Python 2, this means :type:`unicode` objects exclusively.
    On Python 3, this means :type:`str` objects exclusively.
    """
    CLASS = str if IS_PY3 else unicode


class Bytes(StringMatcher):
    """Matches a byte string, i.e. the :type:`bytes` type.

    On Python 2, this is equivalent to :type:`str` type.
    On Python 3, byte strings are a separate type, distinct from :type:`str`.
    """
    CLASS = bytes


# TODO(xion): collection matchers (lists, sequences, dicts, ...)
# TODO(xion): predicate matchers (with arbitrary functions)
# TODO(xion): matchers for positional & keyword arguments
