"""
Matchers for strings.
"""
from callee._compat import IS_PY3
from callee.base import BaseMatcher


__all__ = [
    'String', 'Unicode', 'Bytes',
    'StartsWith', 'EndsWith',
]


# String type matchers

class StringTypeMatcher(BaseMatcher):
    """Matches some string type.
    This class shouldn't be used directly.
    """
    #: String class to match.
    #: Must be overridden in subclasses.
    CLASS = None

    def __init__(self):
        assert self.CLASS, "must specify string type to match"

    def match(self, value):
        return isinstance(value, self.CLASS)

    def __repr__(self):
        return "<%s>" % (self.__class__.__name__,)


class String(StringTypeMatcher):
    """Matches any string.

    On Python 2, this means either :type:`str` or :type:`unicode` objects.
    On Python 3, this means :type:`str` objects exclusively.
    """
    CLASS = str if IS_PY3 else basestring


class Unicode(StringTypeMatcher):
    """Matches a Unicode string.

    On Python 2, this means :type:`unicode` objects exclusively.
    On Python 3, this means :type:`str` objects exclusively.
    """
    CLASS = str if IS_PY3 else unicode


class Bytes(StringTypeMatcher):
    """Matches a byte string, i.e. the :type:`bytes` type.

    On Python 2, this is equivalent to :type:`str` type.
    On Python 3, byte strings are a separate type, distinct from :type:`str`.
    """
    CLASS = bytes


# Infix matchers

# TODO(xion): generalize for all sequence/collection types

class StartsWith(BaseMatcher):
    """Matches a string starting with given prefix."""

    def __init__(self, prefix):
        self.prefix = prefix

    def match(self, value):
        return value.startswith(self.prefix)


class EndsWith(BaseMatcher):
    """Matches a string ending with given suffix."""

    def __init__(self, suffix):
        self.suffix = suffix

    def match(self, value):
        return value.endswith(self.suffix)


# Other

# TODO(xion): Regex matcher
# TODO(xion): Glob matcher
