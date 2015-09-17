"""
callee
"""
__version__ = "0.0.1"
__description__ = "Argument matcher for unittest.mock"
__author__ = "Karol Kuczmarski"
__license__ = "Simplified BSD"


from callee.base import And, Or, Not
from callee.general import \
    Any, ArgThat, IsA, Inherits, InstanceOf, Matching, SubclassOf
from callee.strings import Bytes, String, Unicode


__all__ = [
    'Not', 'And', 'Or',
    'Any',
    'Matching', 'ArgThat', 'InstanceOf', 'IsA', 'SubclassOf', 'Inherits',
    'String', 'Unicode', 'Bytes',
]


# TODO(xion): operator-based matchers (GreaterThan, ShorterThan, etc.)
# TODO(xion): collection matchers (lists, sequences, dicts, ...)
# TODO(xion): matchers for positional & keyword arguments
