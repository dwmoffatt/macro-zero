import pytest
from src.macrozero import MacroZero
from src.modules.RGBDriver import BANK_A, BANK_B


class TestBuildOutputBank:
    # @classmethod
    # def setup_class(cls):

    def setup_method(self, method):
        self.app = MacroZero(test_env=True, run_webserver=False)

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            (("00000000", "00000000"), (0b00000000, 0b00000000)),
            (("11111111", "00000000"), (0b11111111, 0b00000000)),
            (("11111111", "11111111"), (0b11111111, 0b11111111)),
            (("00000000", "11111111"), (0b00000000, 0b11111111)),
            (("11010110", "01010001"), (0b11010110, 0b01010001)),
        ],
    )
    def test_build_output_bank_valid_bank(self, test_input, expected):
        """
        Tests that what is present in output_mappings is return
        :return:
        """
        for i in enumerate(test_input[0]):
            self.app.rgb_driver.output_mappings[f"Bank {BANK_A}"][f"GP{7 - i[0]}"]["Value"] = int(i[1])

        for i in enumerate(test_input[1]):
            self.app.rgb_driver.output_mappings[f"Bank {BANK_B}"][f"GP{7 - i[0]}"]["Value"] = int(i[1])

        result = self.app.rgb_driver.build_output_bank(BANK_A)
        assert result == expected[0]

        result = self.app.rgb_driver.build_output_bank(BANK_B)
        assert result == expected[1]

    def test_build_output_bank_raise_value_error_invalid_bank(self):
        """
        Tests that ValueError Exception is generated when invalid bank is passed in
        :return:
        """
        with pytest.raises(ValueError):
            self.app.rgb_driver.build_output_bank("C")

    def teardown_method(self, method):
        del self.app

    # @classmethod
    # def teardown_class(cls):
