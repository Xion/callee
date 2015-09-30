"""
Matchers for collections.
"""
from __future__ import absolute_import

import collections
import inspect

from callee.base import BaseMatcher
from callee.general import Any, InstanceOf


__all__ = [
    'Iterable', 'Generator',
    'Sequence', 'List', 'Set',
    'Mapping', 'Dict',
]


class CollectionMatcher(BaseMatcher):
    """Base class for collections' matchers.
    This class shouldn't be used directly.
    """
    #: Collection class to match.
    #: Must be overridden in subclasses.
    CLASS = None

    def __init__(self, of=None):
        """Constructor.
        :param of: Matcher for the collection's elements, or a type.
        """
        assert self.CLASS, "must specify collection type to match"
        self.of = self._validate_argument(of)

    def _validate_argument(self, arg):
        """Validate a type or matcher argument to the constructor."""
        if arg is None:
            return arg

        if isinstance(arg, type):
            return InstanceOf(arg)
        if not isinstance(arg, BaseMatcher):
            raise TypeError(
                "argument of %s can be a type or a matcher (got %r)" % (
                    self.__class__.__name__, type(arg)))

        return arg

    def match(self, value):
        if not isinstance(value, self.CLASS):
            return False
        if self.of is not None:
            return all(self.of == item for item in value)
        return True

    def __repr__(self):
        """Return a readable representation of the matcher
        Used mostly for AssertionError messages in failed tests.

        Example::

            <List[<Integer>]>
        """
        of = "" if self.of is None else "[%r]" % (self.of,)
        return "<%s%s>" % (self.__class__.__name__, of)


class Iterable(CollectionMatcher):
    """Matches any iterable."""

    CLASS = collections.Iterable

    def __init__(self):
        # Unfortunately, we can't allow an ``of`` argument to this matcher.
        #
        # An otherwise unspecified iterable can't be iterated upon
        # more than once safely, because it could be a one-off iterable
        # (e.g. generator comprehension) that's exhausted after a single pass.
        #
        # Thus the sole act of checking the element types would alter
        # the object we're trying to match, and potentially cause all sorts
        # of unexpected behaviors (e.g. tests passing/failing depending on
        # the order of assertions).
        #
        super(Iterable, self).__init__(of=None)


class Generator(BaseMatcher):
    """Matches an iterable that's a generator.

    A generator can be a generator expression ("comprehension")
    or an invocation of a function that `yield`\ s objects.
    """
    def match(self, value):
        return inspect.isgenerator(value)

    def __repr__(self):
        return "<Generator>"


# Ordinary collections

class Sequence(CollectionMatcher):
    """Matches a sequence of given items.

    A sequence is an iterable that has a length and can be indexed.
    """
    CLASS = collections.Sequence


class List(CollectionMatcher):
    """Matches a list of given items."""

    CLASS = list


class Set(CollectionMatcher):
    """Matches a set of given items."""

    CLASS = collections.Set


# TODO(xion): Tuple matcher, with of= that accepts a tuple of matchers
# so that tuple elements can be also matched on


# Mappings

class MappingMatcher(CollectionMatcher):
    """Base class for mapping matchers.
    This class shouldn't be used directly.
    """
    #: Mapping class to match.
    #: Must be overridden in subclasses.
    CLASS = None

    # TODO(xion): allow for keys= and values= arguments that'd assume
    # ``Any()`` for the other if only one was specified
    def __init__(self, of=None):
        assert self.CLASS, "must specify mapping type to match"

        self.keys = self.values = None
        if of is not None:
            try:
                self.keys, self.values = map(self._validate_argument, of)
            except ValueError:
                raise TypeError(
                    "argument of %s has to be a pair of types or matchers" % (
                        self.__class__.__name__,))

    def match(self, value):
        if not isinstance(value, self.CLASS):
            return False
        if self.keys is not None and self.values is not None:
            return all(self.keys == k and self.values == v
                       for k, v in value.items())
        return True

    def __repr__(self):
        """Return a readable representation of the matcher
        Used mostly for AssertionError messages in failed tests.

        Example::

            <Dict[<String> => <Any>]>
        """
        of = ""
        if self.keys is not None or self.values is not None:
            keys = repr(Any() if self.keys is None else self.keys)
            values = repr(Any() if self.values is None else self.values)
            of = "[%s => %s]" % (keys, values)
        return "<%s%s>" % (self.__class__.__name__, of)


class Mapping(MappingMatcher):
    """Matches a mapping of given items."""

    CLASS = collections.Mapping


class Dict(MappingMatcher):
    """Matches a dictionary of given items."""

    CLASS = dict


# TODO(xion): consider adding a matcher for OrderedDict, but in a way
# that doesn't unconditionally require the ordereddict package for Python 2.6
