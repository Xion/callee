.. _operators

Operator matchers
=================

.. currentmodule:: callee.operators


Comparisons
***********

These matchers use Python's relational operators: `<`, `>=`, etc.

.. autoclass:: Less
.. autoclass:: LessThan
.. autoclass:: Lt

.. autoclass:: LessOrEqual
.. autoclass:: LessOrEqualTo
.. autoclass:: Le

.. autoclass:: Greater
.. autoclass:: GreaterThan
.. autoclass:: Gt

.. autoclass:: GreaterOrEqual
.. autoclass:: GreaterOrEqualTo
.. autoclass:: Ge


By length
---------

In addition to simple comparison matchers described, *callee* offers a set of dedicated matchers for asserting
on object's `len`\ gth. You can use them in conjunction with any Python :class:`Sequence`: a :class:`str`\ ing,
:class:`list`, :class:`collections.deque`, and so on.

.. autoclass:: Shorter
.. autoclass:: ShorterThan

.. autoclass:: ShorterOrEqual
.. autoclass:: ShorterOrEqualTo

.. autoclass:: Longer
.. autoclass:: LongerThan

.. autoclass:: LongerOrEqual
.. autoclass:: LongerOrEqualTo


Memberships
***********

.. autoclass:: Contains(value)

.. autoclass:: In(container)


Identity
********

.. autoclass:: Is
.. autoclass:: IsNot


Equality
********

.. note:: You will most likely never use the following matcher, but it's included for completeness.
.. autoclass:: Eq
