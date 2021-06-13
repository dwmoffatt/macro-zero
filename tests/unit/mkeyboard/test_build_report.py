import pytest
from src.macrozero import MacroZero
from src.modules.mkeyboard import KEY_NONE, KEY_ENTER, NONE_REPORT, KEY_H, KEY_E, KEY_1, KEY_MOD_LSHIFT, KEY_BACKSLASH


class TestVerifyReport:
    # @classmethod
    # def setup_class(cls):

    def setup_method(self, method):
        self.app = MacroZero(test_env=True, run_webserver=False)

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("Enter", KEY_NONE + KEY_NONE + KEY_ENTER + (KEY_NONE * 5)),
            (None, NONE_REPORT),
            ("H", KEY_MOD_LSHIFT + KEY_NONE + KEY_H + (KEY_NONE * 5)),
            ("e", KEY_NONE + KEY_NONE + KEY_E + (KEY_NONE * 5)),
            ("!", KEY_MOD_LSHIFT + KEY_NONE + KEY_1 + (KEY_NONE * 5)),
            ("\\", KEY_NONE + KEY_NONE + KEY_BACKSLASH + (KEY_NONE * 5)),
            ("|", KEY_MOD_LSHIFT + KEY_NONE + KEY_BACKSLASH + (KEY_NONE * 5)),
        ],
    )
    def test_build_report_correct_report_generated(self, test_input, expected):
        """
        Tests that build_report returns correct report for given value
        :return:
        """
        result = self.app.mkeyboard.build_report(test_input)
        assert result == expected

    def teardown_method(self, method):
        del self.app

    # @classmethod
    # def teardown_class(cls):
