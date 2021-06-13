import pytest
from src.macrozero import MacroZero


class TestInvalidCommand:
    # @classmethod
    # def setup_class(cls):

    def setup_method(self, method):
        self.app = MacroZero(test_env=True, run_webserver=False)

    def test_invalid_command(self):
        """
        Tests that invalid_command returns ValueError
        :return:
        """
        with pytest.raises(ValueError):
            self.app._invalid_command()

    def teardown_method(self, method):
        del self.app

    # @classmethod
    # def teardown_class(cls):
