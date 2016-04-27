"""
callee
"""
__version__ = "0.2"
__description__ = "Argument matchers for unittest.mock"
__author__ = "Karol Kuczmarski"
__license__ = "BSD"


from callee.base import And, Eq, Is, IsNot, Or, Not
from callee.collections import \
    Dict, Generator, Iterable, List, Mapping, Sequence, Set
from callee.general import (Any, ArgThat, Attrs, Attr, HasAttr, HasAttrs,
                            IsA, Inherits, InstanceOf, Matching, SubclassOf)
from callee.numbers import (Complex, Float, Fraction, Int, Integer, Integral,
                            Long, Number, Rational, Real)
from callee.operators import (
    Contains,
    Ge, Greater, GreaterOrEqual, GreaterOrEqualTo, GreaterThan, Gt,
    In,
    Le, Less, LessOrEqual, LessOrEqualTo, LessThan,
    Longer, LongerOrEqual, LongerOrEqualTo, LongerThan, Lt,
    Shorter, ShorterOrEqual, ShorterOrEqualTo, ShorterThan)
from callee.strings import \
    Bytes, EndsWith, Glob, Regex, StartsWith, String, Unicode


__all__ = [
    'Matcher',
    'Eq', 'Is', 'IsNot',
    'Not', 'And', 'Or',

    'Iterable', 'Generator',
    'Sequence', 'List', 'Set',
    'Mapping', 'Dict',

    'Any', 'Matching', 'ArgThat', 'Captor',
    'Callable', 'Function', 'GeneratorFunction',
    'InstanceOf', 'IsA', 'SubclassOf', 'Inherits', 'Type', 'Class',
    'Attrs', 'Attr', 'HasAttrs', 'HasAttr',

    'Number',
    'Complex', 'Real', 'Float', 'Rational', 'Fraction',
    'Integral', 'Integer', 'Int', 'Long',

    'Less', 'LessThan', 'Lt',
    'LessOrEqual', 'LessOrEqualTo', 'Le',
    'Greater', 'GreaterThan', 'Gt',
    'GreaterOrEqual', 'GreaterOrEqualTo', 'Ge',
    'Shorter', 'ShorterThan', 'ShorterOrEqual', 'ShorterOrEqualTo',
    'Longer', 'LongerThan', 'LongerOrEqual', 'LongerOrEqualTo',
    'Contains', 'In',

    'String', 'Unicode', 'Bytes',
    'StartsWith', 'EndsWith', 'Glob', 'Regex',
]


# TODO: matchers for positional & keyword arguments
