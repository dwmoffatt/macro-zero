import unittest
from src.macrozero import MacroZero
from src.modules.mkeyboard import KEY_NONE, KEY_ENTER


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

    def tearDown(self):
        del self.app


if __name__ == "__main__":
    unittest.main()
