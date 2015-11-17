String matchers
===============

.. currentmodule:: callee.strings

The :class:`String` matcher is the one you'd be using most of the time to match string arguments.

More specialized matchers can distinguish between native Python 2/3 types for strings and binary data.

.. autoclass:: String

.. autoclass:: Unicode

.. autoclass:: Bytes


Patterns
********

These matchers check whether the string is of certain form.

Matching may be done based on prefix, suffix, or one of the various ways of specifying strings patterns,
such as regular expressions.

.. autoclass:: StartsWith

.. autoclass:: EndsWith

.. autoclass:: Glob

.. autoclass:: Regex
