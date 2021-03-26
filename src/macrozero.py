"""
Macro-Zero Interface
==========================

Main Control for Device
"""

import argparse

# import threading
import logging
from modules.eink import EInk
import RPi.GPIO as GPIO

logging.basicConfig(
    filename="macro_zero.log", format="[%(asctime)s][%(levelname)s] - %(message)s", filemode="w", level=logging.DEBUG
)


class MacroZero:
    def __init__(self, test_image=0):
        """
        Creates Macro-Zero Device Object
        """

        self.eink = EInk()
        self.test_image = test_image

        self.running = False

    def init(self):
        """
        Initializes all I/O, Peripherals and anything else needed for the device to run

        :return: Nothing
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.eink.module_init()
        self.eink.clear()

    def run(self):
        """
        Runs the interface. This function should never return. It only bails on an error

        :return: Nothing
        """
        self.running = True

        while self.running:

            if self.test_image == 1 or self.test_image == 3:
                self.eink.test_horizontal_image()
                if self.test_image == 1:
                    self.running = False

            if self.test_image == 2 or self.test_image == 3:
                self.eink.test_vertical_image()
                self.running = False

    def close(self):
        """
        Closes all modules and resets I/0

        :return:
        """
        self.eink.module_close()

        GPIO.cleanup()


if __name__ in "__main__":

    macro_zero = None

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--testimage",
            "-ti",
            help="Test Image Level 0,1,2,3",
            default=0,
            const=0,
            nargs="?",
            type=int,
            choices=list(range(0, 4)),
        )
        args = parser.parse_args()

        macro_zero = MacroZero(test_image=args.testimage)

        macro_zero.init()

        macro_zero.run()

    except Exception:
        logging.exception("MacroZero Crashed!!!!!")

    macro_zero.close()
