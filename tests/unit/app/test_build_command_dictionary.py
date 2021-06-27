class TestBuildCommandDictionary:
    # @classmethod
    # def setup_class(cls):

    # def setup_method(self, method):

    def test_build_command_dictionary_returns_dictionary(self, app):
        """
        Tests that build_command_dictionary returns a dictionary
        :return:
        """
        assert isinstance(app.build_command_dictionary(), dict)

    # def teardown_method(self, method):

    # @classmethod
    # def teardown_class(cls):
