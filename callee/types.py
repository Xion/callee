"""
Type-related matchers.
"""
import inspect

from callee.base import BaseMatcher


__all__ = [
    'InstanceOf', 'IsA', 'SubclassOf', 'Inherits', 'Type', 'Class',
]


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


# TODO: reverse of this matcher (TypeOf / ClassOf)
class InstanceOf(TypeMatcher):
    """Matches an object that's an instance of given type
    (as per `isinstance`).
    """
    def __init__(self, type_, exact=False):
        """
        :param type\ _: Type to match against
        :param exact:

            If True, the match will only succeed if the value type matches
            given ``type_`` exactly.
            Otherwise (the default), a subtype of ``type_`` will also match.
        """
        super(InstanceOf, self).__init__(type_)
        self.exact = exact

    def match(self, value):
        if self.exact:
            return type(value) is self.type_
        else:
            return isinstance(value, self.type_)

IsA = InstanceOf


# TODO: reverse of this matcher (SuperclassOf)
class SubclassOf(TypeMatcher):
    """Matches a class that's a subclass of given type
    (as per `issubclass`).
    """
    def __init__(self, type_, strict=False):
        """
        :param type\ _: Type to match against
        :param strict:

            If True, the match if only succeed if the value is a _strict_
            subclass of ``type_`` -- that is, it's not ``type_`` itself.
            Otherwise (the default), any subclass of ``type_`` matches.
        """
        super(SubclassOf, self).__init__(type_)
        self.strict = strict

    def match(self, value):
        if not isinstance(value, type):
            return False
        if not issubclass(value, self.type_):
            return False
        if value is self.type_ and self.strict:
            return False
        return True

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
