Using matchers with ``mock``
============================

*Mocks* -- or more generally, *test doubles* -- are used to provide the necessary dependencies
(objects, functions, data, etc.) to the code under test. We often configure mocks to expose an interface that the code can rely on. We also expect that the tested code makes use of this interface in a well-defined, predictable way.

In Python, the configuration part mostly taken care of by the ``mock`` library. But when it comes to asserting
that the expected mocks interactions had happened, *callee* can help quite a bit.


Example
*******

Suppose you are testing the controller of a landing page for users that are signed in to your web application.
The page should display a portion of the most recent items of interest -- posts or notifications, or anything else
specific to the service.

The test seems straightforward enough:

.. code-block:: python

    @mock.patch.object(database, 'fetch_recent_items')
    def test_landing_page(self, mock_fetch_recent_items):
        login_user(self.user)
        self.http_client.get('/')
        mock_fetch_recent_items.assert_called_with(count=8)

Unfortunately, the assert it contains turns out to be quite brittle. The number of items to display is very much
a UX decision, and it likely changes pretty often as the UI is iterated upon. But with a test like that,
you have to go back and modify the assertion whenever the value is adjusted in the production code.

Not good! The test shouldn't really care what the exact count is. As long as it's a positive integer,
maybe except 1 or 2, the test should pass just fine.

Using **argument matchers** provided by *callee*, you can express this intent clearly and concisely:

.. code-block:: python

    from callee import GreaterThan, Integer

    # ...
    mock_fetch_recent_items.assert_called_with(
        count=Integer() & GreaterThan(1))

Much better! Now you can tweak the layout of the page without further issue.


Matching basics
***************

You can use all *callee* matchers any time you are asserting on calls received by ``Mock``, ``MagicMock``,
or other ``mock`` objects. They are applicable as arguments to any of the following methods:

    * ``assert_called_with``
    * ``assert_called_once_with``
    * ``assert_any_call``
    * ``assert_not_called``

Moreover, the |mock.call|_ helper can also accept matchers in place of call arguments. This enables you to also use
the |assert_has_calls|_ method if you like:

.. code-block:: python

    some_mock.assert_has_calls([
        call(0, String()),
        call(1, String()),
        call(2, String()),
    ])

Finally, you can still leverage matchers even when you're working directly with ``call_args_list``, ``method_calls``,
or ``mock_calls`` attributes. The only reason you'd still want that, though, is verifying the **exact** calls a mock receives, in order:

.. code-block:: python

    assert some_mock.call_args_list == [
        mock.call(String(), Integer()),
        mock.call(String(), 42),
    ]

Note that most tests don't need to be this rigid, so you should use this technique sparingly.

.. |mock.call| replace:: ``mock.call``
.. _mock.call: https://docs.python.org/3/library/unittest.mock.html#calls-as-tuples
.. |assert_has_calls| replace:: ``assert_has_calls``
.. _assert_has_calls: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.assert_has_calls


Combining matchers
******************

.. _logical-expressions:

Individual matchers, such as :class:`String <callee.strings.String>` or :class:`Float <callee.numbers.Float>`,
can be combined to build more complex expressions. This is accomplished with help from Python's "logical" operators:
``|``, ``&``, and ``~``.

Specifically, given matchers ``A`` and ``B``:

    * ``A | B`` matches objects that match ``A`` **or** ``B``
    * ``A & B`` matches objects that match both ``A`` **and** ``B``
    * ``~A`` matches objects do **not** match ``A``

Here are a few examples:

.. code-block:: python

    some_mock.assert_called_with(Number() | InstanceOf(Foo))
    some_mock.assert_called_with(String() & ShorterThan(9))
    some_mock.assert_called_with(String() & ~Contains('forbidden'))

All matchers can be combined this way, including any :doc:`custom ones <custom-matchers>` that you write yourself.

.. TODO(xion): mention the existence of And, Or, Not classes


Next steps
**********

Now that you know how to use matchers and how to combine them into more complex expressions, you probably want to
have a look at the wide array of existing matchers offerred by *callee*:

.. include:: ../reference/toc.rst.inc

If your needs can't be met by it, there is always a possibility of :doc:`defining your own matchers <custom-matchers>`
as well.
