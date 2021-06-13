import pytest
from src.macrozero import MacroZero
from src.modules import RE_SW_PIN
from src.modules.rotaryencoder import RE_COMMAND_RE_B1


class TestBtnRelease:
    # @classmethod
    # def setup_class(cls):

    def setup_method(self, method):
        self.app = MacroZero(test_env=True, run_webserver=False)

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            (RE_SW_PIN, RE_COMMAND_RE_B1),
        ],
    )
    def test_btn_release_valid_channel(self, test_input, expected):
        """
        Tests rotary encoder button put the correct value on the que
        :return:
        """
        self.app.mode_select_rotary_encoder.btn_release(test_input)
        que_value = self.app.input_que.get_nowait()
        assert que_value == expected

    def teardown_method(self, method):
        del self.app

    # @classmethod
    # def teardown_class(cls):
