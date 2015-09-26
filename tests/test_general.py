"""
Tests for general matchers.
"""
import callee.general as __unit__
from tests import MatcherTestCase


class Any(MatcherTestCase):
    test_none = lambda self: self.assert_match(None)
    test_zero = lambda self: self.assert_match(0)
    test_empty_string = lambda self: self.assert_match('')
    test_empty_list = lambda self: self.assert_match([])
    test_empty_tuple = lambda self: self.assert_match(())
    test_some_object = lambda self: self.assert_match(object())
    test_some_string = lambda self: self.assert_match("Alice has a cat")
    test_some_number = lambda self: self.assert_match(42)
    test_some_list = lambda self: self.assert_match([1, 2, 3, 5, 8, 13])
    test_some_tuple = lambda self: self.assert_match(('foo', -1, ['bar']))

    def assert_match(self, value):
        return super(Any, self).assert_match(__unit__.Any(), value)


class Matching(MatcherTestCase):
    EVEN = staticmethod(lambda x: x % 2 == 0)
    ODD = staticmethod(lambda x: x % 2 != 0)

    SHORTER_THAN_THREE = staticmethod(lambda x: len(x) < 3)
    LONGER_THAN_THREE = staticmethod(lambda x: len(x) > 3)

    def test_invalid_predicate(self):
        with self.assertRaises(TypeError):
            __unit__.Matching(object())

    def test_none(self):
        self.assert_no_match(None, self.EVEN)
        self.assert_no_match(None, self.ODD)

    def test_zero(self):
        self.assert_match(0, self.EVEN)
        self.assert_no_match(0, self.ODD)

    def test_empty_string(self):
        self.assert_match('', self.SHORTER_THAN_THREE)
        self.assert_no_match('', self.LONGER_THAN_THREE)

    def test_empty_list(self):
        self.assert_match([], self.SHORTER_THAN_THREE)
        self.assert_no_match([], self.LONGER_THAN_THREE)

    def test_empty_tuple(self):
        self.assert_match((), self.SHORTER_THAN_THREE)
        self.assert_no_match((), self.LONGER_THAN_THREE)

    def test_some_string(self):
        s = "Alice has a cat"
        self.assert_no_match(s, self.SHORTER_THAN_THREE)
        self.assert_match(s, self.LONGER_THAN_THREE)

    # Assertion functions

    def assert_match(self, value, predicate):
        return super(Matching, self) \
            .assert_match(__unit__.Matching(predicate), value)

    def assert_no_match(self, value, predicate):
        return super(Matching, self) \
            .assert_no_match(__unit__.Matching(predicate), value)


# Function-related matchers

class Callable(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_zero = lambda self: self.assert_no_match(0)
    test_string = lambda self: self.assert_no_match("Alice has a cat")
    test_some_object = lambda self: self.assert_no_match(object())

    def test_function(self):
        def func():
            pass
        self.assert_match(func)

    test_method = lambda self: self.assert_match(str.upper)
    test_type = lambda self: self.assert_match(object)

    def test_callable_object(self):
        class Foo(object):
            def __call__(self):
                pass
        self.assert_match(Foo())

    def test_generator_function(self):
        def func():
            yield
        self.assert_match(func)
        self.assert_no_match(func())

    test_lambda = lambda self: self.assert_match(lambda: ())
    test_generator = lambda self: self.assert_no_match(x for x in ())

    def assert_match(self, value):
        return super(Callable, self).assert_match(__unit__.Callable(), value)

    def assert_no_match(self, value):
        return super(Callable, self) \
            .assert_no_match(__unit__.Callable(), value)


class Function(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_zero = lambda self: self.assert_no_match(0)
    test_string = lambda self: self.assert_no_match("Alice has a cat")
    test_some_object = lambda self: self.assert_no_match(object())

    def test_function(self):
        def func():
            pass
        self.assert_match(func)

    test_method = lambda self: self.assert_no_match(str.upper)
    test_type = lambda self: self.assert_no_match(object)

    def test_callable_object(self):
        class Foo(object):
            def __call__(self):
                pass
        self.assert_no_match(Foo())

    def test_generator_function(self):
        def func():
            yield
        self.assert_match(func)
        self.assert_no_match(func())

    test_lambda = lambda self: self.assert_match(lambda: ())
    test_generator = lambda self: self.assert_no_match(x for x in ())

    def assert_match(self, value):
        return super(Function, self).assert_match(__unit__.Function(), value)

    def assert_no_match(self, value):
        return super(Function, self) \
            .assert_no_match(__unit__.Function(), value)


class GeneratorFunction(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_zero = lambda self: self.assert_no_match(0)
    test_string = lambda self: self.assert_no_match("Alice has a cat")
    test_some_object = lambda self: self.assert_no_match(object())

    def test_function(self):
        def func():
            pass
        self.assert_no_match(func)

    test_method = lambda self: self.assert_no_match(str.upper)
    test_type = lambda self: self.assert_no_match(object)

    def test_callable_object(self):
        class Foo(object):
            def __call__(self):
                pass
        self.assert_no_match(Foo())

    def test_generator_function(self):
        def func():
            yield
        self.assert_match(func)
        self.assert_no_match(func())

    test_lambda = lambda self: self.assert_no_match(lambda: ())
    test_generator = lambda self: self.assert_no_match(x for x in ())

    def assert_match(self, value):
        return super(GeneratorFunction, self) \
            .assert_match(__unit__.GeneratorFunction(), value)

    def assert_no_match(self, value):
        return super(GeneratorFunction, self) \
            .assert_no_match(__unit__.GeneratorFunction(), value)


# Type-related matchers

class InstanceOf(MatcherTestCase):

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            __unit__.InstanceOf(object())

    def test_none(self):
        self.assert_match(None, object)
        self.assert_no_match(None, self.Class)

    def test_zero(self):
        self.assert_match(0, int)
        self.assert_no_match(0, self.Class)

    def test_string(self):
        s = "Alice has a cat"
        self.assert_match(s, str)
        self.assert_no_match(s, self.Class)

    def test_class(self):
        self.assert_match(self.Class(), self.Class)
        self.assert_no_match(self.Class(), int)

    def test_meta(self):
        self.assert_match(self.Class, type)
        self.assert_match(type, type)

    # Utility code

    class Class(object):
        pass

    def assert_match(self, value, type_):
        return super(InstanceOf, self) \
            .assert_match(__unit__.InstanceOf(type_), value)

    def assert_no_match(self, value, type_):
        return super(InstanceOf, self) \
            .assert_no_match(__unit__.InstanceOf(type_), value)


class SubclassOf(MatcherTestCase):

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            __unit__.SubclassOf(object())

    def test_non_types(self):
        self.assert_no_match(None, object)
        self.assert_no_match(0, object)
        self.assert_no_match("Alice has a cat", object)
        self.assert_no_match((), object)
        self.assert_no_match([], object)

    def test_types(self):
        self.assert_match(self.Class, object)
        self.assert_match(self.Class, self.Class)
        self.assert_match(self.Class, object)
        self.assert_match(object, object)

    # Utility code

    class Class(object):
        pass

    def assert_match(self, value, type_):
        return super(SubclassOf, self) \
            .assert_match(__unit__.SubclassOf(type_), value)

    def assert_no_match(self, value, type_):
        return super(SubclassOf, self) \
            .assert_no_match(__unit__.SubclassOf(type_), value)
