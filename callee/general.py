"""
General matchers.
"""
from callee.base import BaseMatcher


__all__ = [
    'Any',
    'Matching', 'ArgThat', 'InstanceOf', 'IsA',
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
        return bool(self.predicate(value))

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

