"""
Test package.
"""
try:
    import unittest.mock as mock
except ImportError:
    import mock

from taipan.testing import TestCase


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
