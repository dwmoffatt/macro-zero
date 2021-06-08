from src.macrozero import MacroZero
from src.modules.mkeyboard import KEY_NONE, KEY_ENTER, NONE_REPORT, KEY_H, KEY_E, KEY_1, KEY_MOD_LSHIFT, KEY_BACKSLASH


class TestVerifyReport:
    # @classmethod
    # def setup_class(cls):

    def setup_method(self, method):
        self.app = MacroZero(test_env=True, run_webserver=False)

    def test_build_report_correct_report_generated(self):
        """
        Tests that build_report returns correct report for given value
        :return:
        """
        test_value = "Enter"
        test_report = KEY_NONE + KEY_NONE + KEY_ENTER + (KEY_NONE * 5)
        result = self.app.mkeyboard.build_report(test_value)
        assert result == test_report

        test_value = None
        test_report = NONE_REPORT
        result = self.app.mkeyboard.build_report(test_value)
        assert result == test_report

        test_value = "H"
        test_report = KEY_MOD_LSHIFT + KEY_NONE + KEY_H + (KEY_NONE * 5)
        result = self.app.mkeyboard.build_report(test_value)
        assert result == test_report

        test_value = "e"
        test_report = KEY_NONE + KEY_NONE + KEY_E + (KEY_NONE * 5)
        result = self.app.mkeyboard.build_report(test_value)
        assert result == test_report

        test_value = "!"
        test_report = KEY_MOD_LSHIFT + KEY_NONE + KEY_1 + (KEY_NONE * 5)
        result = self.app.mkeyboard.build_report(test_value)
        assert result == test_report

        test_value = "\\"
        test_report = KEY_NONE + KEY_NONE + KEY_BACKSLASH + (KEY_NONE * 5)
        result = self.app.mkeyboard.build_report(test_value)
        assert result == test_report

        test_value = "|"
        test_report = KEY_MOD_LSHIFT + KEY_NONE + KEY_BACKSLASH + (KEY_NONE * 5)
        result = self.app.mkeyboard.build_report(test_value)
        assert result == test_report

    def teardown_method(self, method):
        del self.app

    # @classmethod
    # def teardown_class(cls):
