import os, requests, json, traceback
from sys import stderr
from threading import Timer


class Example():
    def __init__(self):
        self.env_var = os.getenv("EXAMPLE_VAR", "default to this")
        with open('./data/sample_data.json', 'r') as f:
            self.loaded_data = json.loads(f.read())

    def get_first_element(self):
        return self.loaded_data.get("elements")[0]

    def make_post_request(self, url, data):
        try:
            response = requests.post(url, data=data)
            if response.status_code != 200:
                stderr.write("There was an error making the request: %s\n"%response.status_code)
            else:
                return response.json()
        except Exception as e:
            #print(traceback.format_exc())
            stderr.write("There was an exception: %s\n"%repr(e))

    def execute_on_timer(self, period, f):
        f()
        timer = Timer(period, self.execute_on_timer, period, f)
        timer.start()
