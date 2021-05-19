import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))))

from macrozero import MacroZero
from modules.mkeyboard import KEY_NONE, KEY_ENTER, NONE_REPORT, KEY_H, KEY_E, KEY_1, KEY_MOD_LSHIFT, KEY_BACKSLASH


class VerifyReportTestCase(unittest.TestCase):
    def setUp(self):
        self.app = MacroZero(test_env=True)

    def test_build_report_correct_report_generated(self):
        """
        Tests that build_report returns correct report for given value
        :return:
        """
        test_value = "Enter"
        test_report = KEY_NONE + KEY_NONE + KEY_ENTER + (KEY_NONE * 5)
        result = self.app.mkeyboard.build_report(test_value)
        self.assertEqual(test_report, result)

        test_value = None
        test_report = NONE_REPORT
        result = self.app.mkeyboard.build_report(test_value)
        self.assertEqual(test_report, result)

        test_value = "H"
        test_report = KEY_MOD_LSHIFT + KEY_NONE + KEY_H + (KEY_NONE * 5)
        result = self.app.mkeyboard.build_report(test_value)
        self.assertEqual(test_report, result)

        test_value = "e"
        test_report = KEY_NONE + KEY_NONE + KEY_E + (KEY_NONE * 5)
        result = self.app.mkeyboard.build_report(test_value)
        self.assertEqual(test_report, result)

        test_value = "!"
        test_report = KEY_MOD_LSHIFT + KEY_NONE + KEY_1 + (KEY_NONE * 5)
        result = self.app.mkeyboard.build_report(test_value)
        self.assertEqual(test_report, result)

        test_value = "\\"
        test_report = KEY_NONE + KEY_NONE + KEY_BACKSLASH + (KEY_NONE * 5)
        result = self.app.mkeyboard.build_report(test_value)
        self.assertEqual(test_report, result)

    def tearDown(self):
        del self.app


if __name__ == "__main__":
    unittest.main()
