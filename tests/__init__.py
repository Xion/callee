"""
Test package.
"""
try:
    import unittest.mock as mock
except ImportError:
    import mock

from taipan.testing import TestCase as _TestCase


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
