"""
Compatibility shims for different Python versions.
"""
import sys


__all__ = [
    'IS_PY3',
    'metaclass',
]


IS_PY3 = sys.version_info[0] == 3

STRING_TYPES = (str,) if IS_PY3 else (basestring,)


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
