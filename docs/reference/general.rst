General matchers
================

.. currentmodule:: callee.general

These matchers are the most general breed that is not specific to any
particular kind of objects. They allow you to match mock parameters
based on their Python types, object attributes, and even arbitrary
boolean predicates.

.. autoclass:: Any

.. autoclass:: Matching
.. autoclass:: ArgThat

.. autoclass:: Captor


Type matchers
*************

.. TODO: consider extracting these to a separate document to mirror the module structure
.. currentmodule:: callee.types

Use these matchers to assert on the type of objects passed to your mocks.

.. autoclass:: InstanceOf
.. autoclass:: IsA

.. autoclass:: SubclassOf
.. autoclass:: Inherits

.. autoclass:: Type

.. autoclass:: Class


Attribute matchers
******************

.. TODO: consider extracting these to a separate document to mirror the module structure
.. currentmodule:: callee.attributes

These match objects based on their Python attributes.

.. autoclass:: Attrs

.. autoclass:: HasAttrs


Function matchers
*****************

.. TODO: consider extracting these to a separate document to mirror the module structure
.. currentmodule:: callee.functions

.. autoclass:: Callable

.. autoclass:: Function

.. autoclass:: GeneratorFunction

.. autoclass:: CoroutineFunction


Object matchers
***************

.. TODO: consider extracting these to a separate document to mirror the module structure
.. currentmodule:: callee.objects

.. autoclass:: Bytes

.. autoclass:: Coroutine

.. autoclass:: FileLike
