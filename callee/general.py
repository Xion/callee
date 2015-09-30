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

    def __repr__(self):
        return "<Any>"


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

    def __repr__(self):
        # TODO(xion): better representation of the predicate;
        # we could display the code inline for short lambdas, for example
        return "<Matching %r>" % (self.predicate,)

#: Alias for :class:`Matching`.
ArgThat = Matching


# Function-related matchers

class FunctionMatcher(BaseMatcher):
    """Matches values of callable types.
    This class shouldn't be used directly.
    """
    def __repr__(self):
        return "<%s>" % (self.__class__.__name__,)


class Callable(FunctionMatcher):
    """Matches any callable object."""

    def match(self, value):
        return callable(value)


class Function(FunctionMatcher):
    """Matches any Python function."""

    def match(self, value):
        return inspect.isfunction(value)


class GeneratorFunction(FunctionMatcher):
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

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.type_)


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

    def __repr__(self):
        return "<Type>"


class Class(BaseMatcher):
    """Matches a class (but not any other type)."""

    def match(self, value):
        return inspect.isclass(value)

    def __repr__(self):
        return "<Class>"
