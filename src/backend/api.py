from flask import Flask


class API:
    def __init__(self):
        self.server = Flask(__name__)
        self.server.add_url_rule("/", "hello", self.hello_world)

    def run_api(self):
        self.server.run(host="0.0.0.0")

    def hello_world(self):
        return "Hello World!!"
