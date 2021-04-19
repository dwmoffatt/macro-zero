"""
Macro-Zero Interface
==========================

Main Control for Device
"""

import os

# import argparse
import threading
import logging
import queue
import copy
import json
import time
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
    configs_path,
)
from modules.mkeyboard import (
    MKeyboard,
    MK_COMMAND_MK_B1,
    MK_COMMAND_MK_B2,
    MK_COMMAND_MK_B3,
    MK_COMMAND_MK_B4,
    MK_COMMAND_MK_B5,
    MK_COMMAND_MK_B6,
    MK_COMMAND_MK_B7,
    MK_COMMAND_MK_B8,
)
from modules.pso import PSO, PSO_COMMAND_PSO
from modules.rotaryencoder import RotaryEncoder, RE_COMMAND_RE_B1, RE_COMMAND_RE_CW, RE_COMMAND_RE_CCW
from modules.SSD1305 import SSD1305
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

logging.basicConfig(
    filename="macro_zero.log", format="[%(asctime)s][%(levelname)s] - %(message)s", filemode="w", level=logging.DEBUG
)

CONFIGURATION_FILENAME = "macro-zero configuration.json"
DEFAULT_CONFIGURATION_FILENAME = "macro-zero default configuration.json"
DEVICE_TITLE = "Macro-Zero"

CONFIGURATION_KEY_B1 = "B1"
CONFIGURATION_KEY_B2 = "B2"
CONFIGURATION_KEY_B3 = "B3"
CONFIGURATION_KEY_B4 = "B4"
CONFIGURATION_KEY_B5 = "B5"
CONFIGURATION_KEY_B6 = "B6"
CONFIGURATION_KEY_B7 = "B7"
CONFIGURATION_KEY_B8 = "B8"
CONFIGURATION_KEY_COMMAND_NAME = "CommandName"
CONFIGURATION_KEY_COMMAND_INTERVAL = "CommandInterval"
CONFIGURATION_KEY_COMMANDS = "Commands"


