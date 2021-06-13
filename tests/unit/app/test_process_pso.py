from src.macrozero import MacroZero
from src.modules import STATUS_OK


class TestProcessPSO:
    # @classmethod
    # def setup_class(cls):

    def setup_method(self, method):
        self.app = MacroZero(test_env=True, run_webserver=False)

    def test_process_pso(self):
        """
        Tests that _process_pso sets power_switch_over True and returns OK
        :return:
        """
        result = self.app._process_pso()
        assert self.app.power_switch_over is True
        assert result == STATUS_OK

    def teardown_method(self, method):
        del self.app

    # @classmethod
    # def teardown_class(cls):
