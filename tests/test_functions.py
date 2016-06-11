"""
Tests for function matchers.
"""
import platform
import sys

from taipan.testing import skipIf, skipUnless

from callee._compat import IS_PY3, asyncio
import callee.functions as __unit__
from tests import MatcherTestCase, python_code


IS_PY34 = sys.version_info >= (3, 4)
IS_PY35 = sys.version_info >= (3, 5)

IS_PYPY3 = IS_PY3 and platform.python_implementation() == 'PyPy'


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

    @skipIf(IS_PYPY3, "requires non-PyPy3 interpreter")
    def test_method__non_pypy3(self):
        self.assert_no_match(str.upper)
        # TODO: accept unbound methods as functions

    @skipUnless(IS_PYPY3, "requires PyPy3")
    def test_method__pypy3(self):
        self.assert_match(str.upper)

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


class Coroutine(MatcherTestCase):
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

    @skipIf(IS_PY34, "requires Python 2.x or 3.3")
    def test_generator_function__py2(self):
        def func():
            yield
        self.assert_no_match(func)
        self.assert_no_match(func())

    @skipUnless(IS_PY34, "requires Python 3.4+")
    def test_generator_function__py34(self):
        def func():
            yield
        self.assert_no_match(func)
        self.assert_match(func())

    @skipUnless(IS_PY34, "requires Python 3.4+")
    def test_coroutine__decorator(self):
        @asyncio.coroutine
        def coro_func(loop):
            pass
        coro = self.await_(coro_func)
        self.assert_match(coro)

    @skipUnless(IS_PY35, "requires Python 3.5+")
    def test_coroutine__async_def(self):
        # This whole test uses the asynchronous coroutine definition syntax
        # which is invalid on Python <3.5 so it has to be executed from string.
        try:
            exec(python_code("""
                async def coro_func():
                    pass
                coro = coro_func()
                self.await_(coro)  # to prevent a warning
                self.assert_match(coro)
            """))
        except SyntaxError:
            pass

    @skipUnless(IS_PY34, "requires Python 3.4+")
    def test_coroutine_function__decorator(self):
        @asyncio.coroutine
        def coro_func(loop):
            pass
        self.assert_no_match(coro_func)

    @skipUnless(IS_PY35, "requires Python 3.5+")
    def test_coroutine_function__async_def(self):
        # This whole test uses the asynchronous coroutine definition syntax
        # which is invalid on Python <3.5 so it has to be executed from string.
        try:
            exec(python_code("""
                async def coro_func():
                    pass
                self.assert_no_match(coro_func)
            """))
        except SyntaxError:
            pass

    # Assertion functions

    def assert_match(self, value):
        return super(Coroutine, self) \
            .assert_match(__unit__.Coroutine(), value)

    def assert_no_match(self, value):
        return super(Coroutine, self) \
            .assert_no_match(__unit__.Coroutine(), value)


class CoroutineFunction(MatcherTestCase):
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
        self.assert_no_match(func)
        self.assert_no_match(func())

    @skipUnless(IS_PY34, "requires Python 3.4+")
    def test_coroutine__decorator(self):
        @asyncio.coroutine
        def coro_func(loop):
            pass
        coro = self.await_(coro_func)
        self.assert_no_match(coro)

    @skipUnless(IS_PY35, "requires Python 3.5+")
    def test_coroutine__async_def(self):
        # This whole test uses the asynchronous coroutine definition syntax
        # which is invalid on Python <3.5 so it has to be executed from string.
        try:
            exec(python_code("""
                async def coro_func():
                    pass
                coro = coro_func()
                self.await_(coro)  # to prevent a warning
                self.assert_no_match(coro)
            """))
        except SyntaxError:
            pass

    @skipUnless(IS_PY34, "requires Python 3.4+")
    def test_coroutine_function__decorator(self):
        @asyncio.coroutine
        def coro_func(loop):
            pass
        self.assert_match(coro_func)

    @skipUnless(IS_PY35, "requires Python 3.5+")
    def test_coroutine_function__async_def(self):
        # This whole test uses the asynchronous coroutine definition syntax
        # which is invalid on Python <3.5 so it has to be executed from string.
        try:
            exec(python_code("""
                async def coro_func():
                    pass
                self.assert_match(coro_func)
            """))
        except SyntaxError:
            pass

    # Assertion functions

    def assert_match(self, value):
        return super(CoroutineFunction, self) \
            .assert_match(__unit__.CoroutineFunction(), value)

    def assert_no_match(self, value):
        return super(CoroutineFunction, self) \
            .assert_no_match(__unit__.CoroutineFunction(), value)
