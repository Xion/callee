Creating custom matchers
========================

The wide assortment of predefined matchers should be sufficient for a vast majority of your use cases.

But when they're not, don't worry. *callee* enables you to create your own, custom matchers quickly and succinctly.
Those new matchers will be as capable as the standard ones, too, meaning you can use them in
:ref:`logical expressions <logical-expressions>`, or with collection matchers such as :class:`~callee.collections.List`.

Here you can learn about all the possible ways of creating matchers with custom logic.


Predicates
**********

The simplest technique is based on (re)using a *predicate* -- that is, a function that returns a boolean result
(``True`` or ``False``). This is handy when you already have a piece of code that recognizes objects you want to match.

Suppose you have this function:

.. code-block:: python

    def is_even(x):
        return x % 2 == 0

In order to turn it into an ad-hoc matcher, all need to do is wrap it in a :class:`Matching` object:

.. code-block:: python

    mock_compute_half.assert_called_with(Matching(is_even))

:class:`Matching` (also aliased as :class:`ArgThat`) accepts any callable that takes a single argument -- the object to
match -- and interprets its result as a boolean value.

As you may expect, returning ``True`` (or any Python "truthy" object) means that given argument matches the criteria.
Otherwise, the match is considered unsuccessful.
(If the function raises an exception, this is also interpreted as a failed match).

Since it's valid to pass any Python callable to :class:`Matching`/:class:`ArgThat`, you can do basically anything there:

.. code-block:: python

    Matching(lambda x: x % 2 == 0)  # like above
    ArgThat(is_prime)  # defined elsewhere
    Matching(bool)  # matches any "truthy" value

For clearer code, however, you should strive to keep the predicates short and simple. Rather than writing a complicated
``lambda`` expression, for example, try to break it down and combine :class:`Matching`/:class:`ArgThat` with the built-in
matchers.

If that proves difficult, it's probably time to consider a custom matcher **class** instead.


Matcher classes
***************

Ad-hoc matchers created with :class:`Matching`/:class:`ArgThat` are handy for some quick checks, but they have
certain limitations:

    * They cannot accept parameters that modify their behavior (unless you parametrize the callable itself,
      which is clever but somewhat tricky and therefore not recommended).
    * The error messages they produce are not very informative, which makes it harder to debug and fix tests
      that use them.

These constraints are outgrown quickly when you use the same ad-hoc matcher more than once or twice.

Subclassing ``Matcher``
-----------------------

The canonical way of creating a custom matcher type is to inherit from the :class:`~callee.base.Matcher` base class.

The only method you need to override there is ``match``. It shall take a single argument -- the ``value`` to test --
and return a boolean result:

.. code-block:: python

    class Even(Matcher):
        def match(self, value):
            return value % 2 == 0

The new matcher is immediately usable in assertions:

.. code-block:: python

    mock_compute_half.assert_called_with(Even())

or in any other context you'd normally use a matcher in.

Parametrized matchers
---------------------

Because matchers deriving from the :class:`Matcher` class are normal Python objects, their construction
can be parametrized to provide additional flexibility.

The easiest and most common way is simply to save the arguments of ``__init__`` as attributes on the object,
so that the ``match`` method can access them as needed:

.. code-block:: python

    class Divisible(Matcher):
        """Matches a value that has given divisor."""

        def __init__(self, by):
            self.divisor = by

        def match(self, value):
            return value % self.divisor == 0

Usage of such a matcher is rather straightforward:

.. code-block:: python

    mock_compute_half.assert_called_with(Divisible(by=2))

Overriding ``__repr__``
-----------------------

Custom matchers written as classes have one more advantage over ad-hoc ones. It is possible to redefine their
``__repr__`` method, allowing for more informative error messages on failed assertions.

As an example, it would be good if ``Divisible`` matcher the from previous section told us what number it expected
for the argument to be divisible by. This is easy enough to add:

.. code-block:: python

        def __repr__(self):
            return "<divisible by %d>" % (self.divisor,)

and makes relevant ``AssertionError``\ s more readable:

.. code-block:: python

    >>> mock_compute_half(3)
    >>> mock_compute_half.assert_called_with(Divisible(by=2))
    ...
    AssertionError: Expected call: mock(<divisible by 2>)
    Actual call: mock(3)

In general, all parametrized matchers should probably override ``__repr__`` to show, at a glance, what parameters
they were instantiated with.

.. note::

    The convention to surround matcher representations in angle brackets (``<...>``) is followed by
    all built-in matchers in *callee*, because it makes it easier to tell them apart from literal values.
    Adopting it for your own matches is therefore recommended.


Best practices
**************

Ad-hoc matchers (those created with :class:`Matching`/:class:`ArgThat`) are best used judiciously. Ideally,
you would want to involve them only if:

    * you already have a predicate you can use, or you can define one easily as a ``lambda``
    * your test is very short, so that it's easy to debug when it breaks

As a rule of thumb, whenever you define a function solely to use it with :class:`Matching`/:class:`ArgThat`,
you should strongly consider creating a :class:`Matcher` subclass instead.
There is almost no additional boilerplate involved, and the resulting matcher will be more reusable and easier to extend.

Plus, if the new matcher turns up to be useful in multiple tests or projects, it can be added to *callee* itself!
