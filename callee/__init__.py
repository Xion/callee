"""
callee
"""
__version__ = "0.1"
__description__ = "Argument matchers for unittest.mock"
__author__ = "Karol Kuczmarski"
__license__ = "Simplified BSD"


from callee.base import And, Eq, Is, Or, Not
from callee.collections import \
    Dict, Generator, Iterable, List, Mapping, Sequence, Set
from callee.general import \
    Any, ArgThat, IsA, Inherits, InstanceOf, Matching, SubclassOf
from callee.numbers import (Complex, Float, Fraction, Int, Integer, Integral,
                            Long, Number, Rational, Real)
from callee.strings import Bytes, String, Unicode


__all__ = [
    'Matcher',
    'Eq', 'Is',
    'Not', 'And', 'Or',

    'Iterable', 'Generator',
    'Sequence', 'List', 'Set',
    'Mapping', 'Dict',

    'Any', 'Matching', 'ArgThat',
    'Callable', 'Function', 'GeneratorFunction',
    'InstanceOf', 'IsA', 'SubclassOf', 'Inherits', 'Type', 'Class',

    'Number',
    'Complex', 'Real', 'Float', 'Rational', 'Fraction',
    'Integral', 'Integer', 'Int', 'Long',

    'String', 'Unicode', 'Bytes',
]


# TODO(xion): operator-based matchers (GreaterThan, ShorterThan, etc.)
# TODO(xion): attribute-based matchers: HasAttr, HasAttrs, Attrs(<attr>=<val>)
# TODO(xion): matchers for positional & keyword arguments
