from mock import patch, MagicMock, Mock, mock_open, call, ANY
import unittest
from test_helper import *
from example import *

from python_base.example import Example
from python_base.example_delegate import *

class TestExampleDelegate(asynctest.TestCase):
    def setUp(self):
        self.example = Mock(spec=Example)
        create_patch(self, 'python_base.example_delegate.Example', Mock(return_value=self.example))
        self.delegate = ExampleDelegate()

    def test_creates_example(self):
        constructor = create_patch(self, 'python_base.example_delegate.Example', Mock(return_value=self.example))
        ExampleDelegate()
        constructor.assert_called()

    def test_delegates_post_call(self):
        self.delegate.make_post_request("http://some/url", {"key": "value"})
        self.example.make_post_request.assert_called_with("http://some/url", {"key": "value"})
