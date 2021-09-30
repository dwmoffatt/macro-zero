import sqlite3 as sql


class Database:
    def __init__(self, input_list=None, thread_lock=None, que=None):
        self._input_list = input_list
        self._thread_lock = thread_lock
        self._que = que

        self.db_con = sql.connect("macro-zero.db")

    def init_db(self):
        """
        Create tables

        :return:
        """
