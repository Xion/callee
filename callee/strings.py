"""
Matchers for strings.
"""
import fnmatch
import re

from callee._compat import IS_PY3
from callee.base import BaseMatcher


__all__ = [
    'String', 'Unicode', 'Bytes',
    'StartsWith', 'EndsWith',
    'Glob', 'Regex',
]


# String type matchers

class StringTypeMatcher(BaseMatcher):
    """Matches some string type.
    This class shouldn't be used directly.
    """
    #: String class to match.
    #: Must be overridden in subclasses.
    CLASS = None

    # TODO: support of= param, so we can assert what characters
    # the string consists of (e.g. letters, digits as iterables of chars;
    # boolean predicate; or matcher)
    def __init__(self):
        assert self.CLASS, "must specify string type to match"

    def match(self, value):
        return isinstance(value, self.CLASS)

    def __repr__(self):
        return "<%s>" % (self.__class__.__name__,)


class String(StringTypeMatcher):
    """Matches any string.

    | On Python 2, this means either :class:`str` or :class:`unicode` objects.
    | On Python 3, this means :class:`str` objects exclusively.
    """
    CLASS = str if IS_PY3 else basestring


class Unicode(StringTypeMatcher):
    """Matches a Unicode string.

    | On Python 2, this means :class:`unicode` objects exclusively.
    | On Python 3, this means :class:`str` objects exclusively.
    """
    CLASS = str if IS_PY3 else unicode


class Bytes(StringTypeMatcher):
    """Matches a byte string, i.e. the :class:`bytes` type.

    | On Python 2, this is equivalent to :class:`str` class.
    | On Python 3, byte strings are separate class, distinct from :class:`str`.
    """
    CLASS = bytes


# Infix matchers

# TODO: generalize for all sequence/collection types

class StartsWith(BaseMatcher):
    """Matches a string starting with given prefix."""

    def __init__(self, prefix):
        self.prefix = prefix

    def match(self, value):
        return value.startswith(self.prefix)

    def __repr__(self):
        return "<StartsWith %r>" % (self.prefix,)


class EndsWith(BaseMatcher):
    """Matches a string ending with given suffix."""

    def __init__(self, suffix):
        self.suffix = suffix

    def match(self, value):
        return value.endswith(self.suffix)

    def __repr__(self):
        return "<EndsWith %r>" % (self.suffix,)


# Pattern matchers

class Glob(BaseMatcher):
    """Matches a string against a Unix shell wildcard pattern.

    See the :mod:`fnmatch` module for more details about those patterns.
    """
    DEFAULT_CASE = 'system'

    #: fnmatch functions that the matchers uses based on case= argument.
    FNMATCH_FUNCTIONS = {
        DEFAULT_CASE: fnmatch.fnmatch,
        True: fnmatch.fnmatchcase,
        False: lambda f, p: fnmatch.fnmatchcase(f.lower(), p.lower()),
    }

    def __init__(self, pattern, case=DEFAULT_CASE):
        """
        :param pattern: Pattern to match against
        :param case:

            Case sensitivity setting. Possible options:

                * ``'system'`` (default): case sensitvity is system-dependent
                * ``True``: matching is case-sensitive
                * ``False``: matching is case-insensitive
        """
        self.pattern = pattern
        try:
            self.fnmatch = self.FNMATCH_FUNCTIONS[case]
        except KeyError:
            raise ValueError("invalid case= argument: %r" % (case,))

    def match(self, value):
        return self.fnmatch(value, self.pattern)

    def __repr__(self):
        return "<Glob %s>" % (self.pattern,)


class Regex(BaseMatcher):
    """Matches a string against a regular expression."""

    def __init__(self, pattern, flags=0):
        """
        :param pattern: Regular expression to match against.
                        It can be given as string,
                        or as a compiled regular expression object
        :param flags: Flags to use with a regular expression passed as string
        """
        if self._is_regex_object(pattern):
            if flags and flags != pattern.flags:
                raise ValueError("conflicting regex flags: %s vs. %s" % (
                    bin(flags), bin(pattern.flags)))
        else:
            pattern = re.compile(pattern, flags)

        self.pattern = pattern

    def _is_regex_object(self, obj):
        return isinstance(obj, type(re.compile('')))

    def match(self, value):
        return self.pattern.match(value)

    def __repr__(self):
        return "<Regex %s>" % (self.pattern.pattern,)


# TODO: matchers for common string formats: Url, Email, IPv4, IPv6
