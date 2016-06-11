"""
Matchers related to functions and other similar callables.
"""
import inspect

from callee._compat import asyncio
from callee.base import BaseMatcher


__all__ = [
    'Callable', 'Function', 'GeneratorFunction',
    'Coroutine', 'CoroutineFunction',
]


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


# TODO: this needs a better place, since it's basically what Generator is
# to GeneratorFunction; perhaps we need a dedicated module for matchers for
# async-related objects (coroutines, futures, tasks, etc.),
# or just various Python "builtin" objects, like file-like
class Coroutine(FunctionMatcher):
    """Matches an asynchronous coroutine.

    A coroutine is a result of an asynchronous function call, where the async
    function has been defined using ``@asyncio.coroutine`` or the ``async def``
    syntax.

    These are only available in Python 3.4 and above.
    On previous versions of Python, no object will match this matcher.
    """
    def match(self, value):
        return asyncio and asyncio.iscoroutine(value)


class CoroutineFunction(FunctionMatcher):
    """Matches a coroutine function.

    A coroutine function is an asynchronous function defined using the
    ``@asyncio.coroutine`` or the ``async def`` syntax.

    These are only available in Python 3.4 and above.
    On previous versions of Python, no object will match this matcher.
    """
    def match(self, value):
        return asyncio and asyncio.iscoroutinefunction(value)
