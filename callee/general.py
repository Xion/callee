"""
General matchers.
"""
import inspect
from itertools import starmap
from operator import itemgetter

from callee._compat import IS_PY3, STRING_TYPES
from callee.base import BaseMatcher, Eq


__all__ = [
    'Any', 'Matching', 'ArgThat', 'Captor',
    'Callable', 'Function', 'GeneratorFunction',
    'InstanceOf', 'IsA', 'SubclassOf', 'Inherits', 'Type', 'Class',
    'Attrs', 'Attr', 'HasAttrs', 'HasAttr',
]


# TODO: introduce custom exception types rather than using built-ins


class Any(BaseMatcher):
    """Matches any object."""

    def match(self, value):
        return True

    def __repr__(self):
        return "<Any>"


class Matching(BaseMatcher):
    """Matches an object that satisfies given predicate."""

    MAX_DESC_LENGTH = 32

    def __init__(self, predicate, desc=None):
        """
        :param predicate: Callable taking a single argument
                          and returning True or False
        :param desc: Optional description of the predicate.
                     This will be displayed as a part of the error message
                     on failed assertion.
        """
        if not callable(predicate):
            raise TypeError(
                "Matching requires a predicate, got %r" % (predicate,))

        self.predicate = predicate
        self.desc = self._validate_desc(desc)

    def _validate_desc(self, desc):
        """Validate the predicate description."""
        if desc is None:
            return desc

        if not isinstance(desc, STRING_TYPES):
            raise TypeError(
                "predicate description for Matching must be a string, "
                "got %r" % (type(desc),))

        # Python 2 mandates __repr__ to be an ASCII string,
        # so if Unicode is passed (usually due to unicode_literals),
        # it should be ASCII-encodable.
        if not IS_PY3 and isinstance(desc, unicode):
            try:
                desc = desc.encode('ascii', errors='strict')
            except UnicodeEncodeError:
                raise TypeError("predicate description must be "
                                "an ASCII string in Python 2")

        return desc

    def match(self, value):
        # Note that any possible exceptions from ``predicate``
        # are intentionally let through, to make it easier to diagnose errors
        # than a plain "no match" response would.
        return bool(self.predicate(value))
        # TODO: translate exceptions from the predicate into our own
        # exception type to not clutter user-visible stracktraces with our code

    def __repr__(self):
        """Return a representation of the matcher."""
        name = getattr(self.predicate, '__name__', None)
        desc = self.desc

        # When no user-provided description is available,
        # use function's own name or even its repr().
        if desc is None:
            # If not a lambda function, we can probably make the representation
            # more readable by showing just the function's own name.
            if name and name != '<lambda>':
                # Where possible, make it a fully qualified name, including
                # the module path. This is either on Python 3.3+
                # (via __qualname__), or when the predicate is
                # a standalone function (not a method).
                qualname = getattr(self.predicate, '__qualname__', name)
                is_method = inspect.ismethod(self.predicate) or \
                    isinstance(self.predicate, staticmethod)
                if qualname != name or not is_method:
                    # Note that this shows inner functions (those defined
                    # locally inside other functions) as if they were global
                    # to the module.
                    # This is why we use colon (:) as separator here, as to not
                    # suggest this is an evaluatable identifier.
                    name = '%s:%s' % (self.predicate.__module__, qualname)
            else:
                # For lambdas and other callable objects,
                # we'll just default to the Python repr().
                name = None
        else:
            # Quote and possibly ellipsize the provided description.
            if len(desc) > self.MAX_DESC_LENGTH:
                ellipsis = '...'
                desc = desc[:self.MAX_DESC_LENGTH - len(ellipsis)] + ellipsis
            desc = '"%s"' % desc

        return "<Matching %s>" % (desc or name or repr(self.predicate))

ArgThat = Matching


class Captor(BaseMatcher):
    """Argument captor.

    You can use :class:`Captor` to "capture" the original argument
    that the mock was called with, and perform custom assertions on it.

    Example::

        captor = Captor()
        mock_foo.assert_called_with(captor)

        # captured value is available as `arg` attribute
        self.assertEquals(captor.arg.some_method(), 42)
        self.assertEquals(captor.arg.some_other_method(), "foo")
    """
    __slots__ = ('matcher', 'value')

    def __init__(self, matcher=None):
        """
        :param matcher: Optional matcher to validate the argument against
                        before it's captured
        """
        if matcher is None:
            matcher = Any()

        if not isinstance(matcher, BaseMatcher):
            raise TypeError("expected a matcher, got %r" % (type(matcher),))
        if isinstance(matcher, Captor):
            raise TypeError("cannot pass a captor to another captor")

        self.matcher = matcher

    def has_value(self):
        """Returns whether the :class:`Captor` has captured a value."""
        return hasattr(self, 'value')

    @property
    def arg(self):
        """The captured argument value."""
        if not self.has_value():
            raise ValueError("no value captured")
        return self.value

    def match(self, value):
        if self.has_value():
            raise ValueError("a value has already been captured")

        if not self.matcher.match(value):
            return False
        self.value = value
        return True

    def __repr__(self):
        """Return a representation of the captor."""
        return "<Captor %r%s>" % (self.matcher,
                                  " (*)" if self.has_value() else "")


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


# TODO: reverse of this matcher (SuperclassOf)
class SubclassOf(TypeMatcher):
    """Matches a class that's a subclass of given type
    (as per `issubclass`).
    """
    def __init__(self, type_):
        """:param type\ _: Type to match against"""
        # TODO: strict= argument
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


# TODO: Module() matcher


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
        for name in self.attr_names:
            # Can't use hasattr() here because it swallows *all* exceptions
            # from attribute access in Python 2.x, not just AttributeError.
            # More details: https://hynek.me/articles/hasattr/
            try:
                getattr(value, name)
            except AttributeError:
                return False

        for name, matcher in self.attr_dict.items():
            # Separately handle retrieving of the attribute value,
            # so that any stray AttributeErrors from the matcher itself
            # are correctly propagated.
            try:
                attrvalue = getattr(value, name)
            except AttributeError:
                return False
            if not matcher.match(attrvalue):
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
