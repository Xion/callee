"""
callee
"""
__version__ = "0.0.1"
__description__ = "Argument matcher for unittest.mock"
__author__ = "Karol Kuczmarski"
__license__ = "Simplified BSD"


from callee.base import And, Eq, Is, Or, Not
from callee.collections import \
    Dict, Generator, Iterable, List, Mapping, Sequence, Set
from callee.general import \
    Any, ArgThat, IsA, Inherits, InstanceOf, Matching, SubclassOf
from callee.strings import Bytes, String, Unicode


__all__ = [
    'Eq', 'Is',
    'Not', 'And', 'Or',

    'Iterable', 'Generator',
    'Sequence', 'List', 'Set',
    'Mapping', 'Dict',

    'Any', 'Matching', 'ArgThat',
    'Callable', 'Function', 'GeneratorFunction',
    'InstanceOf', 'IsA', 'SubclassOf', 'Inherits', 'Type', 'Class',

    'String', 'Unicode', 'Bytes',
]


# TODO(xion): numeric matchers (Int, Long, Float, Complex, etc.)
# TODO(xion): operator-based matchers (GreaterThan, ShorterThan, etc.)
# TODO(xion): matchers for positional & keyword arguments
