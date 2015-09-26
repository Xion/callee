"""
General matchers.
"""
import inspect

from callee.base import BaseMatcher


__all__ = [
    'Any', 'Matching', 'ArgThat',
    'Callable', 'Function', 'GeneratorFunction',
    'InstanceOf', 'IsA', 'SubclassOf', 'Inherits', 'Type', 'Class',
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


# Function-related matchers

class Callable(BaseMatcher):
    """Matches any callable object."""

    def match(self, value):
        return callable(value)


class Function(BaseMatcher):
    """Matches any Python function."""

    def match(self, value):
        return inspect.isfunction(value)


class GeneratorFunction(BaseMatcher):
    """Matches a generator function, i.e. one that uses `yield` in its body.

    Note that this is distinct from matching a _generator_
    which is an iterable result of calling the generator function
    (among other things).
    """
    def match(self, value):
        return inspect.isgeneratorfunction(value)


# Type-related matchers

class TypeMatcher(BaseMatcher):
    """Matches an object to a type.
    This class shouldn't be used directly.
    """
    def __init__(self, type_):
        if not isinstance(type_, type):
            raise TypeError("%s requires a type, got %r" % (
                self.__class__.__name__, type_))
        self.type_ = type_


class InstanceOf(TypeMatcher):
    """Matches an object that's an instance of given type."""

    def match(self, value):
        return isinstance(value, self.type_)

#: Alias for :class:`InstanceOf`.
IsA = InstanceOf


class SubclassOf(TypeMatcher):
    """Matches a class that's a subclass of given type."""

    def __init__(self, type_):
        # TODO(xion): strict= argument
        super(SubclassOf, self).__init__(type_)

    def match(self, value):
        return isinstance(value, type) and issubclass(value, self.type_)

#: Alias for :class:`SubclassOf`.
Inherits = SubclassOf


class Type(BaseMatcher):
    """Matches any Python type."""

    def match(self, value):
        return isinstance(value, type)


class Class(BaseMatcher):
    """Matches a class (but not any other type)."""

    def match(self, value):
        return inspect.isclass(value)
