import pytest
from src.macrozero import MacroZero
from src.modules import PSO_PIN
from src.modules.pso import PSO_COMMAND_PSO


class TestBtnRelease:
    # @classmethod
    # def setup_class(cls):

    def setup_method(self, method):
        self.app = MacroZero(test_env=True, run_webserver=False)

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            (PSO_PIN, PSO_COMMAND_PSO),
        ],
    )
    def test_pso_switch_over_valid_channel(self, test_input, expected):
        """
        Tests pso switch over puts the correct value on the que
        :return:
        """
        self.app.pso.pso_switch_over(test_input)
        que_value = self.app.input_que.get_nowait()
        assert que_value == expected

    def teardown_method(self, method):
        del self.app

    # @classmethod
    # def teardown_class(cls):