class MacroZero:
    def __init__(self):
        """
        Creates Macro-Zero Device Object
        """
        self.thread_lock = threading.Lock()
        self.input_que = queue.Queue(maxsize=50)

        self.running = False
        self.power_switch_over = False
        self.current_mode = (0, "")  # No mode, config not loaded
        self.mode_list = list()
        self.command_dictionary = None
        self.configuration = None

        self.current_image = None
        self.font_8 = None
        self.padding = 0
        self.top = 0
        self.bottom = 0

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

        self.build_command_dictionary()
        self.load_configuration()

        # Load font
        self.font_8 = ImageFont.truetype(f"{fonts_path}The Impostor.ttf", 8)
        self.padding = 0
        self.top = self.padding
        self.bottom = self.display.height - self.padding

        # Clear display.
        self.display.clear()
        self.display.display()

    def run(self):
        """
        Runs the interface. This function returns when PSO signals that device is shutting down.

        Each loop and entry will be pulled off the Que and processed.

        Based on events keyboards macros/display changes will take place.

        :return: Nothing
        """
        logging.info("Running macro-zero interface")

        title_font = ImageFont.truetype(f"{fonts_path}Gamer.ttf", 32)

        self.running = True

        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new("1", (self.display.width, self.display.height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, self.display.width, self.display.height), outline=0, fill=0)

        text_size = draw.textsize(DEVICE_TITLE, font=title_font)
        offset_x = int((self.display.width - text_size[0]) / 2)
        if offset_x < 0:
            offset_x = 0
        draw.text((offset_x, self.top), DEVICE_TITLE, font=title_font, fill=255)

        self.current_image = image

        # Display image.
        self.display.image(self.current_image)
        self.display.display()

        time.sleep(2.5)

        # display current mode
        self.display_mode_selection(self.current_mode[1])

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

                try:
                    self.command_dictionary.get(value, self._invalid_command)()
                except ValueError:
                    logging.exception(f"Last Command - {value}")

            if self.power_switch_over:
                self.running = False

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

    def load_configuration(self):
        """
        Try to load custom config file is present, if not present then try to load default config.

        If default is not present then throw exception

        :return:
        """
        config_loaded = False
        current_configuration = copy.deepcopy(self.configuration)

        try:
            with open(f"{configs_path}{CONFIGURATION_FILENAME}") as file:
                self.configuration = json.load(file)
            config_loaded = True
        except FileNotFoundError:
            logging.debug(f"No custom button config under {CONFIGURATION_FILENAME} filename found")

        if not config_loaded:
            try:
                with open(f"{configs_path}{DEFAULT_CONFIGURATION_FILENAME}") as file:
                    self.configuration = json.load(file)
                # config_loaded = True
            except FileNotFoundError:
                logging.exception(f"No default config file found - {DEFAULT_CONFIGURATION_FILENAME}")

        # If the config has changed, verify its new contents
        if current_configuration != self.configuration:
            self.mode_list = list(self.configuration.keys())

            # TODO: Verify Configuration

            self.current_mode = (1, self.mode_list[0])

    def display_mode_selection(self, mode):
        """

        :param mode:
        :return:
        """

        if mode not in self.mode_list:
            logging.debug(f"Chosen mode to display - {mode} - is not part of mode_list - {self.mode_list}")
        else:
            # Make sure to create image with mode '1' for 1-bit color.
            image = Image.new("1", (self.display.width, self.display.height))
            # Get drawing object to draw on image.
            draw = ImageDraw.Draw(image)

            # Draw a black filled box to clear the image.
            draw.rectangle((0, 0, self.display.width, self.display.height), outline=0, fill=0)

            draw.line(
                [((self.display.width / 2) - 1, 2), ((self.display.width / 2) - 1, self.bottom - 2)], fill=128, width=2
            )

            draw.text(
                (1, self.top),
                f"B1: {self.configuration[mode][CONFIGURATION_KEY_B1][CONFIGURATION_KEY_COMMAND_NAME]}",
                font=self.font_8,
                fill=255,
            )
            draw.text(
                (1, self.top + (8 * 1)),
                f"B3: {self.configuration[mode][CONFIGURATION_KEY_B3][CONFIGURATION_KEY_COMMAND_NAME]}",
                font=self.font_8,
                fill=255,
            )
            draw.text(
                (1, self.top + (8 * 2)),
                f"B5: {self.configuration[mode][CONFIGURATION_KEY_B5][CONFIGURATION_KEY_COMMAND_NAME]}",
                font=self.font_8,
                fill=255,
            )
            draw.text(
                (1, self.top + (8 * 3)),
                f"B7: {self.configuration[mode][CONFIGURATION_KEY_B7][CONFIGURATION_KEY_COMMAND_NAME]}",
                font=self.font_8,
                fill=255,
            )

            draw.text(
                ((self.display.width / 2) + 2, self.top),
                f"B2: {self.configuration[mode][CONFIGURATION_KEY_B2][CONFIGURATION_KEY_COMMAND_NAME]}",
                font=self.font_8,
                fill=255,
            )
            draw.text(
                ((self.display.width / 2) + 2, self.top + (8 * 1)),
                f"B4: {self.configuration[mode][CONFIGURATION_KEY_B4][CONFIGURATION_KEY_COMMAND_NAME]}",
                font=self.font_8,
                fill=255,
            )
            draw.text(
                ((self.display.width / 2) + 2, self.top + (8 * 2)),
                f"B6: {self.configuration[mode][CONFIGURATION_KEY_B6][CONFIGURATION_KEY_COMMAND_NAME]}",
                font=self.font_8,
                fill=255,
            )
            draw.text(
                ((self.display.width / 2) + 2, self.top + (8 * 3)),
                f"B8: {self.configuration[mode][CONFIGURATION_KEY_B8][CONFIGURATION_KEY_COMMAND_NAME]}",
                font=self.font_8,
                fill=255,
            )

            self.current_image = image

            # Display image.
            self.display.image(self.current_image)
            self.display.display()

    def _process_pso(self):
        """
        Process PSO Command

        :return:
        """
        logging.debug("Processing PSO Command")

        self.power_switch_over = True

    def _process_mk_b1(self):
        """
        Process MK_B1 Command

        :return:
        """
        logging.debug("Processing MK_B1 Command")

        # self.mkeyboard.write_report(chr(32) + chr(0) + chr(11) + chr(0) * 5)  # H
        # self.mkeyboard.write_report(chr(0) * 8)  # Release all keys
        # self.mkeyboard.write_report(chr(0) * 2 + chr(8) + chr(0) * 5)  # e
        # self.mkeyboard.write_report(chr(0) * 8)  # Release all keys
        # self.mkeyboard.write_report(chr(0) * 2 + chr(15) + chr(0) * 5)  # l
        # self.mkeyboard.write_report(chr(0) * 8)  # Release all keys
        # self.mkeyboard.write_report(chr(0) * 2 + chr(15) + chr(0) * 5)  # l
        # self.mkeyboard.write_report(chr(0) * 8)  # Release all keys
        # self.mkeyboard.write_report(chr(0) * 2 + chr(18) + chr(0) * 5)  # o
        # self.mkeyboard.write_report(chr(0) * 8)  # Release all keys
        # self.mkeyboard.write_report(chr(32) + chr(0) + chr(30) + chr(0) * 5)  # !
        # self.mkeyboard.write_report(chr(0) * 8)  # Release all keys

    def _process_mk_b2(self):
        """
        Process MK_B2 Command

        :return:
        """
        logging.debug("Processing MK_B2 Command")

    def _process_mk_b3(self):
        """
        Process MK_B3 Command

        :return:
        """
        logging.debug("Processing MK_B3 Command")

    def _process_mk_b4(self):
        """
        Process MK_B4 Command

        :return:
        """
        logging.debug("Processing MK_B4 Command")

    def _process_mk_b5(self):
        """
        Process MK_B5 Command

        :return:
        """
        logging.debug("Processing MK_B5 Command")

    def _process_mk_b6(self):
        """
        Process MK_B6 Command

        :return:
        """
        logging.debug("Processing MK_B6 Command")

    def _process_mk_b7(self):
        """
        Process MK_B7 Command

        :return:
        """
        logging.debug("Processing MK_B7 Command")

    def _process_mk_b8(self):
        """
        Process MK_B8 Command

        :return:
        """
        logging.debug("Processing MK_B8 Command")

    def _process_re_b1(self):
        """
        Process RE_B1 Command

        :return:
        """
        logging.debug("Processing RE_B1 Command")

    def _process_re_cw(self):
        """
        Process RE_CW Command

        :return:
        """
        logging.debug("Processing RE_CW Command")

    def _process_re_ccw(self):
        """
        Process RE_CCW Command

        :return:
        """
        logging.debug("Processing RE_CCW Command")

    def _invalid_command(self):
        raise ValueError("Invalid Command")

    def build_command_dictionary(self):
        self.command_dictionary = {
            PSO_COMMAND_PSO: self._process_pso,
            MK_COMMAND_MK_B1: self._process_mk_b1,
            MK_COMMAND_MK_B2: self._process_mk_b2,
            MK_COMMAND_MK_B3: self._process_mk_b3,
            MK_COMMAND_MK_B4: self._process_mk_b4,
            MK_COMMAND_MK_B5: self._process_mk_b5,
            MK_COMMAND_MK_B6: self._process_mk_b6,
            MK_COMMAND_MK_B7: self._process_mk_b7,
            MK_COMMAND_MK_B8: self._process_mk_b8,
            RE_COMMAND_RE_B1: self._process_re_b1,
            RE_COMMAND_RE_CW: self._process_re_cw,
            RE_COMMAND_RE_CCW: self._process_re_ccw,
        }


if __name__ in "__main__":

    macro_zero = None

    try:
        # parser = argparse.ArgumentParser()
        # parser.add_argument(
        #    "--testimage",
        #    "-ti",
        #    help="Test Image Level 0,1,2,3",
        #    default=0,
        #    const=0,
        #    nargs="?",
        #    type=int,
        #    choices=list(range(0, 4)),
        # )
        # args = parser.parse_args()

        macro_zero = MacroZero()

        macro_zero.init()

        macro_zero.run()

    except Exception:
        logging.exception("MacroZero Crashed!!!!!")

    macro_zero.close()
