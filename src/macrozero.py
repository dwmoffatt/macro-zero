"""
Macro-Zero Interface
==========================

Main Control for Device
"""

import os
import argparse
import threading
import logging
import queue
from modules import MK_B1_PIN, MK_B2_PIN, MK_B3_PIN, MK_B4_PIN, MK_B5_PIN, MK_B6_PIN, MK_B7_PIN, MK_B8_PIN
from modules.mkeyboard import MKeyboard
import RPi.GPIO as GPIO

logging.basicConfig(
    filename="macro_zero.log", format="[%(asctime)s][%(levelname)s] - %(message)s", filemode="w", level=logging.DEBUG
)


class MacroZero:
    def __init__(self, test_image=0):
        """
        Creates Macro-Zero Device Object
        """
        self.test_image = test_image
        self.thread_lock = threading.Lock()
        self.input_que = queue.Queue(maxsize=50)
        self.button_input_list = [
            MK_B1_PIN,
            MK_B2_PIN,
            MK_B3_PIN,
            MK_B4_PIN,
            MK_B5_PIN,
            MK_B6_PIN,
            MK_B7_PIN,
            MK_B8_PIN,
        ]

        self.mkeyboard = MKeyboard(self.button_input_list, self.thread_lock, self.input_que)
        self.running = False
        self.power_switch_over = False

    def init(self):
        """
        Initializes all I/O, Peripherals and anything else needed for the device to run

        :return: Nothing
        """
        logging.info("Initializing macro-zero I/O & peripherals")

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.mkeyboard.module_init()

    def run(self):
        """
        Runs the interface. This function returns when PSO signals that device is shutting down.

        Each loop and entry will be pulled off the Que and processed.

        Based on events keyboards macros/display changes will take place.

        :return: Nothing
        """
        logging.info("Running macro-zero interface")

        self.running = True

        while self.running:

            # Check if running on supercaps, bail out of main loop
            if self.power_switch_over:
                self.running = False

    def close(self):
        """
        Closes all modules and resets I/0

        :return:
        """
        logging.info("Closing macro-zero interface")

        self.mkeyboard.module_close()

        GPIO.cleanup()

        if self.power_switch_over:
            logging.info("System shutdown started!")
            os.system("systemctl poweroff")


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
