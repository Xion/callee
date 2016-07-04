"""
Matchers for various common kinds of objects.
"""
from callee._compat import asyncio
from callee.base import BaseMatcher


__all__ = ['Coroutine']


class ObjectMatcher(BaseMatcher):
    """Base class for object matchers.
    This class shouldn't be used directly.
    """
    def __repr__(self):
        return "<%s>" % (self.__class__.__name__,)


class Coroutine(ObjectMatcher):
    """Matches an asynchronous coroutine.

    A coroutine is a result of an asynchronous function call, where the async
    function has been defined using ``@asyncio.coroutine`` or the ``async def``
    syntax.

    These are only available in Python 3.4 and above.
    On previous versions of Python, no object will match this matcher.
    """
    def match(self, value):
        return asyncio and asyncio.iscoroutine(value)
