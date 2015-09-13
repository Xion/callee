"""
callee
"""
__version__ = "0.0.1"
__description__ = "Argument matcher for unittest.mock"
__author__ = "Karol Kuczmarski"
__license__ = "Simplified BSD"


import sys


__all__ = [
    'Any', 'Matching', 'InstanceOf', 'IsA',
    'Not', 'And', 'Or',
    'String', 'Unicode', 'Bytes',
]


# TODO(xion): introduce custom exception types rather than using built-ins


IS_PY3 = sys.version[0] == '3'


class Matcher(object):
    """Base class for argument matchers."""

    def match(self, value):
        raise NotImplementedError("matching not implemented")

    # TODO(xion): prevent the methods below from being overridden via metaclass

    def __eq__(self, other):
        if isinstance(other, Matcher):
            # TODO(xion): although this most likely indicates that a Matcher
            # has been used in production code (and thus passed to a mock),
            # this is technically a valid use case, so we should introduce
            # an Eq matcher that allows it for the miniscule number of users
            # that require it, while retaining this sanity check for others
            raise TypeError(
                "incorrect use of matcher object as a value to match on")
        return self.match(other)

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

    def match(self, value):
        return True


class Matching(Matcher):
    """Matches an object that satisfies given predicate."""

    def __init__(self, predicate):
        if not callable(predicate):
            raise TypeError(
                "Matching requires a predicate, got %r" % (predicate,))
        self.predicate = predicate

    def match(self, value):
        return bool(self.predicate(value))


class InstanceOf(Matcher):
    """Matches an object that's an instance of given type."""

    def __init__(self, type_):
        if not isinstance(type_, type):
            raise TypeError("InstanceOf requires a type, got %r" % (type_,))
        self.type_ = type_

    def match(self, value):
        return isinstance(value, self.type_)

#: Alias for :class:`InstanceOf`.
IsA = InstanceOf


# Logical combinators for matchers

class Not(Matcher):
    """Negates given matcher.

    :param matcher: Matcher object to negate the semantics of
    """
    def __init__(self, matcher):
        assert isinstance(matcher, Matcher), "Not() expects a matcher"
        self._matcher = matcher

    def match(self, value):
        return not self._matcher.match(value)

    def __invert__(self):
        return self._matcher


class And(Matcher):
    """Matches the argument only if all given matchers do."""

    def __init__(self, *matchers):
        assert matchers, "And() expects at least one matcher"
        assert all(isinstance(m, Matcher)
                   for m in matchers), "And() expects matchers"
        self._matchers = list(matchers)

    def match(self, value):
        return all(matcher.match(value) for matcher in self._matchers)


class Or(Matcher):
    """Matches the argument only if at least one given matcher does."""

    def __init__(self, *matchers):
        assert matchers, "Or() expects at least one matcher"
        assert any(isinstance(m, Matcher)
                   for m in matchers), "Or() expects matchers"
        self._matchers = list(matchers)

    def match(self, value):
        return any(matcher.match(value) for matcher in self._matchers)


# String matchers

class StringMatcher(Matcher):
    """Matches some string type."""

    #: String class to match.
    #: Must be overridden in subclasses.
    CLASS = None

    def __init__(self):
        assert self.CLASS, "must specify string type to match"

    def match(self, value):
        return isinstance(value, self.CLASS)


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
