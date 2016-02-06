Installing
==========

**TL;DR**: On Python 2.6, 2.7, and 3.3+, simply use *pip* (preferably inside virtualenv):

.. code-block:: shell

    $ pip install callee

More detailed instructions and additional notes can be found below.


Compatibility
*************

*callee* itself has no external depedencies: it only needs Python. Both Python 2 and Python 3 is supported,
with some caveats:

* if you're using Python 2, you need version 2.6 or 2.7
* if you use Python 3, you need at least version 3.3

The library is tested against both CPython (the standard Python implementation) and `PyPy`_.

.. _PyPy: http://pypy.org/


About the mock library
**********************

Although it's not a hard dependency, by design *callee* is meant to be used with the ``unittest.mock`` module,
which implements *mock objects* for testing.

In Python 3.3 and later, this module is a part of `the standard library`_, and it's already available on any Python distribution.

In earlier versions of Python -- including 2.7 and even 2.6 -- you should be using the `backport`_ called ``mock``.
It has the exact same interface as ``unittest.mock``, and can be used to write forward-compatible test code.
You can install it from PyPI with *pip*:

.. code-block:: shell

    $ pip install mock

If you plan to run your tests against both Python 2.x and 3.x, the recommended way of importing the mock library
is the following:

.. code-block:: python

    try:
        import unittest.mock as mock
    except ImportError:
        import mock

You can then use the mock classes in your tests by referring to them as |mock.Mock|_ or |mock.MagicMock|_.
Additionally, you'll also have a convenient access to the rest of the mocking functionality, like the |@mock.patch|_
decorator.

.. _the standard library: https://docs.python.org/3/library/unittest.mock.html
.. _backport: https://pypi.python.org/pypi/mock

.. |mock.Mock| replace:: ``mock.Mock``
.. _mock.Mock: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
.. |mock.MagicMock| replace:: ``mock.MagicMock``
.. _mock.MagicMock: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.MagicMock
.. |@mock.patch| replace:: ``@mock.patch``
.. _@mock.patch: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch


Instructions
************

The preferred way to install *callee* is through *pip*:

.. code-block:: shell

    $ pip install callee

This will get you the most recent version available on `PyPI`_.

.. _PyPI: https://pypi.python.org/pypi/callee/

Bleeding edge
-------------

If you want to work with the development version instead, you may either manually clone it using Git, or have *pip*
install it directly from the Git repository.

The first option is especially useful when you need to make some modifications to the library itself
(which you'll hopefully contribute back via a pull request!). If that's the case, clone the library
and install it in development mode:

.. code-block:: shell

    $ git clone https://github.com/Xion/callee.git
    Initialized empty Git repository in ~/dev/callee/.git/
    $ cd callee
    # activate/create your virtualenv if necessary
    $ python setup.py develop
    ...
    Finished processing dependencies for callee

The second approach is adequate if you want to use some feature of the library that hasn't made it to a PyPI release yet
but don't need to make your own modifications. You can tell *pip* to pull the library directly from its Git repository:

.. code-block:: shell

    # activate/create your virtualenv if necessary
    $ pip install git+https://github.com/Xion/callee.git#egg=callee
