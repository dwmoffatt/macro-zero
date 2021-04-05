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
from modules import (
    INPUT_LIST_KEY_INPUT_TYPE,
    INPUT_LIST_KEY_PIN_NUMBER,
    INPUT_TYPE_BUTTON,
    INPUT_TYPE_SWITCH,
    INPUT_TYPE_ROTARY_ENCODER_CLK,
    INPUT_TYPE_ROTARY_ENCODER_DIR,
    INPUT_TYPE_DISPLAY_RST,
    INPUT_TYPE_DISPLAY_DC,
    DISPLAY_RST_PIN,
    DISPLAY_DC_PIN,
    MK_B1_PIN,
    MK_B2_PIN,
    MK_B3_PIN,
    MK_B4_PIN,
    MK_B5_PIN,
    MK_B6_PIN,
    MK_B7_PIN,
    MK_B8_PIN,
    RE_SW_PIN,
    RE_DR_PIN,
    RE_CLK_PIN,
    PSO_PIN,
    fonts_path,
)
from modules.mkeyboard import MKeyboard, MK_B1
from modules.pso import PSO
from modules.rotaryencoder import RotaryEncoder
from modules.SSD1305 import SSD1305
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

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

        pso_input_list = [
            {INPUT_LIST_KEY_INPUT_TYPE: INPUT_TYPE_SWITCH, INPUT_LIST_KEY_PIN_NUMBER: PSO_PIN},
        ]

        display_input_list = [
            {INPUT_LIST_KEY_INPUT_TYPE: INPUT_TYPE_DISPLAY_DC, INPUT_LIST_KEY_PIN_NUMBER: DISPLAY_DC_PIN},
            {INPUT_LIST_KEY_INPUT_TYPE: INPUT_TYPE_DISPLAY_RST, INPUT_LIST_KEY_PIN_NUMBER: DISPLAY_RST_PIN},
        ]

        mkeyboard_input_list = [
            {INPUT_LIST_KEY_INPUT_TYPE: INPUT_TYPE_BUTTON, INPUT_LIST_KEY_PIN_NUMBER: MK_B1_PIN},
            {INPUT_LIST_KEY_INPUT_TYPE: INPUT_TYPE_BUTTON, INPUT_LIST_KEY_PIN_NUMBER: MK_B2_PIN},
            {INPUT_LIST_KEY_INPUT_TYPE: INPUT_TYPE_BUTTON, INPUT_LIST_KEY_PIN_NUMBER: MK_B3_PIN},
            {INPUT_LIST_KEY_INPUT_TYPE: INPUT_TYPE_BUTTON, INPUT_LIST_KEY_PIN_NUMBER: MK_B4_PIN},
            {INPUT_LIST_KEY_INPUT_TYPE: INPUT_TYPE_BUTTON, INPUT_LIST_KEY_PIN_NUMBER: MK_B5_PIN},
            {INPUT_LIST_KEY_INPUT_TYPE: INPUT_TYPE_BUTTON, INPUT_LIST_KEY_PIN_NUMBER: MK_B6_PIN},
            {INPUT_LIST_KEY_INPUT_TYPE: INPUT_TYPE_BUTTON, INPUT_LIST_KEY_PIN_NUMBER: MK_B7_PIN},
            {INPUT_LIST_KEY_INPUT_TYPE: INPUT_TYPE_BUTTON, INPUT_LIST_KEY_PIN_NUMBER: MK_B8_PIN},
        ]

        mode_select_input_list = [
            {INPUT_LIST_KEY_INPUT_TYPE: INPUT_TYPE_BUTTON, INPUT_LIST_KEY_PIN_NUMBER: RE_SW_PIN},
            {INPUT_LIST_KEY_INPUT_TYPE: INPUT_TYPE_ROTARY_ENCODER_DIR, INPUT_LIST_KEY_PIN_NUMBER: RE_DR_PIN},
            {INPUT_LIST_KEY_INPUT_TYPE: INPUT_TYPE_ROTARY_ENCODER_CLK, INPUT_LIST_KEY_PIN_NUMBER: RE_CLK_PIN},
        ]

        self.running = False
        self.power_switch_over = False

        self.font = None
        self.padding = 0
        self.top = 0
        self.bottom = 0
        self.x = 0

        self.pso = PSO(pso_input_list, self.thread_lock, self.input_que)
        self.display = SSD1305(display_input_list, self.thread_lock, self.input_que)
        self.mkeyboard = MKeyboard(mkeyboard_input_list, self.thread_lock, self.input_que)
        self.mode_select_rotary_encoder = RotaryEncoder(mode_select_input_list, self.thread_lock, self.input_que)

    def init(self):
        """
        Initializes all I/O, Peripherals and anything else needed for the device to run

        :return: Nothing
        """
        logging.info("Initializing macro-zero I/O & peripherals")

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.pso.module_init()
        self.display.module_init()
        self.mkeyboard.module_init()
        self.mode_select_rotary_encoder.module_init()

        # Clear display.
        self.display.clear()
        self.display.display()

        # Load font
        self.font = ImageFont.truetype(f"{fonts_path}04B_08__.TTF", 8)
        self.padding = 0
        self.top = self.padding
        self.bottom = self.display.height - self.padding

    def run(self):
        """
        Runs the interface. This function returns when PSO signals that device is shutting down.

        Each loop and entry will be pulled off the Que and processed.

        Based on events keyboards macros/display changes will take place.

        :return: Nothing
        """
        logging.info("Running macro-zero interface")

        self.running = True

        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new("1", (self.display.width, self.display.height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, self.display.width, self.display.height), outline=0, fill=0)

        draw.text((self.x, self.top), "", font=self.font, fill=255)

        # Display image.
        self.display.image(image)
        self.display.display()

        while self.running:
            value = None

            self.thread_lock.acquire()
            try:
                value = self.input_que.get_nowait()
            except queue.Empty:
                pass
            finally:
                self.thread_lock.release()

            if value is not None:
                logging.info(f"Value pulled off Queue - {value}")

                if value == MK_B1:
                    self.mkeyboard.write_report(chr(32) + chr(0) + chr(11) + chr(0) * 5)  # H
                    self.mkeyboard.write_report(chr(0) * 8)  # Release all keys
                    self.mkeyboard.write_report(chr(0) * 2 + chr(8) + chr(0) * 5)  # e
                    self.mkeyboard.write_report(chr(0) * 8)  # Release all keys
                    self.mkeyboard.write_report(chr(0) * 2 + chr(15) + chr(0) * 5)  # l
                    self.mkeyboard.write_report(chr(0) * 8)  # Release all keys
                    self.mkeyboard.write_report(chr(0) * 2 + chr(15) + chr(0) * 5)  # l
                    self.mkeyboard.write_report(chr(0) * 8)  # Release all keys
                    self.mkeyboard.write_report(chr(0) * 2 + chr(18) + chr(0) * 5)  # o
                    self.mkeyboard.write_report(chr(0) * 8)  # Release all keys
                    self.mkeyboard.write_report(chr(32) + chr(0) + chr(30) + chr(0) * 5)  # !
                    self.mkeyboard.write_report(chr(0) * 8)  # Release all keys

    def close(self):
        """
        Closes all modules and resets I/0

        :return:
        """
        logging.info("Closing macro-zero interface")

        self.mode_select_rotary_encoder.module_close()
        self.mkeyboard.module_close()
        self.display.module_close()
        self.pso.module_close()

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
