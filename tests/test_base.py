# flake8: noqa
"""
Tests for matcher base classes.
"""
import callee.base as __unit__
from tests import TestCase


class BaseMatcherMetaclassTest(TestCase):
    """Tests for the BaseMatcherMetaclass."""

    def test_validate_class_definition(self):
        """Test for BaseMatcherMetaclass._validate_class_definition."""
        vcd = __unit__.BaseMatcherMetaclass._validate_class_definition

        bases = (object,)
        method = lambda self: None

        vcd('BaseMatcher', bases, __unit__.BaseMatcher.__dict__)
        vcd('Foo', bases, {})  # OK, empty definition
        vcd('Foo', bases, {'foo': 42})  # OK, no methods at all
        vcd('Foo', bases, {'__foo__': 42})  # OK, magic name but not method
        vcd('Foo', bases, {'__foo__': method})  # OK, not BaseMatcher's method
        vcd('Foo', bases, {'__init__': method})  # OK, explicitly allowed
        with self.assertRaises(RuntimeError):
            vcd('Foo', bases, {'__eq__': method})  # trying to mess up!

    def test_is_base_matcher_class_definition(self):
        """Test for BaseMatcherMetaclass._is_base_matcher_class_definition."""
        is_bmcd = \
            __unit__.BaseMatcherMetaclass._is_base_matcher_class_definition

        self.assertFalse(is_bmcd('Foo', {}))
        self.assertFalse(is_bmcd('BaseMatcher', {}))  # needs members
        self.assertFalse(is_bmcd('BaseMatcher', {'foo': 1}))  # needs methods
        self.assertFalse(  # needs methods from same module
            is_bmcd('BaseMatcher', {'foo': lambda self: None}))

        self.assertTrue(is_bmcd('BaseMatcher', __unit__.BaseMatcher.__dict__))

    def test_list_magic_methods(self):
        """Test for BaseMatcherMetaclass._list_magic_methods."""
        lmm = __unit__.BaseMatcherMetaclass._list_magic_methods

        class Foo(object):
            pass
        self.assertItemsEqual([], lmm(Foo))

        class Bar(object):
            def method(self):
                pass
        self.assertItemsEqual([], lmm(Bar))

        class Baz(object):
            def __init__(self):
                pass
            def __rdiv__(self, other):
                return self
        self.assertItemsEqual(['init', 'rdiv'], lmm(Baz))


class Matcher(TestCase):
    """Tests for the Matcher base class."""

    def test_match(self):
        """Test default match() is left to be implemented by subclasses."""
        class Custom(__unit__.Matcher):
            pass
        matcher = Custom()
        with self.assertRaises(NotImplementedError):
            matcher.match(None)

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
