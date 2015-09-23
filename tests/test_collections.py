"""
Tests for collections' matchers.
"""
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

        # ensure that the generator is still usable after the test
        # (i.e. the matcher didn't go over it, which would exhaust it)
        for x in gen:
            return
        self.fail("matcher shouldn't have iterated over the passed generator")

    test_some_object = lambda self: self.assert_no_match(object())

    def assert_match(self, value):
        return super(Iterable, self).assert_match(__unit__.Iterable(), value)

    def assert_no_match(self, value):
        return super(Iterable, self) \
            .assert_no_match(__unit__.Iterable(), value)


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
    test_empty_dict = lambda self: self.assert_match({})
    test_empty_generator = lambda self: self.assert_no_match(x for x in ())
    test_some_string = lambda self: self.assert_no_match("Alice has a cat")
    test_some_number = lambda self: self.assert_no_match(42)
    test_some_list = lambda self: self.assert_no_match([1, 2, 3, 5, 8, 13])
    test_some_set = lambda self: self.assert_no_match(set([2, 4, 6, 8, 10]))
    test_some_tuple = lambda self: self.assert_no_match(('foo', -1, ['bar']))

    def test_some_dict(self):
        d = {'a': 1}
        self.assert_match(d)
        self.assert_match(d, of=(str, int))

    test_some_generator = lambda self: self.assert_no_match(x for x in [1, 2])
    test_some_object = lambda self: self.assert_no_match(object())

    def assert_match(self, value, of=None):
        return super(Dict, self).assert_match(__unit__.Dict(of), value)

    def assert_no_match(self, value, of=None):
        return super(Dict, self).assert_no_match(__unit__.Dict(of), value)
