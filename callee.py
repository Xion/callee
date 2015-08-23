"""
callee
"""
__version__ = "0.0.1"
__description__ = "Argument matcher for unittest.mock"
__author__ = "Karol Kuczmarski"
__license__ = "Simplified BSD"


__all__ = ['Any']


class Matcher(object):
    """Base class for argument matchers."""

    def __eq__(self, other):
        raise NotImplementedError("matching not implemented")


class Any(object):
    """Matches any object."""

    def __eq__(self, other):
        return True
