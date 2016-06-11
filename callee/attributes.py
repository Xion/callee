"""
Attribute-based matchers.
"""
from itertools import starmap
from operator import itemgetter

from callee.base import BaseMatcher, Eq


__all__ = [
    'Attrs', 'Attr', 'HasAttrs', 'HasAttr',
]


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
