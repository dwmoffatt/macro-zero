"""
RGB Driver
"""
import logging
from .utils import set_bit, unset_bit
from . import STATUS_OK

RGB_COLOR_OFF = "Off"
RGB_COLOR_RED = "Red"
RGB_COLOR_BLUE = "Blue"
RGB_COLOR_GREEN = "Green"
RGB_COLOR_YELLOW = "Yellow"
RGB_COLOR_PURPLE = "Purple"
RGB_COLOR_CYAN = "Cyan"
RGB_COLOR_WHITE = "White"
COLOR_LIST = {
    RGB_COLOR_OFF: {"R": 0, "G": 0, "B": 0},
    RGB_COLOR_RED: {"R": 1, "G": 0, "B": 0},
    RGB_COLOR_BLUE: {"R": 0, "G": 0, "B": 1},
    RGB_COLOR_GREEN: {"R": 0, "G": 1, "B": 0},
    RGB_COLOR_YELLOW: {"R": 1, "G": 1, "B": 0},
    RGB_COLOR_PURPLE: {"R": 1, "G": 0, "B": 1},
    RGB_COLOR_CYAN: {"R": 0, "G": 1, "B": 1},
    RGB_COLOR_WHITE: {"R": 1, "G": 1, "B": 1},
}

IODIRA = 0x00
IODIRB = 0x01
OLATA = 0x14
OLATB = 0x15

BANK_A = "A"
BANK_B = "B"
BANK_LIST = [BANK_A, BANK_B]

OUTPUTS_PER_BANK = 8


class RGBDriver:
    def __init__(self, input_list=None, thread_lock=None, que=None, **kwargs):
        self._input_list = input_list
        self._thread_lock = thread_lock
        self._que = que
        self._i2c_bus = None

        self.device_address = 0x20
        self.output_mappings = {
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
        self.output_bank_a = 0b00000000
        self.output_bank_b = 0b00000000

        if "i2c_bus" in kwargs.keys():
            self._i2c_bus = kwargs["i2c_bus"]

    def module_init(self):
        logging.info("Initializing RGBDriver Module")

        # Set all GPA & GPB pins as outputs by setting all bits of IODIRA & IODIRB registers to 0
        self._i2c_bus.write_byte_data(self.device_address, IODIRA, 0b00000000)
        self._i2c_bus.write_byte_data(self.device_address, IODIRB, 0b00000000)

        # Write output banks
        self.write_output_banks()

        return True

    def module_close(self):
        logging.info("Closing RGBDriver Module")

        # Set outputs to 0
        self.output_bank_a = 0b00000000
        self.output_bank_b = 0b00000000
        self.write_output_banks()

        return True

    def build_output_bank(self, bank="A"):
        """
        Given the bank specified, generate the bit value based on the values in the output_mappings

        :param bank: Specified bank you want to generate output bit value for
        :return: Value in bit format of specified bank
        """
        # Check bank is of valid type, A or B
        value = 0b00000000

        if bank not in BANK_LIST:
            raise ValueError(f"bank needs to be of available types {BANK_LIST}")

        for index in range(0, OUTPUTS_PER_BANK):
            if self.output_mappings[f"Bank {bank}"][f"GP{index}"]["Value"] == 0:
                value = unset_bit(value, bit_index=index)
            elif self.output_mappings[f"Bank {bank}"][f"GP{index}"]["Value"] == 1:
                value = set_bit(value, bit_index=index)

        return value

    def set_output_mappings(self, color, index):
        """
        Given a color and index set the associated color in RGB Rep
        Color has to be one of the supported color types, throw ValueError otherwise
        Index needs to be between 1-4, throw ValueError otherwise

        :param color: color in COLOR_LIST
        :param index: int between 1-4
        :return status: OK on success, error message on error case
        """
        status = STATUS_OK

        if color not in COLOR_LIST.keys():
            raise ValueError(f"color value is not part of accepted colors - {COLOR_LIST.keys()}")

        if index < 1 or index > 4:
            raise ValueError("index needs to be between 1 and 4")

        rgb = COLOR_LIST.get(color)
        for gp in self.output_mappings[f"Bank {BANK_A}"].keys():
            if f"LED{index}" in self.output_mappings[f"Bank {BANK_A}"][gp]["Type"]:
                if "Red" in self.output_mappings[f"Bank {BANK_A}"][gp]["Type"]:
                    self.output_mappings[f"Bank {BANK_A}"][gp]["Value"] = rgb.get("R")
                elif "Green" in self.output_mappings[f"Bank {BANK_A}"][gp]["Type"]:
                    self.output_mappings[f"Bank {BANK_A}"][gp]["Value"] = rgb.get("G")
                elif "Blue" in self.output_mappings[f"Bank {BANK_A}"][gp]["Type"]:
                    self.output_mappings[f"Bank {BANK_A}"][gp]["Value"] = rgb.get("B")

        for gp in self.output_mappings[f"Bank {BANK_B}"].keys():
            if f"LED{index}" in self.output_mappings[f"Bank {BANK_B}"][gp]["Type"]:
                if "Red" in self.output_mappings[f"Bank {BANK_B}"][gp]["Type"]:
                    self.output_mappings[f"Bank {BANK_B}"][gp]["Value"] = rgb.get("R")
                elif "Green" in self.output_mappings[f"Bank {BANK_B}"][gp]["Type"]:
                    self.output_mappings[f"Bank {BANK_B}"][gp]["Value"] = rgb.get("G")
                elif "Blue" in self.output_mappings[f"Bank {BANK_B}"][gp]["Type"]:
                    self.output_mappings[f"Bank {BANK_B}"][gp]["Value"] = rgb.get("B")

        return status

    def write_output_banks(self):
        """
        Write both output banks
        :return:
        """
        # write outputs
        self._i2c_bus.write_byte_data(self.device_address, OLATA, self.output_bank_a)
        self._i2c_bus.write_byte_data(self.device_address, OLATB, self.output_bank_b)
