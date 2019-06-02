import asynctest
from asynctest import MagicMock
from python_base.test.test_helper import start_patch

from python_base.example import Example
from python_base.example_delegate import ExampleDelegate


class TestExampleDelegate(asynctest.TestCase):
    def setUp(self):
        self.example = MagicMock(spec=Example)
        start_patch(self, ExampleDelegate, Example, return_value=self.example)
        self.delegate = ExampleDelegate()

    def test_creates_example(self):
        constructor = start_patch(self, ExampleDelegate, Example, return_value=self.example)
        ExampleDelegate()
        constructor.assert_called()

    def test_delegates_post_call(self):
        self.delegate.make_post_request("http://some/url", {"key": "value"})
        self.example.make_post_request.assert_called_with("http://some/url", {"key": "value"})

    async def test_delegates_async_method(self):
        await self.delegate.an_async_delegation()
        self.example.an_async_method.assert_awaited_with()
