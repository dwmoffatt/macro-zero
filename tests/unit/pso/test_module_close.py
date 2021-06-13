import pytest
from src.macrozero import MacroZero
from src.modules import RUNNING_ON_PI


class TestModuleInit:
    # @classmethod
    # def setup_class(cls):

    def setup_method(self, method):
        self.app = MacroZero(test_env=True, run_webserver=False)

    @pytest.mark.skipif(RUNNING_ON_PI is False, reason="Requires running on Raspberry-Pi")
    def test_module_close(self):
        """
        Tests that pso module_close runs correctly
        Requires init'ing the module first
        :return:
        """
        self.app.pso.module_init()
        result = self.app.pso.module_close()
        assert result is True

    def teardown_method(self, method):
        del self.app

    # @classmethod
    # def teardown_class(cls):
