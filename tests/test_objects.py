"""
Tests for object matchers.
"""
import io
try:
    from StringIO import StringIO
except ImportError:
    StringIO = io.StringIO

from taipan.testing import skipIf, skipUnless

from callee._compat import IS_PY3, asyncio
import callee.objects as __unit__
from tests import IS_PY34, IS_PY35, MatcherTestCase, python_code


class Bytes(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_empty_unicode = lambda self: self.assert_no_match(u'')
    test_some_unicode = lambda self: self.assert_no_match(u"Alice has a cat")

    @skipIf(IS_PY3, "requires Python 2.x")
    def test_some_string__py2(self):
        self.assert_match("Alice has a cat")

    @skipUnless(IS_PY3, "requires Python 3.x")
    def test_some_string__py3(self):
        self.assert_no_match("Alice has a cat")

    test_some_object = lambda self: self.assert_no_match(object())
    test_some_number = lambda self: self.assert_no_match(42)

    def assert_match(self, value):
        return super(Bytes, self).assert_match(__unit__.Bytes(), value)

    def assert_no_match(self, value):
        return super(Bytes, self).assert_no_match(__unit__.Bytes(), value)


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


class FileLike(MatcherTestCase):
    test_none = lambda self: self.assert_no_match(None)
    test_zero = lambda self: self.assert_no_match(0)
    test_string = lambda self: self.assert_no_match("Alice has a cat")
    test_some_object = lambda self: self.assert_no_match(object())

    def test_openfile__read(self):
        with open(__file__, 'r') as f:
            self.assert_match(f, read=True)

    def test_openfile__write(self):
        with open(__file__, 'a') as f:
            self.assert_match(f, write=True)

    def test_openfile__both(self):
        with open(__file__, 'r+') as f:
            self.assert_match(f, read=True, write=True)

    def test_io_open__read(self):
        with io.open(__file__, 'r') as f:
            self.assert_match(f, read=True)

    def test_io_open__write(self):
        with io.open(__file__, 'a') as f:
            self.assert_match(f, write=True)

    def test_io_open__both(self):
        with io.open(__file__, 'r+') as f:
            self.assert_match(f, read=True, write=True)

    def test_stringio(self):
        self.assert_match(StringIO(), read=True, write=True)

    def test_ctor(self):
        with self.assertRaises(ValueError):
            __unit__.FileLike(read=None, write=None)

    def test_repr(self):
        self.assertEquals("<FileLike (read)>",
                          repr(__unit__.FileLike(read=True, write=None)))
        self.assertEquals("<FileLike (read,write)>",
                          repr(__unit__.FileLike(read=True, write=True)))
        self.assertEquals("<FileLike (noread)>",
                          repr(__unit__.FileLike(read=False, write=None)))
        self.assertEquals("<FileLike (noread,nowrite)>",
                          repr(__unit__.FileLike(read=False, write=False)))

    # Assertion functions

    def assert_match(self, value, *args, **kwargs):
        return super(FileLike, self) \
            .assert_match(__unit__.FileLike(*args, **kwargs), value)

    def assert_no_match(self, value, *args, **kwargs):
        return super(FileLike, self) \
            .assert_no_match(__unit__.FileLike(*args, **kwargs), value)
