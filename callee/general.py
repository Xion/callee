"""
General matchers.
"""
from callee.base import BaseMatcher


__all__ = [
    'Any',
    'Matching', 'ArgThat', 'InstanceOf', 'IsA', 'SubclassOf', 'Inherits',
]


# TODO(xion): introduce custom exception types rather than using built-ins


class Any(BaseMatcher):
    """Matches any object."""

    def match(self, value):
        return True


class Matching(BaseMatcher):
    """Matches an object that satisfies given predicate."""

    def __init__(self, predicate):
        if not callable(predicate):
            raise TypeError(
                "Matching requires a predicate, got %r" % (predicate,))
        self.predicate = predicate

    def match(self, value):
        try:
            return bool(self.predicate(value))
        except Exception:
            return False

#: Alias for :class:`Matching`.
ArgThat = Matching


class InstanceOf(BaseMatcher):
    """Matches an object that's an instance of given type."""

    def __init__(self, type_):
        if not isinstance(type_, type):
            raise TypeError("InstanceOf requires a type, got %r" % (type_,))
        self.type_ = type_

    def match(self, value):
        return isinstance(value, self.type_)

#: Alias for :class:`InstanceOf`.
IsA = InstanceOf


class SubclassOf(BaseMatcher):
    """Matches a class that's a subclass of given type."""

    def __init__(self, type_):
        # TODO(xion): strict= argument
        if not isinstance(type_, type):
            raise TypeError("SubclassOf requires a type, got %r" % (type_,))
        self.type_ = type_

    def match(self, value):
        return isinstance(value, type) and issubclass(value, self.type_)

#: Alias for :class:`SubclassOf`.
Inherits = SubclassOf
