import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))))

from macrozero import MacroZero


class VerifyReportTestCase(unittest.TestCase):
    def setUp(self):
        self.app = MacroZero(test_env=True)

    def test_verify_report_length_error(self):
        """
        Test that verify_report throws ValueError if report length is not equal to 8
        :return:
        """
        test_report = b"\x00\x00\x00\x00\x00"  # 5 bytes
        with self.assertRaises(ValueError):
            self.app.mkeyboard._verify_report(test_report)

        test_report = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00"  # 9 bytes
        with self.assertRaises(ValueError):
            self.app.mkeyboard._verify_report(test_report)

    def test_verify_report_first_byte_not_accepted_modifier(self):
        """
        Tests that verify_report throws ValueError if the first byte is not one of accepted modifiers
        :return:
        """
        test_report = b"\x22\x00\x00\x00\x00\x00\x00\x00"  # 8 bytes
        with self.assertRaises(ValueError):
            self.app.mkeyboard._verify_report(test_report)

    def test_verify_report_second_byte_not_00(self):
        """
        Tests that verify_report throws ValueError if second byte in report is not x00
        :return:
        """
        test_report = b"\x00\x10\x00\x00\x00\x00\x00\x00"  # 8 bytes
        with self.assertRaises(ValueError):
            self.app.mkeyboard._verify_report(test_report)

    def test_verify_report_valid_report(self):
        """
        Tests that verify_report returns True and doesn't throw any exceptions when valid report is passed in
        :return:
        """
        test_report = b"\x00\x00\x00\x00\x00\x00\x00\x00"  # 8 bytes
        result = self.app.mkeyboard._verify_report(test_report)
        self.assertTrue(result)

        test_report = b"\x02\x00\x04\x00\x00\x00\x00\x00"  # 8 bytes
        result = self.app.mkeyboard._verify_report(test_report)
        self.assertTrue(result)

    def tearDown(self):
        del self.app


if __name__ == "__main__":
    unittest.main()
