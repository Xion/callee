"""
Matchers for various common kinds of objects.
"""
import inspect
import sys

from callee._compat import asyncio, getargspec
from callee.base import BaseMatcher


__all__ = ['Coroutine', 'FileLike']


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


class FileLike(ObjectMatcher):
    """Matches a file-like object.

    In general, a  _file-like object_ is an object you can `read` data from.
    """
    def __init__(self, read=True, write=None):
        """
        :param read:

            Whether only to match objects that do support (``True``)
            or don't support (``False``) reading from them.
            If ``None`` is passed, reading capability is not matched against.

        :param write:

            Whether only to match objects that do support (``True``)
            or don't support (``False``) writing to them.
            If ``None`` is passed, writing capability is not matched against.
        """
        if read is None and write is None:
            raise ValueError("cannot match file-like objects "
                             "that are neither readable nor writable")
        self.read = read if read is None else bool(read)
        self.write = write if write is None else bool(write)

    def match(self, value):
        if self.read is not None:
            if self.read != self._is_readable(value):
                return False
        if self.write is not None:
            if self.write != self._is_writable(value):
                return False
        return True

    def _is_readable(self, obj):
        """Check if the argument is a readable file-like object."""
        try:
            read = getattr(obj, 'read')
        except AttributeError:
            return False
        else:
            return is_method(read, max_arity=1)

    def _is_writable(self, obj):
        """Check if the argument is a writable file-like object."""
        try:
            write = getattr(obj, 'write')
        except AttributeError:
            return False
        else:
            return is_method(write, max_arity=1)

    def __repr__(self):
        """Return a representation of this matcher."""
        requirements = []
        if self.read is not None:
            requirements.append("read" if self.read else "noread")
        if self.write is not None:
            requirements.append("write" if self.write else "nowrite")
        return "<FileLike %s>" % "(%s)" % ",".join(requirements)


# Utility method

def is_method(arg, max_arity=None):
    """Check if argument is a method, optionally of given maximum arity."""
    if not callable(arg):
        return False

    if not any(is_(arg) for is_ in (inspect.ismethod,
                                    inspect.ismethoddescriptor,
                                    inspect.isbuiltin)):
        return False

    try:
        argnames, varargs, kwargs, _ = getargspec(arg)
    except TypeError:
        # On CPython 2.x, built-in methods of file aren't inspectable,
        # so if it's file.read() or file.write(), we can't tell it for sure.
        # Given how this check is being used, assuming the best is probably
        # all we can do here.
        return True
    else:
        if argnames and argnames[0] == 'self':
            argnames = argnames[1:]

    # TODO: verify min_arity as well (e.g. read() of file-like objects
    # may or may not accept an argument, but write() has to)
    if max_arity is None:
        return True
    actual_max_arity = sys.maxsize if varargs or kwargs else len(argnames)
    return int(max_arity) == actual_max_arity
