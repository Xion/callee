"""
Base classes for argument matchers.
"""
import inspect
from operator import itemgetter

from callee._compat import IS_PY3, metaclass


__all__ = [
    'Matcher',
    'Eq', 'Is', 'IsNot',
    'Not', 'And', 'Or', 'Either', 'OneOf', 'Xor',
]


class BaseMatcherMetaclass(type):
    """Metaclass for :class:`BaseMatcher`."""

    #: What __magic__ methods of :class:`BaseMatcher`
    #: can be overriden by user-defined subclasses.
    #:
    #: Any method not on this list can only be overridden by classes defined
    #: within this module. This prevents users from accidentally interfering
    #: with fundamental matcher functionality while writing their own matchers.
    #
    #: The names are given without the leading or trailing underscores.
    #:
    USER_OVERRIDABLE_MAGIC_METHODS = ('init', 'repr')

    def __new__(meta, classname, bases, dict_):
        """Create a new matcher class."""
        meta._validate_class_definition(classname, bases, dict_)
        return super(BaseMatcherMetaclass, meta) \
            .__new__(meta, classname, bases, dict_)

    @classmethod
    def _validate_class_definition(meta, classname, bases, dict_):
        """Ensure the matcher class definition is acceptable.
        :raise RuntimeError: If there is a problem
        """
        # let the BaseMatcher class be created without hassle
        if meta._is_base_matcher_class_definition(classname, dict_):
            return

        # ensure that no important magic methods are being overridden
        for name, member in dict_.items():
            if not (name.startswith('__') and name.endswith('__')):
                continue

            # check if it's not a whitelisted magic method name
            name = name[2:-2]
            if not name:
                continue  # unlikely case of a ``____`` function
            if name not in meta._list_magic_methods(BaseMatcher):
                continue
            if name in meta.USER_OVERRIDABLE_MAGIC_METHODS:
                continue

            # non-function attributes, like __slots__, are harmless
            if not inspect.isfunction(member):
                continue

            # classes in this very module are exempt, since they define
            # the very behavior of matchers we want to protect
            if member.__module__ == __name__:
                continue

            raise RuntimeError(
                "matcher class %s cannot override the __%s__ method" % (
                    classname, name))

    @classmethod
    def _is_base_matcher_class_definition(meta, classname, dict_):
        """Checks whether given class name and dictionary
        define the :class:`BaseMatcher`.
        """
        if classname != 'BaseMatcher':
            return False
        methods = list(filter(inspect.isfunction, dict_.values()))
        return methods and all(m.__module__ == __name__ for m in methods)

    @classmethod
    def _list_magic_methods(meta, class_):
        """Return names of magic methods defined by a class.
        :return: Iterable of magic methods, each w/o the ``__`` prefix/suffix
        """
        return [
            name[2:-2] for name, member in class_.__dict__.items()
            if len(name) > 4 and name.startswith('__') and name.endswith('__')
            and inspect.isfunction(member)
        ]

    # TODO: consider making matcher classes interchangeable with matcher
    # objects created w/o ctor args, i.e. making Integer and Integer()
    # equivalent; it'd require this metaclass to implement the magic methods
    # from BaseMatcher and something better than `isinstance(x, BaseMatcher)`


@metaclass(BaseMatcherMetaclass)
class BaseMatcher(object):
    """Base class for all argument matchers.

    This class shouldn't be used directly by the clients.
    To create custom matchers, inherit from :class:`Matcher` instead.
    """
    __slots__ = ()

    def match(self, value):
        raise NotImplementedError("matching not implemented")

    def __repr__(self):
        return "<unspecified matcher>"

    def __eq__(self, other):
        if isinstance(other, BaseMatcher):
            raise TypeError(
                "incorrect use of matcher object as a value to match on")
        return self.match(other)

    # TODO: make matcher objects callable

    def __invert__(self):
        return Not(self)

    def __and__(self, other):
        matchers = other._matchers if isinstance(other, And) else [other]
        return And(self, *matchers)

    def __or__(self, other):
        matchers = other._matchers if isinstance(other, Or) else [other]
        return Or(self, *matchers)

    def __xor__(self, other):
        matchers = other._matchers if isinstance(other, Either) else [other]
        return Either(self, *matchers)


class Matcher(BaseMatcher):
    """Base class for custom (user-defined) argument matchers.

    To create a custom matcher, simply inherit from this class
    and implement the :meth:`match` method.

    If the matcher is more complicated (e.g. parametrized),
    you may also  want to provide a :meth:`__repr__` method implementation
    for better error messages.
    """
    def __repr__(self):
        """Provides a default ``repr``\ esentation for custom matchers.

        This representation will include matcher class name
        and the values of its public attributes.
        If that's insufficient, consider overriding this method.
        """
        args = ""

        # check if the matcher class has a parametrized constructor
        has_argful_ctor = False
        if '__init__' in self.__class__.__dict__:
            argnames, vargargs, kwargs, _ = inspect.getargspec(
                self.__class__.__init__)
            has_argful_ctor = bool(argnames[1:] or vargargs or kwargs)

        # if so, then it probably means it has some interesting state
        # in its attributes which we can include in the default representation
        if has_argful_ctor:
            # TODO: __getstate__ instead of __dict__?
            fields = [(name, value) for name, value in self.__dict__.items()
                      if not name.startswith('_')]
            if fields:
                def repr_value(value):
                    """Safely represent a value as an ASCII string."""
                    if isinstance(value, bytes):
                        value = value.decode('ascii', 'ignore')
                    if not IS_PY3 and isinstance(value, unicode):
                        value = value.encode('ascii', 'replace')
                        value = str(value)
                    return repr(value)

                fields.sort(key=itemgetter(0))
                args = "(%s)" % ", ".join(
                    "%s=%s" % (name, repr_value(value)[:32])
                    for name, value in fields)
            else:
                args = "(...)"

        return "<%s%s>" % (self.__class__.__name__, args)


