"""
Base classes for argument matcher.
"""


__all__ = [
    'BaseMatcher',
    'Eq', 'Is',
    'Not', 'And', 'Or',
]


class BaseMatcher(object):
    """Base class for all argument matchers.

    This class shouldn't be used directly by the client.
    To create custom matchers, inherit from :class:`Matcher` instead.
    """
    def match(self, value):
        raise NotImplementedError("matching not implemented")

    def __repr__(self):
        return "<unspecified matcher>"

    # TODO(xion): prevent the methods below from being overridden via metaclass

    def __eq__(self, other):
        if isinstance(other, BaseMatcher):
            raise TypeError(
                "incorrect use of matcher object as a value to match on")
        return self.match(other)

    def __invert__(self):
        return Not(self)

    def __and__(self, other):
        matchers = other._matchers if isinstance(other, And) else [other]
        return And(self, *matchers)

    def __or__(self, other):
        matchers = other._matchers if isinstance(other, Or) else [other]
        return Or(self, *matchers)


# TODO(xion): add the Matcher class as an allowed base class for custom,
# user-written matchers


# Special cases around equality/identity

class Eq(BaseMatcher):
    """Matches given value exactly using the equality operator."""

    # TODO(xion): document the potential rare use of this class, which
    # is asserting on mock calls that pass matcher objects in *production* code

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other

    def __repr__(self):
        return "<Eq %r>" % (self.value,)


class Is(BaseMatcher):
    """Matches given value using the identity (``is``) operator."""

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value is other

    def __repr__(self):
        return "<Is %r>" % (self.value,)


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
        return "not %r" % (self.matcher,)

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

    def match(self, value):
        return all(matcher.match(value) for matcher in self._matchers)

    def __repr__(self, value):
        return "<%s>" % " and ".join(map(repr, self.matchers))


class Or(BaseMatcher):
    """Matches the argument only if at least one given matcher does."""

    def __init__(self, *matchers):
        assert matchers, "Or() expects at least one matcher"
        assert any(isinstance(m, BaseMatcher)
                   for m in matchers), "Or() expects matchers"
        self._matchers = list(matchers)

    def match(self, value):
        return any(matcher.match(value) for matcher in self._matchers)

    def __repr__(self, value):
        return "<%s>" % " or ".join(map(repr, self.matchers))
