import pytest
from src.macrozero import MacroZero
from src.modules import (
    MK_B1_PIN,
    MK_B2_PIN,
    MK_B3_PIN,
    MK_B4_PIN,
    MK_B5_PIN,
    MK_B6_PIN,
    MK_B7_PIN,
    MK_B8_PIN,
    RE_SW_PIN,
)
from src.modules.mkeyboard import (
    MK_COMMAND_MK_B1,
    MK_COMMAND_MK_B2,
    MK_COMMAND_MK_B3,
    MK_COMMAND_MK_B4,
    MK_COMMAND_MK_B5,
    MK_COMMAND_MK_B6,
    MK_COMMAND_MK_B7,
    MK_COMMAND_MK_B8,
)


class TestBtnRelease:
    # @classmethod
    # def setup_class(cls):

    def setup_method(self, method):
        self.app = MacroZero(test_env=True, run_webserver=False)

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            (MK_B1_PIN, MK_COMMAND_MK_B1),
            (MK_B2_PIN, MK_COMMAND_MK_B2),
            (MK_B3_PIN, MK_COMMAND_MK_B3),
            (MK_B4_PIN, MK_COMMAND_MK_B4),
            (MK_B5_PIN, MK_COMMAND_MK_B5),
            (MK_B6_PIN, MK_COMMAND_MK_B6),
            (MK_B7_PIN, MK_COMMAND_MK_B7),
            (MK_B8_PIN, MK_COMMAND_MK_B8),
        ],
    )
    def test_btn_release_valid_channel(self, test_input, expected):
        """
        Tests all button pin mappings put the correct value on the que
        :return:
        """
        self.app.mkeyboard.btn_release(test_input)
        que_value = self.app.input_que.get_nowait()
        assert que_value == expected

    def test_btn_release_invalid_channel(self):
        """
        Test an invalid channel input put nothing on the que
        :return:
        """
        self.app.mkeyboard.btn_release(RE_SW_PIN)
        assert self.app.input_que.qsize() == 0

    def teardown_method(self, method):
        del self.app

    # @classmethod
    # def teardown_class(cls):
