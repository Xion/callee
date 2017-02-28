"""
General matchers.

These don't belong to any broader category, and include matchers for common
Python objects, like functions or classes.
"""
import inspect

from callee._compat import IS_PY3, STRING_TYPES
from callee.base import BaseMatcher


__all__ = [
    'Any', 'Matching', 'ArgThat', 'Captor',
]


# TODO: introduce custom exception types rather than using built-ins

# TODO: matchers for positional & keyword arguments,
# e.g. *Args(Integer(), min=1, max=10), **Kwargs(foo=String(), bar=Float())


class Any(BaseMatcher):
    """Matches any object."""

    def match(self, value):
        return True

    def __repr__(self):
        return "<Any>"


class Matching(BaseMatcher):
    """Matches an object that satisfies given predicate."""

    MAX_DESC_LENGTH = 32

    def __init__(self, predicate, desc=None):
        """
        :param predicate: Callable taking a single argument
                          and returning True or False
        :param desc: Optional description of the predicate.
                     This will be displayed as a part of the error message
                     on failed assertion.
        """
        if not callable(predicate):
            raise TypeError(
                "Matching requires a predicate, got %r" % (predicate,))

        self.predicate = predicate
        self.desc = self._validate_desc(desc)

    def _validate_desc(self, desc):
        """Validate the predicate description."""
        if desc is None:
            return desc

        if not isinstance(desc, STRING_TYPES):
            raise TypeError(
                "predicate description for Matching must be a string, "
                "got %r" % (type(desc),))

        # Python 2 mandates __repr__ to be an ASCII string,
        # so if Unicode is passed (usually due to unicode_literals),
        # it should be ASCII-encodable.
        if not IS_PY3 and isinstance(desc, unicode):
            try:
                desc = desc.encode('ascii', errors='strict')
            except UnicodeEncodeError:
                raise TypeError("predicate description must be "
                                "an ASCII string in Python 2")

        return desc

    def match(self, value):
        # Note that any possible exceptions from ``predicate``
        # are intentionally let through, to make it easier to diagnose errors
        # than a plain "no match" response would.
        return bool(self.predicate(value))
        # TODO: translate exceptions from the predicate into our own
        # exception type to not clutter user-visible stracktraces with our code

    def __repr__(self):
        """Return a representation of the matcher."""
        name = getattr(self.predicate, '__name__', None)
        desc = self.desc

        # When no user-provided description is available,
        # use function's own name or even its repr().
        if desc is None:
            # If not a lambda function, we can probably make the representation
            # more readable by showing just the function's own name.
            if name and name != '<lambda>':
                # Where possible, make it a fully qualified name, including
                # the module path. This is either on Python 3.3+
                # (via __qualname__), or when the predicate is
                # a standalone function (not a method).
                qualname = getattr(self.predicate, '__qualname__', name)
                is_method = inspect.ismethod(self.predicate) or \
                    isinstance(self.predicate, staticmethod)
                if qualname != name or not is_method:
                    # Note that this shows inner functions (those defined
                    # locally inside other functions) as if they were global
                    # to the module.
                    # This is why we use colon (:) as separator here, as to not
                    # suggest this is an evaluatable identifier.
                    name = '%s:%s' % (self.predicate.__module__, qualname)
            else:
                # For lambdas and other callable objects,
                # we'll just default to the Python repr().
                name = None
        else:
            # Quote and possibly ellipsize the provided description.
            if len(desc) > self.MAX_DESC_LENGTH:
                ellipsis = '...'
                desc = desc[:self.MAX_DESC_LENGTH - len(ellipsis)] + ellipsis
            desc = '"%s"' % desc

        return "<Matching %s>" % (desc or name or repr(self.predicate))

ArgThat = Matching


class Captor(BaseMatcher):
    """Argument captor.

    You can use :class:`Captor` to "capture" the original argument
    that the mock was called with, and perform custom assertions on it.

    Example::

        captor = Captor()
        mock_foo.assert_called_with(captor)

        # captured value is available as the `arg` attribute
        self.assertEquals(captor.arg.some_method(), 42)
        self.assertEquals(captor.arg.some_other_method(), "foo")

    .. versionadded:: 0.2
    """
    __slots__ = ('matcher', 'value')

    def __init__(self, matcher=None):
        """
        :param matcher: Optional matcher to validate the argument against
                        before it's captured
        """
        if matcher is None:
            matcher = Any()

        if not isinstance(matcher, BaseMatcher):
            raise TypeError("expected a matcher, got %r" % (type(matcher),))
        if isinstance(matcher, Captor):
            raise TypeError("cannot pass a captor to another captor")

        self.matcher = matcher

    def has_value(self):
        """Returns whether the :class:`Captor` has captured a value."""
        return hasattr(self, 'value')

    @property
    def arg(self):
        """The captured argument value."""
        if not self.has_value():
            raise ValueError("no value captured")
        return self.value

    def match(self, value):
        if self.has_value():
            raise ValueError("a value has already been captured")

        if not self.matcher.match(value):
            return False
        self.value = value
        return True

    def __repr__(self):
        """Return a representation of the captor."""
        return "<Captor %r%s>" % (self.matcher,
                                  " (*)" if self.has_value() else "")
