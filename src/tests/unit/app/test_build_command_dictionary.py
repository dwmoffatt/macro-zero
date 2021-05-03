import unittest
from src.macrozero import MacroZero


class BuildCommandDictionaryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = MacroZero(test_env=True)

    def test_build_command_dictionary_returns_dictionary(self):
        """
        Tests that build_command_dictionary returns a dictionary
        :return:
        """
        type_dict = dict()
        self.assertEqual(type(type_dict), type(self.app.build_command_dictionary()))

    def tearDown(self):
        del self.app


if __name__ == "__main__":
    unittest.main()
