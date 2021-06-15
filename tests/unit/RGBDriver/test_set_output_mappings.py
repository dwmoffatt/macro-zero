import copy
import pytest
from src.macrozero import MacroZero
from src.modules.RGBDriver import (
    BANK_A,
    BANK_B,
    COLOR_LIST,
    RGB_COLOR_OFF,
    RGB_COLOR_RED,
    RGB_COLOR_BLUE,
    RGB_COLOR_GREEN,
    RGB_COLOR_YELLOW,
    RGB_COLOR_PURPLE,
    RGB_COLOR_CYAN,
    RGB_COLOR_WHITE,
)
from src.modules import STATUS_OK

DEFAULT_OUTPUT_MAPPINGS = {
    "Bank A": {
        "GP0": {"Type": "LED3 Blue", "Value": 0},
        "GP1": {"Type": "LED3 Green", "Value": 0},
        "GP2": {"Type": "LED3 Red", "Value": 0},
        "GP3": {"Type": "LED4 Red", "Value": 0},
        "GP4": {"Type": "LED4 Green", "Value": 0},
        "GP5": {"Type": "LED4 Blue", "Value": 0},
        "GP6": {"Type": "N/A", "Value": 0},
        "GP7": {"Type": "N/A", "Value": 0},
    },
    "Bank B": {
        "GP0": {"Type": "LED1 Blue", "Value": 0},
        "GP1": {"Type": "LED1 Green", "Value": 0},
        "GP2": {"Type": "LED1 Red", "Value": 0},
        "GP3": {"Type": "LED2 Red", "Value": 0},
        "GP4": {"Type": "LED2 Green", "Value": 0},
        "GP5": {"Type": "LED2 Blue", "Value": 0},
        "GP6": {"Type": "N/A", "Value": 0},
        "GP7": {"Type": "N/A", "Value": 0},
    },
}


class TestSetOutputMappings:
    # @classmethod
    # def setup_class(cls):

    def setup_method(self, method):
        self.app = MacroZero(test_env=True, run_webserver=False)

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ((RGB_COLOR_OFF, 1), STATUS_OK),
            ((RGB_COLOR_OFF, 2), STATUS_OK),
            ((RGB_COLOR_OFF, 3), STATUS_OK),
            ((RGB_COLOR_OFF, 4), STATUS_OK),
            ((RGB_COLOR_RED, 1), STATUS_OK),
            ((RGB_COLOR_RED, 2), STATUS_OK),
            ((RGB_COLOR_RED, 3), STATUS_OK),
            ((RGB_COLOR_RED, 4), STATUS_OK),
            ((RGB_COLOR_BLUE, 1), STATUS_OK),
            ((RGB_COLOR_BLUE, 2), STATUS_OK),
            ((RGB_COLOR_BLUE, 3), STATUS_OK),
            ((RGB_COLOR_BLUE, 4), STATUS_OK),
            ((RGB_COLOR_GREEN, 1), STATUS_OK),
            ((RGB_COLOR_GREEN, 2), STATUS_OK),
            ((RGB_COLOR_GREEN, 3), STATUS_OK),
            ((RGB_COLOR_GREEN, 4), STATUS_OK),
            ((RGB_COLOR_YELLOW, 1), STATUS_OK),
            ((RGB_COLOR_YELLOW, 2), STATUS_OK),
            ((RGB_COLOR_YELLOW, 3), STATUS_OK),
            ((RGB_COLOR_YELLOW, 4), STATUS_OK),
            ((RGB_COLOR_PURPLE, 1), STATUS_OK),
            ((RGB_COLOR_PURPLE, 2), STATUS_OK),
            ((RGB_COLOR_PURPLE, 3), STATUS_OK),
            ((RGB_COLOR_PURPLE, 4), STATUS_OK),
            ((RGB_COLOR_CYAN, 1), STATUS_OK),
            ((RGB_COLOR_CYAN, 2), STATUS_OK),
            ((RGB_COLOR_CYAN, 3), STATUS_OK),
            ((RGB_COLOR_CYAN, 4), STATUS_OK),
            ((RGB_COLOR_WHITE, 1), STATUS_OK),
            ((RGB_COLOR_WHITE, 2), STATUS_OK),
            ((RGB_COLOR_WHITE, 3), STATUS_OK),
            ((RGB_COLOR_WHITE, 4), STATUS_OK),
        ],
    )
    def test_set_output_mappings_valid_index_and_color(self, test_input, expected):
        """
        Tests that output_mappings is updated correctly and OK is returned
        :return:
        """
        result_output_mappings = copy.deepcopy(DEFAULT_OUTPUT_MAPPINGS)
        rgb = COLOR_LIST.get(test_input[0])
        for gp in result_output_mappings[f"Bank {BANK_A}"].keys():
            if f"LED{test_input[1]}" in result_output_mappings[f"Bank {BANK_A}"][gp]["Type"]:
                if "Red" in result_output_mappings[f"Bank {BANK_A}"][gp]["Type"]:
                    result_output_mappings[f"Bank {BANK_A}"][gp]["Value"] = rgb.get("R")
                elif "Green" in result_output_mappings[f"Bank {BANK_A}"][gp]["Type"]:
                    result_output_mappings[f"Bank {BANK_A}"][gp]["Value"] = rgb.get("G")
                elif "Blue" in result_output_mappings[f"Bank {BANK_A}"][gp]["Type"]:
                    result_output_mappings[f"Bank {BANK_A}"][gp]["Value"] = rgb.get("B")

        for gp in result_output_mappings[f"Bank {BANK_B}"].keys():
            if f"LED{test_input[1]}" in result_output_mappings[f"Bank {BANK_B}"][gp]["Type"]:
                if "Red" in result_output_mappings[f"Bank {BANK_B}"][gp]["Type"]:
                    result_output_mappings[f"Bank {BANK_B}"][gp]["Value"] = rgb.get("R")
                elif "Green" in result_output_mappings[f"Bank {BANK_B}"][gp]["Type"]:
                    result_output_mappings[f"Bank {BANK_B}"][gp]["Value"] = rgb.get("G")
                elif "Blue" in result_output_mappings[f"Bank {BANK_B}"][gp]["Type"]:
                    result_output_mappings[f"Bank {BANK_B}"][gp]["Value"] = rgb.get("B")

        assert self.app.rgb_driver.output_mappings == DEFAULT_OUTPUT_MAPPINGS

        result = self.app.rgb_driver.set_output_mappings(test_input[0], test_input[1])
        assert result == STATUS_OK
        assert result_output_mappings == self.app.rgb_driver.output_mappings

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            (("Pink", 1), None),
            ((RGB_COLOR_BLUE, 0), None),
            ((RGB_COLOR_BLUE, 5), None),
        ],
    )
    def test_set_output_mappings_invalid_index_or_color(self, test_input, expected):
        """
        Tests invalid index or color raises ValueError
        :return:
        """
        with pytest.raises(ValueError):
            self.app.rgb_driver.set_output_mappings(test_input[0], test_input[1])

    def teardown_method(self, method):
        del self.app

    # @classmethod
    # def teardown_class(cls):
