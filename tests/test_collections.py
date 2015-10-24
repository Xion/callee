"""
Tests for collections' matchers.
"""
import collections

import callee.collections as __unit__
from tests import MatcherTestCase


class Iterable(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_zero = lambda self: self.assert_no_match(0)
    test_empty_string = lambda self: self.assert_match('')
    test_empty_list = lambda self: self.assert_match([])
    test_empty_tuple = lambda self: self.assert_match(())
    test_empty_dict = lambda self: self.assert_match({})
    test_empty_generator = lambda self: self.assert_match(x for x in ())
    test_some_string = lambda self: self.assert_match("Alice has a cat")
    test_some_number = lambda self: self.assert_no_match(42)
    test_some_list = lambda self: self.assert_match([1, 2, 3, 5, 8, 13])
    test_some_tuple = lambda self: self.assert_match(('foo', -1, ['bar']))

    def test_some_generator(self):
        gen = (x for x in [1, 2, 5])
        self.assert_match(gen)
        self.assertNotEmpty(
            gen, msg="matcher shouldn't have iterated over the generator")

    test_some_object = lambda self: self.assert_no_match(object())

    def assert_match(self, value):
        return super(Iterable, self).assert_match(__unit__.Iterable(), value)

    def assert_no_match(self, value):
        return super(Iterable, self) \
            .assert_no_match(__unit__.Iterable(), value)


class Generator(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_zero = lambda self: self.assert_no_match(0)
    test_empty_string = lambda self: self.assert_no_match('')
    test_empty_list = lambda self: self.assert_no_match([])
    test_empty_tuple = lambda self: self.assert_no_match(())
    test_empty_dict = lambda self: self.assert_no_match({})
    test_empty_generator = lambda self: self.assert_match(x for x in ())
    test_some_string = lambda self: self.assert_no_match("Alice has a cat")
    test_some_number = lambda self: self.assert_no_match(42)
    test_some_list = lambda self: self.assert_no_match([1, 2, 3, 5, 8, 13])
    test_some_tuple = lambda self: self.assert_no_match(('foo', -1, ['bar']))

    def test_some_generator(self):
        gen = (x for x in [1, 2, 5])
        self.assert_match(gen)
        self.assertNotEmpty(
            gen, msg="matcher shouldn't have iterated over the generator")

    test_some_object = lambda self: self.assert_no_match(object())

    def assert_match(self, value):
        return super(Generator, self).assert_match(__unit__.Generator(), value)

    def assert_no_match(self, value):
        return super(Generator, self) \
            .assert_no_match(__unit__.Generator(), value)


# Ordinary collections

class Sequence(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_zero = lambda self: self.assert_no_match(0)
    test_empty_string = lambda self: self.assert_match('')
    test_empty_list = lambda self: self.assert_match([])
    test_empty_set = lambda self: self.assert_no_match(set())
    test_empty_tuple = lambda self: self.assert_match(())
    test_empty_dict = lambda self: self.assert_no_match({})
    test_empty_generator = lambda self: self.assert_no_match(x for x in ())

    def test_some_string(self):
        s = "Alice has a cat"
        self.assert_match(s)
        self.assert_match(s, of=str)

    test_some_number = lambda self: self.assert_no_match(42)

    def test_some_list(self):
        l = [1, 2, 3, 5, 8, 13]
        self.assert_match(l)
        self.assert_match(l, of=int)

    test_some_tuple = lambda self: self.assert_match(('foo', -1, ['bar']))
    test_some_generator = lambda self: self.assert_no_match(x for x in [1, 2])
    test_some_object = lambda self: self.assert_no_match(object())

    def assert_match(self, value, of=None):
        return super(Sequence, self).assert_match(__unit__.Sequence(of), value)

    def assert_no_match(self, value, of=None):
        return super(Sequence, self) \
            .assert_no_match(__unit__.Sequence(of), value)


class List(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_zero = lambda self: self.assert_no_match(0)
    test_empty_string = lambda self: self.assert_no_match('')
    test_empty_list = lambda self: self.assert_match([])
    test_empty_set = lambda self: self.assert_no_match(set())
    test_empty_tuple = lambda self: self.assert_no_match(())
    test_empty_dict = lambda self: self.assert_no_match({})
    test_empty_generator = lambda self: self.assert_no_match(x for x in ())
    test_some_string = lambda self: self.assert_no_match("Alice has a cat")
    test_some_number = lambda self: self.assert_no_match(42)
    test_some_list = lambda self: self.assert_match([1, 2, 3, 5, 8, 13], int)
    test_some_tuple = lambda self: self.assert_no_match(('foo', -1, ['bar']))
    test_some_generator = lambda self: self.assert_no_match(x for x in [1, 2])
    test_some_object = lambda self: self.assert_no_match(object())

    def assert_match(self, value, of=None):
        return super(List, self).assert_match(__unit__.List(of), value)

    def assert_no_match(self, value, of=None):
        return super(List, self).assert_no_match(__unit__.List(of), value)


class Set(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_zero = lambda self: self.assert_no_match(0)
    test_empty_string = lambda self: self.assert_no_match('')
    test_empty_list = lambda self: self.assert_no_match([])
    test_empty_set = lambda self: self.assert_match(set())
    test_empty_tuple = lambda self: self.assert_no_match(())
    test_empty_dict = lambda self: self.assert_no_match({})
    test_empty_generator = lambda self: self.assert_no_match(x for x in ())
    test_some_string = lambda self: self.assert_no_match("Alice has a cat")
    test_some_number = lambda self: self.assert_no_match(42)
    test_some_list = lambda self: self.assert_no_match([1, 2, 3, 5, 8, 13])
    test_some_set = lambda self: self.assert_match(set([2, 4, 6, 8, 10]), int)
    test_some_tuple = lambda self: self.assert_no_match(('foo', -1, ['bar']))
    test_some_generator = lambda self: self.assert_no_match(x for x in [1, 2])
    test_some_object = lambda self: self.assert_no_match(object())

    def assert_match(self, value, of=None):
        return super(Set, self).assert_match(__unit__.Set(of), value)

    def assert_no_match(self, value, of=None):
        return super(Set, self).assert_no_match(__unit__.Set(of), value)


# Mappings

class CustomDict(collections.MutableMapping):
    """"Custom, no-op mapping class that just wraps a regular Python dict
    but is not a Python dict itself.
    """
    def __init__(self, iterable=(), **kwargs):
        if isinstance(iterable, collections.Mapping):
            iterable = iterable.items()

        self.d = {}
        for k, v in iterable:
            self.d[k] = v
        self.d.update(kwargs)

    def __delitem__(self, key):
        del self.d[key]

    def __getitem__(self, key):
        return self.d[key]

    def __iter__(self):
        return iter(self.d)

    def __len__(self):
        return len(self.d)

    def __setitem__(self, key, value):
        self.d[key] = value


class Mapping(MatcherTestCase):

    def test_invalid_arg(self):
        with self.assertRaises(TypeError):
            self.assert_match(None, of='not a pair of matchers')

    test_none = lambda self: self.assert_no_match(None)
    test_zero = lambda self: self.assert_no_match(0)
    test_empty_string = lambda self: self.assert_no_match('')
    test_empty_list = lambda self: self.assert_no_match([])
    test_empty_set = lambda self: self.assert_no_match(set())
    test_empty_tuple = lambda self: self.assert_no_match(())
    test_empty_dict__regular = lambda self: self.assert_match({})
    test_empty_dict__custom = lambda self: self.assert_match(CustomDict())
    test_empty_generator = lambda self: self.assert_no_match(x for x in ())
    test_some_string = lambda self: self.assert_no_match("Alice has a cat")
    test_some_number = lambda self: self.assert_no_match(42)
    test_some_list = lambda self: self.assert_no_match([1, 2, 3, 5, 8, 13])
    test_some_set = lambda self: self.assert_no_match(set([2, 4, 6, 8, 10]))
    test_some_tuple = lambda self: self.assert_no_match(('foo', -1, ['bar']))

    def test_some_dict__regular(self):
        d = {'a': 1}
        self.assert_match(d)
        self.assert_match(d, of=(str, int))

    def test_some_dict__custom(self):
        d = CustomDict({'a': 1})
        self.assert_match(d)
        self.assert_match(d, of=(str, int))

    test_some_generator = lambda self: self.assert_no_match(x for x in [1, 2])
    test_some_object = lambda self: self.assert_no_match(object())

    def assert_match(self, value, *args, **kwargs):
        return super(Mapping, self)\
            .assert_match(__unit__.Mapping(*args, **kwargs), value)

    def assert_no_match(self, value, *args, **kwargs):
        return super(Mapping, self) \
            .assert_no_match(__unit__.Mapping(*args, **kwargs), value)


class Dict(MatcherTestCase):

    def test_invalid_arg(self):
        with self.assertRaises(TypeError):
            self.assert_match(None, of='not a pair of matchers')

    test_none = lambda self: self.assert_no_match(None)
    test_zero = lambda self: self.assert_no_match(0)
    test_empty_string = lambda self: self.assert_no_match('')
    test_empty_list = lambda self: self.assert_no_match([])
    test_empty_set = lambda self: self.assert_no_match(set())
    test_empty_tuple = lambda self: self.assert_no_match(())
    test_empty_dict__regular = lambda self: self.assert_match({})
    test_empty_dict__custom = lambda self: self.assert_no_match(CustomDict())
    test_empty_generator = lambda self: self.assert_no_match(x for x in ())
    test_some_string = lambda self: self.assert_no_match("Alice has a cat")
    test_some_number = lambda self: self.assert_no_match(42)
    test_some_list = lambda self: self.assert_no_match([1, 2, 3, 5, 8, 13])
    test_some_set = lambda self: self.assert_no_match(set([2, 4, 6, 8, 10]))
    test_some_tuple = lambda self: self.assert_no_match(('foo', -1, ['bar']))

    def test_some_dict__regular(self):
        d = {'a': 1}
        self.assert_match(d)
        self.assert_match(d, of=(str, int))

    def test_some_dict__custom(self):
        d = CustomDict({'a': 1})
        self.assert_no_match(d)
        self.assert_no_match(d, of=(str, int))

    test_some_generator = lambda self: self.assert_no_match(x for x in [1, 2])
    test_some_object = lambda self: self.assert_no_match(object())

    def assert_match(self, value, *args, **kwargs):
        return super(Dict, self) \
            .assert_match(__unit__.Dict(*args, **kwargs), value)

    def assert_no_match(self, value, *args, **kwargs):
        return super(Dict, self) \
            .assert_no_match(__unit__.Dict(*args, **kwargs), value)
