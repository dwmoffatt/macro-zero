"""
Macro-Zero Interface
==========================

Main Control for Device
"""

# import argparse
# import threading
import logging
from modules.eink import EInk

logging.basicConfig(level=logging.DEBUG)


class MacroZero:
    def __init__(self):
        """
        Creates Macro-Zero Device Object
        """

        self.eink = EInk()

        self.running = False

    def init(self):
        """
        Initializes all I/O, Peripherals and anything else needed for the device to run

        :return: Nothing
        """

    def run(self):
        """
        Runs the interface. This function should never return. It only bails on an error

        :return: Nothing
        """


if __name__ in "__main__":

    macro_zero = MacroZero()

    macro_zero.init()

    macro_zero.run()
