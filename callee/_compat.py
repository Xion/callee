"""
Compatibility shims for different Python versions.
"""
from __future__ import absolute_import

try:
    import asyncio
except ImportError:
    asyncio = None
try:
    from collections import OrderedDict  # Python 2.7+
except ImportError:
    try:
        from ordereddict import OrderedDict  # Python 2.6 with the shim library
    except ImportError:
        OrderedDict = None
import inspect
import sys


__all__ = [
    'asyncio',
    'OrderedDict',
    'IS_PY3',
    'STRING_TYPES', 'casefold',
    'metaclass',
    'getargspec',
]


IS_PY3 = sys.version_info[0] == 3

STRING_TYPES = (str,) if IS_PY3 else (basestring,)
casefold = getattr(str, 'casefold', None) or (lambda s: s.lower())


class MetaclassDecorator(object):
    """Decorator for creating a class through a metaclass.

    Unlike ``__metaclass__`` attribute from Python 2, or ``metaclass=`` keyword
    argument from Python 3, the ``@metaclass`` decorator works with both
    versions of the language.

    Example::

        @metaclass(MyMetaclass)
        class MyClass(object):
            pass
    """
    def __init__(self, meta):
        if not issubclass(meta, type):
            raise TypeError(
                "expected a metaclass, got %s instead" % type(meta).__name__)
        self.metaclass = meta

    def __call__(self, cls):
        """Apply the decorator to given class.

        This recreates the class using the previously supplied metaclass.
        """
        # Copyright (c) Django Software Foundation and individual contributors.
        # All rights reserved.

        original_dict = cls.__dict__.copy()
        original_dict.pop('__dict__', None)
        original_dict.pop('__weakref__', None)

        slots = original_dict.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slot in slots:
                original_dict.pop(slot)

        return self.metaclass(cls.__name__, cls.__bases__, original_dict)

metaclass = MetaclassDecorator
del MetaclassDecorator


def getargspec(obj):
    """Portable version of inspect.getargspec().

    Necessary because the original is no longer available
    starting from Python 3.6.

    :return: 4-tuple of (argnames, varargname, kwargname, defaults)

    Note that distinction between positional-or-keyword and keyword-only
    parameters will be lost, as the original getargspec() doesn't honor it.
    """
    try:
        return inspect.getargspec(obj)
    except AttributeError:
        pass  # we let a TypeError through

    # translate the signature object back into the 4-tuple
    argnames = []
    varargname, kwargname = None, None
    defaults = []
    for name, param in inspect.signature(obj):
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            varargname = name
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            kwargname = name
        else:
            argnames.append(name)
            if param.default is not inspect.Parameter.empty:
                defaults.append(param.default)
    defaults = defaults or None

    return argnames, varargname, kwargname, defaults
