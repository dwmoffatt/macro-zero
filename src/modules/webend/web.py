from modules.webend.api import API
from flask import Flask


class Web:
    def __init__(self, thread_lock=None, que=None):
        self._thread_lock = thread_lock
        self._que = que

        self.server = Flask(__name__)
        self.api = API(self.server)

    def run_api(self):
        self.server.run(host="0.0.0.0", port=1994)
