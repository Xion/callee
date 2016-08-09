Collection matchers
===================

.. currentmodule:: callee.collections

Besides allowing you to assert about various collection types (lists, sets, etc.),
these matchers can also verify the *elements* inside those collections.

This way, you can express even complex conditions in a concise and readable manner.
Here's a couple of examples:

.. code-block:: python

    # list of ints
    List(Integer())
    List(of=Integer())
    List(int)  # types are also accepted as item matchers

    # list of strings starting with 'http://'
    List(of=String() & StartsWith('http://'))

    # dictionary mapping strings to strings
    Dict(String(), String())

    # dict with string keys (no restriction on values)
    Dict(keys=String())

    # list of dicts mapping strings to some custom type
    List(Dict(String(), Foo))


Abstract collection types
*************************

These mostly correspond to the `abstract base classes`_ defined in the standard |collections module|_.

.. _abstract base classes: https://docs.python.org/library/collections.html#collections-abstract-base-classes

.. |collections module| replace:: :mod:`collections` module
.. _collections module: https://docs.python.org/library/collections.html

.. autoclass:: Iterable

.. autoclass:: Generator

.. autoclass:: Sequence

.. autoclass:: Mapping


Concrete collections
********************

These match the particular Python built-in collections types, like :class:`list` or :class:`dict`.

.. autoclass:: List

.. autoclass:: Set

.. autoclass:: Dict

.. autoclass:: OrderedDict
