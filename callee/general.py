"""
General matchers.
"""
import inspect
from itertools import chain, starmap
from operator import itemgetter

from callee.base import BaseMatcher, Eq


__all__ = [
    'Any', 'Matching', 'ArgThat',
    'Callable', 'Function', 'GeneratorFunction',
    'InstanceOf', 'IsA', 'SubclassOf', 'Inherits', 'Type', 'Class',
    'Attrs', 'Attr', 'HasAttrs', 'HasAttr',
]


# TODO(xion): introduce custom exception types rather than using built-ins


class Any(BaseMatcher):
    """Matches any object."""

    def match(self, value):
        return True

    def __repr__(self):
        return "<Any>"


class Matching(BaseMatcher):
    """Matches an object that satisfies given predicate."""

    # TODO(xion): consider accepting multiple predicates as And() condition
    def __init__(self, predicate):
        """
        :param predicate: Callable taking a single argument
                          and returning True or False
        """
        if not callable(predicate):
            raise TypeError(
                "Matching requires a predicate, got %r" % (predicate,))
        self.predicate = predicate

    def match(self, value):
        try:
            return bool(self.predicate(value))
        except Exception:
            return False

    def __repr__(self):
        # TODO(xion): better representation of the predicate;
        # we could display the code inline for short lambdas, for example
        return "<Matching %r>" % (self.predicate,)

ArgThat = Matching


# Function-related matchers

class FunctionMatcher(BaseMatcher):
    """Matches values of callable types.
    This class shouldn't be used directly.
    """
    def __repr__(self):
        return "<%s>" % (self.__class__.__name__,)


class Callable(FunctionMatcher):
    """Matches any callable object (as per the :func:`callable` function)."""

    def match(self, value):
        return callable(value)


class Function(FunctionMatcher):
    """Matches any Python function."""

    def match(self, value):
        return inspect.isfunction(value)


class GeneratorFunction(FunctionMatcher):
    """Matches a generator function, i.e. one that uses ``yield`` in its body.

    .. note::

        This is distinct from matching a *generator*,
        i.e. an iterable result of calling the generator function,
        or a generator comprehension (``(... for x in ...)``).
        The :class:`~callee.collections.Generator` matcher
        should be used for those objects instead.
    """
    def match(self, value):
        return inspect.isgeneratorfunction(value)


# Type-related matchers

class TypeMatcher(BaseMatcher):
    """Matches an object to a type.
    This class shouldn't be used directly.
    """
    def __init__(self, type_):
        """:param type\ _: Type to match against"""
        if not isinstance(type_, type):
            raise TypeError("%s requires a type, got %r" % (
                self.__class__.__name__, type_))
        self.type_ = type_

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.type_)


class InstanceOf(TypeMatcher):
    """Matches an object that's an instance of given type
    (as per `isinstance`).
    """
    def match(self, value):
        return isinstance(value, self.type_)

IsA = InstanceOf


# TODO(xion): reverse of this matcher (SuperclassOf)
class SubclassOf(TypeMatcher):
    """Matches a class that's a subclass of given type
    (as per `issubclass`).
    """
    def __init__(self, type_):
        """:param type\ _: Type to match against"""
        # TODO(xion): strict= argument
        super(SubclassOf, self).__init__(type_)

    def match(self, value):
        return isinstance(value, type) and issubclass(value, self.type_)

Inherits = SubclassOf


class Type(BaseMatcher):
    """Matches any Python type object."""

    def match(self, value):
        return isinstance(value, type)

    def __repr__(self):
        return "<Type>"


class Class(BaseMatcher):
    """Matches a class (but not any other type object)."""

    def match(self, value):
        return inspect.isclass(value)

    def __repr__(self):
        return "<Class>"


# TODO(xion): Module() matcher


# Attribute-based matchers

class Attrs(BaseMatcher):
    """Matches objects based on their attributes.

    To match successfully, the object needs to:

        * have all the attributes whose names were passed
          as positional arguments (regardless of their values)
        * have the attribute names/values that correspond exactly
          to keyword arguments' names and values

    Examples::

        Attrs('foo')  # `foo` attribute with any value
        Attrs('foo', 'bar')  # `foo` and `bar` attributes with any values
        Attrs(foo=42)  # `foo` attribute with value of 42
        Attrs(bar=Integer())  # `bar` attribute whose value is an integer
        Attrs('foo', bar='x')  # `foo` with any value, `bar` with value of 'x'
    """
    def __init__(self, *args, **kwargs):
        if not (args or kwargs):
            raise TypeError("%s() requires at least one argument" % (
                self.__class__.__name__,))

        self.attr_names = list(args)
        self.attr_dict = dict((k, v if isinstance(v, BaseMatcher) else Eq(v))
                              for k, v in kwargs.items())

    def match(self, value):
        # We also check the keyword-passed attributes here because
        # we don't want to swallow any AttributeError exceptions that a custom
        # matcher for an attribute value may raise.
        # This would be awkward to do with regular try-catch.
        for name in chain(self.attr_names, self.attr_dict.keys()):
            if not hasattr(value, name):
                return False

        for name, matcher in self.attr_dict.items():
            if not matcher.match(getattr(value, name)):
                return False

        return True

    def __repr__(self):
        """Return a representation of the matcher."""
        # get both the names-only and valued attributes and sort them by name
        sentinel = object()
        attrs = [(name, sentinel)
                 for name in self.attr_names] + list(self.attr_dict.items())
        attrs.sort(key=itemgetter(0))

        def attr_repr(name, value):
            # include the value with attribute name whenever necessary
            if value is sentinel:
                return name
            value = value.value if isinstance(value, Eq) else value
            return "%s=%r" % (name, value)

        return "<%s %s>" % (self.__class__.__name__,
                            " ".join(starmap(attr_repr, attrs)))


class Attr(Attrs):
    """Matches objects that have an attribute with given name and value,
    as given by a keyword argument.
    """
    def __init__(self, **kwargs):
        if not len(kwargs) == 1:
            raise TypeError("Attr() requires exactly one keyword argument")
        super(Attr, self).__init__(**kwargs)


class HasAttrs(Attrs):
    """Matches objects that have all of the specified attribute names,
    regardless of their values.
    """
    def __init__(self, *args):
        super(HasAttrs, self).__init__(*args)


class HasAttr(HasAttrs):
    """Matches object that have an attribute with given name,
    regardless of its value.
    """
    def __init__(self, name):
        super(HasAttr, self).__init__(name)
