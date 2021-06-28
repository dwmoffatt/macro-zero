import sqlite3 as sql
from flask import Flask, jsonify


class API:
    def __init__(self, thread_lock=None, que=None):
        self._thread_lock = thread_lock
        self._que = que

        self.server = Flask(__name__)
        self.server.add_url_rule("/api/v1/hello", "hello", self.hello_world, methods=["GET"])

        self.con = sql.connect("macro-zero.db")

    def init_db(self):
        """
        Create tables

        :return:
        """

    def run_api(self):
        self.server.run(host="0.0.0.0")

    @staticmethod
    def hello_world():
        return jsonify({"message": "Hello World!!"})
