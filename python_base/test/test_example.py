import asynctest
from asynctest import Mock, mock_open, ANY
from python_base.test.test_helper import start_patch

import json
import os
import sys
import requests
from threading import Timer

from python_base.example import Example


class TestExample(asynctest.TestCase):
    def setUp(self):
        self.env_vars = {"EXAMPLE_VAR": "VALUE", "OTHER_VAR": ANY}
        self.p_getenv = Mock(side_effect=self.retrieve_env_var)
        start_patch(self, Example, os, new=Mock(getenv=self.p_getenv))
        self.p_stderr = Mock()
        start_patch(self, Example, sys, new=Mock(stderr=self.p_stderr))

        self.post_return = {"elements": [100, 2, 15, 28], "other_thing": "This is a thing (other)"}
        post = Mock(return_value=Mock(status_code=200,
                                      json=Mock(return_value=self.post_return)))
        self.post = post
        self.requests = start_patch(self, Example, requests, new=Mock(name="requests", post=post))

        self.open = start_patch(self,
                                target='builtins.open',
                                new=mock_open(read_data=json.dumps([{"field": 1}, {"field": 2}])))

        self.timer = Mock()
        self.timer_constructor = start_patch(self, Example, Timer, return_value=self.timer)

        self.example = Example()

    def test_gets_environment_variable_in_constructor(self):
        self.p_getenv.assert_called_with("EXAMPLE_VAR", "default to this")

    def test_sends_request(self):
        data = {"field": 1, "field2": 200}
        self.example.make_post_request("www.google.com", data)

        self.requests.post.assert_called_with("www.google.com", data=data)

    def test_writes_error_on_non_200(self):
        self.requests.post = Mock(return_value=Mock(status_code=404))
        self.example.make_post_request("www.google.com", {})

        self.p_stderr.write.assert_called_with("There was an error making the request: 404\n")

    def test_writes_error_on_exception(self):
        self.requests.post.side_effect = Exception("BadTimesMan")
        self.example.make_post_request("www.google.com", {})

        self.p_stderr.write.assert_called_with("There was an exception: Exception('BadTimesMan',)\n")

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
