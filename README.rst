callee
======

Argument matchers for *unittest.mock*

|Version| |Development Status| |Python Versions| |License| |Build Status|

.. |Version| image:: https://img.shields.io/pypi/v/callee.svg?style=flat
    :target: https://pypi.python.org/pypi/callee
    :alt: Version
.. |Development Status| image:: https://img.shields.io/pypi/status/callee.svg?style=flat
    :target: https://pypi.python.org/pypi/callee/
    :alt: Development Status
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/callee.svg?style=flat
    :target: https://pypi.python.org/pypi/callee
    :alt: Python versions
.. |License| image:: https://img.shields.io/pypi/l/callee.svg?style=flat
    :target: https://github.com/Xion/callee/blob/master/LICENSE
    :alt: License
.. |Build Status| image:: https://img.shields.io/travis/Xion/callee.svg?style=flat
    :target: https://travis-ci.org/Xion/callee
    :alt: Build Status


More robust tests
~~~~~~~~~~~~~~~~~

Python's `mocking library`_ (or its `backport`_ for Python <3.3) is simple, reliable, and easy to use.
But it is also a little lacking when it comes to asserting what calls a mock has received.

You can be either very specific::

    my_mock.assert_called_with(42, some_foo_object, 'certain string')

or extremely general::

    my_mock.assert_called_with(ANY, ANY, ANY)
    # passes as long as argument count is the same

This can make your tests over-specified (and thus fragile) or too broad, missing some erroneous
cases and possibly letting your code fail in production.

*callee* provides **argument matchers** that allow you to be exactly as precise as you want::

    my_mock.assert_called_with(Number(), InstanceOf(Foo), String())

without tedious, handcrafted, and poorly readable code that checks ``call_args`` or ``call_args_list``::

    for posargs, kwargs in my_mock.call_args_list:
        self.assertIsInstance(posargs[0], int)
        self.assertIsInstance(posargs[1], Foo)
        self.assertIsInstance(posargs[2], str)

It has plenty of matcher types to fit all common and uncommon needs, and you can easily write your own if necessary.

.. _mocking library: https://docs.python.org/3/library/unittest.mock.html
.. _backport: https://pypi.python.org/pypi/mock