# Special cases around equality/identity

class Eq(BaseMatcher):
    """Matches a value exactly using the equality (``==``) operator.

    This is already the default mode of operation for ``assert_called_with``
    methods on mocks, making this matcher redundant in most situations::

        mock_foo.assert_called_with(bar)
        mock_foo.assert_called_with(Eq(bar))  # equivalent

    In very rare and specialized cases, however, if the **tested code** treats
    `callee` matcher objects in some special way, using :class:`Eq` may be
    necessary.

    Those situations shouldn't generally arise outside of writing tests
    for code that is itself a test library or helper.
    """
    def __init__(self, value):
        """:param value: Value to match against"""
        self.value = value

    def match(self, value):
        return self.value == value

    def __eq__(self, other):
        return self.match(other)

    def __repr__(self):
        # This representation matches the format of comparison operators
        # (such as :class:`Less`) defined in the ``.operators`` module.
        return "<... == %r>" % (self.value,)


class Is(BaseMatcher):
    """Matches a value using the identity (``is``) operator."""

    def __init__(self, value):
        self.value = value

    def match(self, value):
        return value is self.value

    def __eq__(self, other):
        return self.match(other)

    def __repr__(self):
        # This representation matches the format of comparison operators
        # (such as :class:`Less`) defined in the ``.operators`` module.
        return "<... is %r>" % (self.value,)


class IsNot(BaseMatcher):
    """Matches a value using the negated identity (``is not``) operator."""

    def __init__(self, value):
        self.value = value

    def match(self, value):
        return value is not self.value

    def __eq__(self, other):
        return self.match(other)

    def __repr__(self):
        # This representation matches the format of comparison operators
        # (such as :class:`Less`) defined in the ``.operators`` module.
        return "<... is not %r>" % (self.value,)


# Logical combinators for matchers

class Not(BaseMatcher):
    """Negates given matcher.

    :param matcher: Matcher object to negate the semantics of
    """
    def __init__(self, matcher):
        assert isinstance(matcher, BaseMatcher), "Not() expects a matcher"
        self._matcher = matcher

    def match(self, value):
        return not self._matcher.match(value)

    def __repr__(self):
        return "not %r" % (self._matcher,)

    def __invert__(self):
        return self._matcher

    def __and__(self, other):
        # convert (~a) & (~b) into ~(a | b) which is one operation less
        # but still equivalent as per de Morgan laws
        if isinstance(other, Not):
            return Not(self.matcher | other.matcher)
        return super(Not, self).__and__(other)

    def __or__(self, other):
        # convert (~a) | (~b) into ~(a & b) which is one operation less
        # but still equivalent as per de Morgan laws
        if isinstance(other, Not):
            return Not(self.matcher & other.matcher)
        return super(Not, self).__or__(other)


class And(BaseMatcher):
    """Matches the argument only if all given matchers do."""

    def __init__(self, *matchers):
        assert matchers, "And() expects at least one matcher"
        assert all(isinstance(m, BaseMatcher)
                   for m in matchers), "And() expects matchers"
        self._matchers = list(matchers)

    # TODO: coalesce a & b & c into single And(a, b, c)

    def match(self, value):
        return all(matcher.match(value) for matcher in self._matchers)

    def __repr__(self):
        return "<%s>" % " and ".join(map(repr, self._matchers))


class Or(BaseMatcher):
    """Matches the argument only if at least one given matcher does."""

    def __init__(self, *matchers):
        assert matchers, "Or() expects at least one matcher"
        assert all(isinstance(m, BaseMatcher)
                   for m in matchers), "Or() expects matchers"
        self._matchers = list(matchers)

    # TODO: coalesce a | b | c into single Or(a, b, c)

    def match(self, value):
        return any(matcher.match(value) for matcher in self._matchers)

    def __repr__(self):
        return "<%s>" % " or ".join(map(repr, self._matchers))


class Either(BaseMatcher):
    """Matches the argument only if some (but not all) of given matchers do.

    .. versionadded:: 0.3
    """
    def __init__(self, *matchers):
        assert len(matchers) >= 2, "Either() expects at least two matchers"
        assert all(isinstance(m, BaseMatcher)
                   for m in matchers), "Either() expects matchers"
        self._matchers = list(matchers)

    def match(self, value):
        any_matches = bool(self._matchers[0].match(value))
        for matcher in self._matchers[1:]:
            is_match = bool(matcher.match(value))
            if is_match != any_matches:
                return True
            any_matches |= is_match
        return False

    def __repr__(self):
        return "<%s>" % " xor ".join(map(repr, self._matchers))

#: Alias for :class:`Either`.
OneOf = Either
#: Alias for :class:`Either`.
Xor = Either
