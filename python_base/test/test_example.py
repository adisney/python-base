from mock import patch, MagicMock, Mock, mock_open, call, ANY
import unittest
from test_helper import *
from example import *

import json

class TestExample(unittest.TestCase):
    def setUp(self):
        self.env_vars = {"EXAMPLE_VAR": "VALUE"}
        self.getenv = Mock(side_effect=self.retrieve_env_var)
        create_patch(self, 'os.getenv', self.getenv)
        self.stderr = create_patch(self, 'example.stderr')

        self.post_return = {"elements":[100, 2, 15, 28], "other_thing": "This is a thing (other)"}
        post = Mock(return_value=Mock(status_code=200,
                                      json=Mock(return_value=self.post_return)))
        self.post = post
        self.requests = create_patch(self, 'example.requests', Mock(name="requests", post=post))

        self.open = create_patch(self,
                                 'builtins.open',
                                 mock_open(read_data=json.dumps([{"field": 1}, {"field": 2}])))

        self.timer = Mock()
        self.timer_constructor = create_patch(self, 'example.Timer', Mock(return_value=self.timer))

        self.example = Example()

    def test_gets_environment_variable_in_constructor(self):
        self.getenv.assert_called_with("EXAMPLE_VAR", "default to this")

    def test_sends_request(self):
        data = {"field": 1, "field2": 200}
        self.example.make_post_request("www.google.com", data)

        self.requests.post.assert_called_with("www.google.com", data=data)

    def test_writes_error_on_non_200(self):
        self.requests.post = Mock(return_value=Mock(status_code=404))
        self.example.make_post_request("www.google.com", {})

        self.stderr.write.assert_called_with("There was an error making the request: 404\n")

    def test_writes_error_on_exception(self):
        self.requests.post.side_effect=Exception("BadTimesMan")
        self.example.make_post_request("www.google.com", {})

        self.stderr.write.assert_called_with("There was an exception: Exception('BadTimesMan',)\n")

    def test_gets_json_response_from_request(self):
        self.assertEqual(self.post_return, self.example.make_post_request("www.google.com", {}))

    def test_timer_created(self):
        self.example.execute_on_timer(20, self.placeholder)
        self.timer_constructor.assert_called_with(20, self.example.execute_on_timer, 20, self.placeholder)

    def test_timer_started(self):
        self.example.execute_on_timer(20, self.placeholder)
        self.timer.start.assert_called()

    def retrieve_env_var(self, var_name, default):
        if var_name in self.env_vars:
            return self.env_vars.get(var_name)
        return default

    def placeholder(self):
        pass
