General matchers
================

.. currentmodule:: callee.general

These matchers are the most general breed that is not specific to any
particular kind of objects. They allow you to match mock parameters
based on their Python types, object attributes, and even arbitrary
logical predicates.

.. autoclass:: Any

.. autoclass:: Matching


Type matchers
*************

Use these matchers to assert on the type of objects passed to your mocks.

.. autoclass:: InstanceOf
.. autoclass:: IsA

.. autoclass:: SubclassOf
.. autoclass:: Inherits

.. autoclass:: Type

.. autoclass:: Class


Attribute matchers
******************

These match objects based on their Python attributes.

.. autoclass:: Attrs

.. autoclass:: HasAttrs


Function matchers
*****************

.. autoclass:: Callable

.. autoclass:: Function

.. autoclass:: GeneratorFunction
