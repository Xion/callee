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
    def __init__(self, type_):
        """:param type\ _; Type to match against"""
        # TODO: strict= argument
        super(InstanceOf, self).__init__(type_)

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
