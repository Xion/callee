.. callee documentation master file, created by
   sphinx-quickstart on Wed Oct 14 11:24:04 2015.

callee
======

*callee* provides a wide collection of **argument matchers** to use with the standard ``unittest.mock`` library.

It allows you to write simple, readable, and powerful assertions
on how the tested code should interact with your mocks:

.. code-block:: python

    from callee import Dict, StartsWith, String

    mock_requests.get.assert_called_with(
        String() & StartsWith('https://'),
        params=Dict(String(), String()))

With *callee*, you can avoid both the overly lenient |mock.ANY|_, as well as the tedious, error-prone code
that manually checks |Mock.call_args|_ and |Mock.call_args_list|_.

.. |mock.ANY| replace:: ``mock.ANY``
.. _mock.ANY: https://docs.python.org/3/library/unittest.mock.html#any
.. |Mock.call_args| replace:: ``Mock.call_args``
.. _Mock.call_args: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.call_args
.. |Mock.call_args_list| replace:: ``call_args_list``
.. _Mock.call_args_list: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.call_args_list


User's Guide
------------

Start here for the installation instructions and a quick, complete overview of *callee* and its usage.

.. include:: guide/toc.rst.inc


API Reference
-------------

If you are looking for detailed information about all the matchers offered by *callee*,
this is the place to go.

.. include:: reference/toc.rst.inc
