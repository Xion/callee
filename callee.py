"""
callee
"""
__version__ = "0.0.1"
__description__ = "Argument matcher for unittest.mock"
__author__ = "Karol Kuczmarski"
__license__ = "Simplified BSD"


import sys


__all__ = [
    'Any',
    'String', 'Unicode', 'Bytes',
]


IS_PY3 = sys.version[0] == '3'


class Matcher(object):
    """Base class for argument matchers."""

    def __eq__(self, other):
        raise NotImplementedError("matching not implemented")

    # TODO(xion): overload & | ~ to work as `and`, `or`, `not`
    # TODO(xion): but also provide And, Or and Not matchers separately


class Any(object):
    """Matches any object."""

    def __eq__(self, other):
        return True


# String matchers

class StringMatcher(object):
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
