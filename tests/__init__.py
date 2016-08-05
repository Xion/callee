"""
Test package.
"""
import os
import sys

try:
    import unittest.mock as mock
except ImportError:
    import mock

from taipan.testing import TestCase as _TestCase

from callee._compat import asyncio


__all__ = [
    'IS_PY34', 'IS_PY35',
    'MatcherTestCase',
    'python_code'
]


IS_PY34 = sys.version_info >= (3, 4)
IS_PY35 = sys.version_info >= (3, 5)


class TestCase(_TestCase):
    """Base class for all test cases."""

    def setUp(self):
        super(TestCase, self).setUpClass()

        # display full diffs when equality assertions fail under py.test
        self.maxDiff = None


class MatcherTestCase(TestCase):
    """Base class for matcher test cases."""

    def assert_match(self, matcher, value):
        m = mock.Mock()
        m(value)
        m.assert_called_with(matcher)
        return True

    def assert_no_match(self, matcher, value):
        m = mock.Mock()
        m(value)
        with self.assertRaises(AssertionError):
            m.assert_called_with(matcher)
        return True

    def await_(self, coroutine):
        """Run given asynchronous coroutine to completion.
        This prevents a warning from being emitted when it goes out of scope.

        :param coroutine: A coroutine or a coroutine function
        """
        self.assertIsNotNone(
            asyncio,
            msg="Tried to use asyncio on unsupported Python version")

        loop = asyncio.new_event_loop()
        if asyncio.iscoroutinefunction(coroutine):
            coroutine = coroutine(loop)
        loop.run_until_complete(coroutine)
        loop.close()

        return coroutine


# Utility functions

def python_code(source):
    """Format Python source code, given as a string, for use with ``exec``.

    Use it like so::

        exec(python_code('''
            async def foo():
                pass
        '''))

    This allows to use newer syntactic constructs that'd cause SyntaxError
    on older Python versions.
    """
    # (Whitespace shenanigans adapted from sphinx.utils.prepare_docstring)

    # remove excess whitespace from source code lines which will be there
    # if the code was given as indented, multiline string
    lines = source.expandtabs().splitlines()
    margin = sys.maxsize
    for line in lines:
        code_len = len(line.strip())
        if code_len > 0:
            indent = len(line) - code_len
            margin = min(margin, indent)
    if margin < sys.maxsize:
        for i in range(len(lines)):
            lines[i] = lines[i][margin:]

    # ensure there is an empty line at the end
    if lines and lines[-1]:
        lines.append('')

    return os.linesep.join(lines)
