"""
callee
"""
__version__ = "0.3.1"
__description__ = "Argument matchers for unittest.mock"
__author__ = "Karol Kuczmarski"
__license__ = "BSD"


from callee.attributes import Attrs, Attr, HasAttrs, HasAttr
from callee.base import \
    And, Either, Eq, Is, IsNot, OneOf, Or, Matcher, Not, Xor
from callee.collections import \
    Dict, Generator, Iterable, List, Mapping, OrderedDict, Sequence, Set
from callee.general import Any, ArgThat, Captor, Matching
from callee.functions import \
    Callable, CoroutineFunction, Function, GeneratorFunction
from callee.numbers import (Complex, Float, Fraction, Int, Integer, Integral,
                            Long, Number, Rational, Real)
from callee.objects import Bytes, Coroutine, FileLike
from callee.operators import (
    Contains,
    Ge, Greater, GreaterOrEqual, GreaterOrEqualTo, GreaterThan, Gt,
    In,
    Le, Less, LessOrEqual, LessOrEqualTo, LessThan,
    Longer, LongerOrEqual, LongerOrEqualTo, LongerThan, Lt,
    Shorter, ShorterOrEqual, ShorterOrEqualTo, ShorterThan)
from callee.strings import \
    EndsWith, Glob, Regex, StartsWith, String, Unicode
from callee.types import InstanceOf, IsA, SubclassOf, Inherits, Type, Class


__all__ = [
    'Matcher',
    'Eq', 'Is', 'IsNot',
    'Not', 'And', 'Or', 'Either', 'OneOf', 'Xor',

    'Attrs', 'Attr', 'HasAttrs', 'HasAttr',

    'Iterable', 'Generator',
    'Sequence', 'List', 'Set',
    'Mapping', 'Dict', 'OrderedDict',

    'Any', 'Matching', 'ArgThat', 'Captor',

    'Callable', 'Function', 'GeneratorFunction',
    'CoroutineFunction',

    'Number',
    'Complex', 'Real', 'Float', 'Rational', 'Fraction',
    'Integral', 'Integer', 'Int', 'Long',

    'Bytes',
    'Coroutine',
    'FileLike',

    'Less', 'LessThan', 'Lt',
    'LessOrEqual', 'LessOrEqualTo', 'Le',
    'Greater', 'GreaterThan', 'Gt',
    'GreaterOrEqual', 'GreaterOrEqualTo', 'Ge',
    'Shorter', 'ShorterThan', 'ShorterOrEqual', 'ShorterOrEqualTo',
    'Longer', 'LongerThan', 'LongerOrEqual', 'LongerOrEqualTo',
    'Contains', 'In',

    'String', 'Unicode',
    'StartsWith', 'EndsWith', 'Glob', 'Regex',

    'InstanceOf', 'IsA', 'SubclassOf', 'Inherits', 'Type', 'Class',
]
