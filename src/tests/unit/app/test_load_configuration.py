import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))))

from macrozero import MacroZero


class LoadConfigurationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = MacroZero(test_env=True, run_webserver=False)

    def test_load_configuration_returns_dictionary(self):
        """
        Tests that load_configuration loads data from json file into dictionary
        :return:
        """
        self.app.load_configuration()
        self.assertEqual(type(dict()), type(self.app.configuration))

    def tearDown(self):
        del self.app


if __name__ == "__main__":
    unittest.main()
