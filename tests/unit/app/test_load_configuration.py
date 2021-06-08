from src.macrozero import MacroZero


class TestLoadConfiguration:
    # @classmethod
    # def setup_class(cls):

    def setup_method(self, method):
        self.app = MacroZero(test_env=True, run_webserver=False)

    def test_load_configuration_returns_dictionary(self):
        """
        Tests that load_configuration loads data from json file into dictionary
        :return:
        """
        self.app.load_configuration()
        assert isinstance(self.app.configuration, dict)

    def teardown_method(self, method):
        del self.app

    # @classmethod
    # def teardown_class(cls):
