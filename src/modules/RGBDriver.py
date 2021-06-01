"""
RGB Driver
"""
import logging
from .utils import set_bit, unset_bit

RGB_COLOR_OFF = "Off"
RGB_COLOR_RED = "Red"
RGB_COLOR_BLUE = "Blue"
RGB_COLOR_GREEN = "Green"
RGB_COLOR_YELLOW = "Yellow"
RGB_COLOR_PURPLE = "Purple"
RGB_COLOR_CYAN = "Cyan"
RGB_COLOR_WHITE = "White"

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
        self._output_bank_a = 0b00000000
        self._output_bank_b = 0b00000000

        if "i2c_bus" in kwargs.keys():
            self._i2c_bus = kwargs["i2c_bus"]

    def module_init(self):
        logging.info("Initializing RGBDriver Module")

        # Set all GPA & GPB pins as outputs by setting all bits of IODIRA & IODIRB registers to 0
        self._i2c_bus.write_byte_data(self.device_address, IODIRA, 0b00000000)
        self._i2c_bus.write_byte_data(self.device_address, IODIRB, 0b00000000)

        # Set outputs to 0
        self._i2c_bus.write_byte_data(self.device_address, OLATA, self._output_bank_a)
        self._i2c_bus.write_byte_data(self.device_address, OLATB, self._output_bank_b)

    def module_close(self):
        logging.info("Closing RGBDriver Module")

        # Set outputs to 0
        self._i2c_bus.write_byte_data(self.device_address, OLATA, 0b00000000)
        self._i2c_bus.write_byte_data(self.device_address, OLATB, 0b00000000)

    def build_output_bank(self, bank="A"):
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
