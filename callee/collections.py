"""
Matchers for collections.
"""
from __future__ import absolute_import

try:
    import collections.abc
    abc = collections.abc
except ImportError:
    import collections
    abc = collections

import inspect

from callee._compat import OrderedDict as _OrderedDict
from callee.base import BaseMatcher
from callee.general import Any
from callee.types import InstanceOf


__all__ = [
    'Iterable', 'Generator',
    'Sequence', 'List', 'Set',
    'Mapping', 'Dict', 'OrderedDict',
]


class CollectionMatcher(BaseMatcher):
    """Base class for collections' matchers.
    This class shouldn't be used directly.
    """
    #: Collection class to match.
    #: Must be overridden in subclasses.
    CLASS = None

    def __init__(self, of=None):
        """
        :param of: Optional matcher for the elements,
                   or the expected type of the elements.
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
        """Return a readable representation of the matcher.
        Used mostly for AssertionError messages in failed tests.

        Example::

            <List[<Integer>]>
        """
        of = "" if self.of is None else "[%r]" % (self.of,)
        return "<%s%s>" % (self.__class__.__name__, of)


class Iterable(CollectionMatcher):
    """Matches any iterable."""

    CLASS = abc.Iterable

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
    or an invocation of a generator function (one that ``yield``\ s objects).

    .. note::

        To match a *generator function* itself, you should use the
        :class:`~callee.functions.GeneratorFunction` matcher instead.
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
    CLASS = abc.Sequence


class List(CollectionMatcher):
    """Matches a :class:`list` of given items."""

    CLASS = list


class Set(CollectionMatcher):
    """Matches a :class:`set` of given items."""

    CLASS = abc.Set


# TODO: Tuple matcher, with of= that accepts a tuple of matchers
# so that tuple elements can be also matched on


# Mappings

class MappingMatcher(CollectionMatcher):
    """Base class for mapping matchers.
    This class shouldn't be used directly.
    """
    #: Mapping class to match.
    #: Must be overridden in subclasses.
    CLASS = None

    def __init__(self, *args, **kwargs):
        """Constructor can be invoked either with parameters described below
        (given as keyword arguments), or with two positional arguments:
        matchers/types for dictionary keys & values::

            Dict(String(), int)  # dict mapping strings to ints

        :param keys: Matcher for dictionary keys.
        :param values: Matcher for dictionary values.
        :param of: Matcher for dictionary items, or a tuple of matchers
                   for keys & values, e.g. ``(String(), Integer())``.
                   Cannot be provided if either ``keys`` or ``values``
                   is also passed.

        """
        assert self.CLASS, "must specify mapping type to match"
        self._initialize(*args, **kwargs)

    def _initialize(self, *args, **kwargs):
        """Initiaize the mapping matcher with constructor arguments."""
        self.items = None
        self.keys = None
        self.values = None

        if args:
            if len(args) != 2:
                raise TypeError("expected exactly two positional arguments, "
                                "got %s" % len(args))
            if kwargs:
                raise TypeError(
                    "expected positional or keyword arguments, not both")

            # got positional arguments only
            self.keys, self.values = map(self._validate_argument, args)
        elif kwargs:
            has_kv = 'keys' in kwargs and 'values' in kwargs
            has_of = 'of' in kwargs
            if not (has_kv or has_of):
                raise TypeError("expected keys/values or items matchers, "
                                "but got: %s" % list(kwargs.keys()))
            if has_kv and has_of:
                raise TypeError(
                    "expected keys & values, or items matchers, not both")

            if has_kv:
                # got keys= and values= matchers
                self.keys = self._validate_argument(kwargs['keys'])
                self.values = self._validate_argument(kwargs['values'])
            else:
                # got of= matcher, which can be a tuple of matchers,
                # or a single matcher for dictionary items
                of = kwargs['of']
                if isinstance(of, tuple):
                    try:
                        # got of= as tuple of matchers
                        self.keys, self.values = \
                            map(self._validate_argument, of)
                    except ValueError:
                        raise TypeError(
                            "of= tuple has to be a pair of matchers/types" % (
                                self.__class__.__name__,))
                else:
                    # got of= as a single matcher
                    self.items = self._validate_argument(of)

    def match(self, value):
        if not isinstance(value, self.CLASS):
            return False

        if self.items is not None:
            return all(self.items == i for i in value.items())
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

        if self.items is not None:
            of = "[%r]" % self.items

        if self.keys is not None or self.values is not None:
            keys = repr(Any() if self.keys is None else self.keys)
            values = repr(Any() if self.values is None else self.values)
            of = "[%s => %s]" % (keys, values)

        return "<%s%s>" % (self.__class__.__name__, of)


class Mapping(MappingMatcher):
    """Matches a mapping of given items."""

    CLASS = abc.Mapping


class Dict(MappingMatcher):
    """Matches a dictionary (:class:`dict`) of given items."""

    CLASS = dict


class OrderedDict(MappingMatcher):
    """Matches an ordered dictionary (:class:`collections.OrderedDict`)
    of given items.

    On Python 2.6, this requires the ordereddict backport package.
    Otherwise, no object will match this matcher.
    """
    CLASS = _OrderedDict

    def __init__(self, *args, **kwargs):
        """For more information about arguments,
        see the documentation of :class:`Dict`.
        """
        # Override the constructor from the base matcher class
        # without asserting that CLASS is not None, because it legimately will
        # be on Python 2.6 without the ordereddict package.
        self._initialize(*args, **kwargs)

    def match(self, value):
        if self.CLASS is None:
            return False
        return super(OrderedDict, self).match(value)
