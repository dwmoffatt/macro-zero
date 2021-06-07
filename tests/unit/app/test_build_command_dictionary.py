from src.macrozero import MacroZero


class TestBuildCommandDictionary:
    # @classmethod
    # def setup_class(cls):

    def setup_method(self, method):
        self.app = MacroZero(test_env=True, run_webserver=False)

    def test_build_command_dictionary_returns_dictionary(self):
        """
        Tests that build_command_dictionary returns a dictionary
        :return:
        """
        assert isinstance(self.app.build_command_dictionary(), dict)

    def teardown_method(self, method):
        del self.app

    # @classmethod
    # def teardown_class(cls):
