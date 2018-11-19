from python_base.example import Example


class ExampleDelegate:
    def __init__(self):
        self.example = Example()

    def make_post_request(self, url, data):
        self.example.make_post_request(url, data)
