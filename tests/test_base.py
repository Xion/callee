"""
Tests for matcher base classes.
"""
import callee.base as __unit__
from tests import TestCase


class Matcher(TestCase):
    """Tests for the Matcher base class."""

    def test_repr__no_ctor(self):
        """Test default __repr__ of Matcher subclass without a constructor."""
        class Custom(__unit__.Matcher):
            pass
        self.assertEquals("<Custom>", "%r" % Custom())

    def test_repr__argless_ctor__no_state(self):
        """Test default __repr__ of Matcher subclass with argless ctor."""
        class Custom(__unit__.Matcher):
            def __init__(self):
                pass
        self.assertEquals("<Custom>", "%r" % Custom())

    def test_repr__argless_ctor__with_state(self):
        """Test __repr__ of Matcher subclass with argless ctor & state."""
        class Custom(__unit__.Matcher):
            def __init__(self):
                self.foo = 42
        self.assertEquals("<Custom>", "%r" % Custom())

    def test_repr__argful_ctor__no_state(self):
        """Test __repr__ with argful constructor but no actual fields."""
        class Custom(__unit__.Matcher):
            def __init__(self, unused):
                pass
        self.assertEquals("<Custom(...)>", "%r" % Custom('unused'))

    def test_repr__argful_ctor__with_state(self):
        """Test __repr__ with argful constructor & object fields."""
        class Custom(__unit__.Matcher):
            def __init__(self, foo):
                self.foo = foo

        foo = 'bar'
        self.assertEquals("<Custom(foo=%r)>" % (foo,),
                          "%r" % Custom(foo='bar'))
