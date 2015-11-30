Creating custom matchers
========================

The wide assortment of predefined matchers should be sufficient for a vast majority of your use cases.

But when they're not, don't worry. *callee* enables you to create your own, custom matchers quickly and succinctly.
Those new matchers will be as capable as the standard ones, too, meaning you can use them in
:ref:`logical expressions <logical-expressions>`, or with collection matchers such as :class:`~callee.collections.List`.

Here you can learn about all the possible ways of creating matchers with custom logic.


Predicates
**********

.. currentmodule:: callee.general

The simplest technique is based on (re)using a *predicate* -- that is, a function that returns a boolean result
(``True`` or ``False``). This is handy when you already have a piece of code that recognizes objects you want to match.

Suppose this is it:

.. code-block:: python

    def is_even(x):
        return x % 2 == 0

In order to turn this function into a matcher, you just need to wrap in a :class:`Matching` object:

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

API
---

.. autoclass:: Matching
.. autoclass:: ArgThat


Custom ``Matcher`` classes
**************************

Ad-hoc matchers created with :class:`Matching`/:class:`ArgThat` are handy for some quick checks, but they have
certain limitations:

    * They cannot accept parameters to modify their behavior (unless you parametrize the callable itself,
      which is clever but somewhat tricky and therefore not recommended).
    * The error messages they produce are not very informative, which makes it harder to debug and fix tests
      which use them.

...
