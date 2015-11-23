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

# TODO(xion): add example

Moreover, the |mock.call|_ helper can also accept matchers in place of call arguments. This enables you to also use
the |assert_has_calls|_ method if you like.

# TODO(xion): add example

Finally, you can still leverage matchers even when you're working directly with ``call_args_list``, ``method_calls``,
or ``mock_calls`` attributes. The only reason you'd still want that, though, is verifying the **exact** calls a mock receives, in order:

.. code-block:: python

    assert some_mock.call_args_list == [
        mock.call(String(), Integer()),
        mock.call(String(), 42),
    ]

Note that most tests don't need to be this rigid, so you should use that technique sparingly.

.. |mock.call| replace:: ``mock.call``
.. _mock.call: https://docs.python.org/3/library/unittest.mock.html#calls-as-tuples
.. |assert_has_calls| replace:: ``assert_has_calls``
.. _assert_has_calls: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.assert_has_calls


Combining matchers
******************

TODO(xion): describe & | ~ operators
