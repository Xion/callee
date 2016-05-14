"""
Tests that touch more than a single module.
"""
from tests import TestCase


class Init(TestCase):
    """Tests for the __init__ module."""

    def test_all(self):
        """Tests that __all__ has only names that are actually exported."""
        import callee

        missing = set(n for n in callee.__all__
                      if getattr(callee, n, None) is None)
        self.assertEmpty(
            missing, msg="callee.__all__ contains unresolved names: %s" % (
                ", ".join(missing),))
