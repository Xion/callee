Numeric matchers
================

.. currentmodule:: callee.numbers

These matchers allow you to assert on specific numeric types, such as :class:`int`\ s or :class:`float`\ s
They are often combined with :doc:`operator matchers <operators>` to formulate constaints on numeric arguments of mocks:

.. code-block:: python

    from callee import Integer, GreaterThan
    mock_foo.assert_called_with(Integer() & GreaterThan(42))


Integers
********

.. autoclass:: Integer

.. autoclass:: Long

.. autoclass:: Integral


Rational numbers
****************

.. autoclass:: Fraction

.. autoclass:: Rational


Floating point numbers
**********************

.. autoclass:: Float

.. autoclass:: Real


Complex numbers
***************

.. autoclass:: Complex


All numbers
***********

.. autoclass:: Number
