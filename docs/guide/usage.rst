Using matchers with ``mock``
============================

*Mocks* -- or more generally, *test doubles* -- are used to provide the necessary dependencies
(objects, functions, data, etc.) to the code under test. We often configure mocks to expose an interface that the code can rely on. We also expect that the tested code makes use of this interface in a well-defined, predictable way.

In Python, the configuration part mostly taken care of by the ``mock`` library. But when it comes to asserting
that the expected interactions with mocks had happened, *callee* can help quite a bit.


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
    mock_fetch_recent_items.assert_called_with(count=Integer() & GreaterThan(1))

Much better! Now you can tweak the layout of the page without any issues.
