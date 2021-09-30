from flask import jsonify


class API:
    def __init__(self, flask_server=None):
        self._server = flask_server

        self._server.add_url_rule("/api/v1/hello", "hello", self.hello_world, methods=["GET"])

    @staticmethod
    def hello_world():
        return jsonify({"message": "Hello World!!"})
