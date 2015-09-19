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
