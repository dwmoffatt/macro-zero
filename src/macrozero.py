"""
Macro-Zero Interface
==========================

Main Control for Device
"""

# import argparse
import os
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
    RUNNING_ON_PI,
    STATUS_OK,
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
from modules.RGBDriver import RGBDriver, BANK_A, BANK_B
from backend.api import API
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from smbus2 import SMBus

if RUNNING_ON_PI:
    import RPi.GPIO as GPIO

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
CONFIGURATION_KEY_TYPE = "Type"
CONFIGURATION_KEY_COMMAND = "Command"
CONFIGURATION_KEY_LEDS = "LEDs"
CONFIGURATION_KEY_LED1 = "LED1"
CONFIGURATION_KEY_LED2 = "LED2"
CONFIGURATION_KEY_LED3 = "LED3"
CONFIGURATION_KEY_LED4 = "LED4"

CONFIGURATION_TYPE_COMMAND_STRING = "Command String"
CONFIGURATION_TYPE_KEYBOARD_FUNCTION = "Keyboard Function"

ROTARY_ENCODER_MODES = "Modes"
ROTARY_ENCODER_BUTTONS = "Buttons"

BUTTONS_INDEXES_MIN = 1
BUTTONS_INDEXES_MAX = 8

CONFIG_MODES_MIN = 1


class MacroZero:
    def __init__(self, test_env=False, run_webserver=True):
        """
        Creates Macro-Zero Device Object
        """

        if test_env is False:
            logging.basicConfig(
                filename="macro_zero.log",
                format="[%(asctime)s][%(levelname)s] - %(message)s",
                filemode="w",
                level=logging.DEBUG,
            )

        self._run_webserver = run_webserver

        self.i2c_bus = None
        if RUNNING_ON_PI:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            self.i2c_bus = SMBus(1)

        self.thread_lock = threading.Lock()
        self.input_que = queue.Queue(maxsize=50)

        self.running = False
        self.power_switch_over = False
        self.current_mode = (0, "")  # No mode, config not loaded
        self.buttons_display_indexes = (1, 3)  # Default buttons to display
        self.mode_list = list()
        self.command_dictionary = None
        self.configuration = None
        self.rotary_encoder_mode = ROTARY_ENCODER_BUTTONS

        self.current_image = None
        self.font = None
        self.font_size = 5
        self.padding = 0
        self.top = 0
        self.bottom = 0

        self._update_display = False
        self._update_leds = False
        self._config_modes_max = 0

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
        self.rgb_driver = RGBDriver([], self.thread_lock, self.input_que, i2c_bus=self.i2c_bus)
        self.api = API()

    def init(self):
        """
        Initializes all I/O, Peripherals and anything else needed for the device to run

        :return: Nothing
        """
        logging.info("Initializing macro-zero I/O & peripherals")

        self.pso.module_init()
        self.display.module_init()
        self.mkeyboard.module_init()
        self.mode_select_rotary_encoder.module_init()
        self.rgb_driver.module_init()

        self.command_dictionary = self.build_command_dictionary()
        self.load_configuration()

        # Load font
        self.font = ImageFont.truetype(f"{fonts_path}All Square Now.otf", self.font_size)
        self.padding = 0
        self.top = self.padding
        self.bottom = self.display.height - self.padding

        # Clear display.
        self.display.clear()
        self.display.display()

        return True

    def run(self):
        """
        Runs the interface. This function returns when PSO signals that device is shutting down.

        Each loop and entry will be pulled off the Que and processed.

        Based on events keyboards macros/display changes will take place.

        :return: Nothing
        """
        logging.info("Running macro-zero interface")

        if self._run_webserver:
            t = threading.Thread(target=self.api.run_api, name="APIThread")
            t.start()

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

        # turn on LEDs associated with the current mode
        self.update_leds_based_on_mode(self.current_mode[1])
        self.rgb_driver.write_output_banks()

        # This is the main running loop for the program
        while self.running:
            value = None

            # Acquire thread lock and pull value off the que
            self.thread_lock.acquire()
            try:
                value = self.input_que.get_nowait()
            except queue.Empty:
                pass
            finally:
                self.thread_lock.release()

            # Process the value if there was one
            if value is not None:
                logging.info(f"Value pulled off Queue - {value}")

                # Run function for specific command
                try:
                    self.command_dictionary.get(value, self._invalid_command)()
                except ValueError:
                    logging.exception(f"Last Command - {value}")

            # Update Display
            if self._update_display:
                self.display_mode_selection(self.current_mode[1])
                self._update_display = False

            # Update LEDs
            if self._update_leds:
                self.update_leds_based_on_mode(self.current_mode[1])
                self.rgb_driver.write_output_banks()
                self._update_leds = False

            # Check Power Switch Over Input
            if self.power_switch_over:
                self.running = False

    def close(self):
        """
        Closes all modules and resets I/0

        :return: Nothing
        """
        logging.info("Closing macro-zero interface")

        self.rgb_driver.module_close()
        self.mode_select_rotary_encoder.module_close()
        self.mkeyboard.module_close()
        self.display.module_close()
        self.pso.module_close()

        self.i2c_bus.close()

        GPIO.cleanup()

        for client_thread in threading.enumerate():
            if client_thread is threading.main_thread():
                continue
            client_thread.join(1)

        if self.power_switch_over:
            logging.info("System shutdown started!")
            os.system("systemctl poweroff")

        return True

    def load_configuration(self):
        """
        Try to load custom config file is present, if not present then try to load default config.

        If default is not present then throw exception

        :return: Nothing
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

            self._config_modes_max = len(self.mode_list)
            self.current_mode = (1, self.mode_list[0])
            self.buttons_display_indexes = (1, 3)

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

            mode_size = draw.textsize(mode, font=self.font)
            offset_x = int((self.display.width - mode_size[0]) / 2)
            if offset_x < 0:
                offset_x = 0
            draw.text((offset_x, self.top), mode, font=self.font, fill=255)

            draw.line([(0, mode_size[1]), (self.display.width, mode_size[1])], fill=255, width=1)
            selection_offset = mode_size[1] + 1
            spacer = 1

            position = 1
            for i in range(self.buttons_display_indexes[0], self.buttons_display_indexes[1] + 1):
                draw.text(
                    (0, selection_offset + (spacer * position) + (mode_size[1] * (position - 1))),
                    f"B{i}: {self.configuration[mode][f'B{i}'][CONFIGURATION_KEY_COMMAND_NAME]}",
                    font=self.font,
                    fill=255,
                )
                position += 1

            self.current_image = image

            # Display image.
            self.display.image(self.current_image)
            self.display.display()

    def build_report_list(self, command):
        """
        Build report_list for given command.

        :param command: Command dictionary from config
        ex. Command = {
            "Type": "Keyboard Function"
            "Command": "Enter"
        :return report_list: list of reports needed to send command
        """
        report_list = list()

        if command[CONFIGURATION_KEY_TYPE] == CONFIGURATION_TYPE_COMMAND_STRING:
            for char in command[CONFIGURATION_KEY_COMMAND]:
                report_list.append(self.mkeyboard.build_report(char))
                report_list.append(self.mkeyboard.build_report(None))
        elif command[CONFIGURATION_KEY_TYPE] == CONFIGURATION_TYPE_KEYBOARD_FUNCTION:
            report_list.append(self.mkeyboard.build_report(command[CONFIGURATION_KEY_COMMAND]))
            report_list.append(self.mkeyboard.build_report(None))

        return report_list

    def _process_pso(self):
        """
        Process PSO Command

        :return status: OK
        """
        status = STATUS_OK

        logging.debug("Processing PSO Command")

        self.power_switch_over = True

        return status

    def _process_mk_b1(self):
        """
        Process MK_B1 Command

        :return:
        """
        logging.debug("Processing MK_B1 Command")

        commands = self.configuration[self.current_mode[1]][CONFIGURATION_KEY_B1][CONFIGURATION_KEY_COMMANDS]
        for command in commands:
            report_list = self.build_report_list(command)

            for report in report_list:
                self.mkeyboard.write_report(report)

            time.sleep(
                self.configuration[self.current_mode[1]][CONFIGURATION_KEY_B1][CONFIGURATION_KEY_COMMAND_INTERVAL]
            )

        return True

    def _process_mk_b2(self):
        """
        Process MK_B2 Command

        :return:
        """
        logging.debug("Processing MK_B2 Command")

        commands = self.configuration[self.current_mode[1]][CONFIGURATION_KEY_B2][CONFIGURATION_KEY_COMMANDS]
        for command in commands:
            report_list = self.build_report_list(command)

            for report in report_list:
                self.mkeyboard.write_report(report)

            time.sleep(
                self.configuration[self.current_mode[1]][CONFIGURATION_KEY_B2][CONFIGURATION_KEY_COMMAND_INTERVAL]
            )

        return True

    def _process_mk_b3(self):
        """
        Process MK_B3 Command

        :return:
        """
        logging.debug("Processing MK_B3 Command")

        commands = self.configuration[self.current_mode[1]][CONFIGURATION_KEY_B3][CONFIGURATION_KEY_COMMANDS]
        for command in commands:
            report_list = self.build_report_list(command)

            for report in report_list:
                self.mkeyboard.write_report(report)

            time.sleep(
                self.configuration[self.current_mode[1]][CONFIGURATION_KEY_B3][CONFIGURATION_KEY_COMMAND_INTERVAL]
            )

        return True

    def _process_mk_b4(self):
        """
        Process MK_B4 Command

        :return:
        """
        logging.debug("Processing MK_B4 Command")

        commands = self.configuration[self.current_mode[1]][CONFIGURATION_KEY_B4][CONFIGURATION_KEY_COMMANDS]
        for command in commands:
            report_list = self.build_report_list(command)

            for report in report_list:
                self.mkeyboard.write_report(report)

            time.sleep(
                self.configuration[self.current_mode[1]][CONFIGURATION_KEY_B4][CONFIGURATION_KEY_COMMAND_INTERVAL]
            )

        return True

    def _process_mk_b5(self):
        """
        Process MK_B5 Command

        :return:
        """
        logging.debug("Processing MK_B5 Command")

        commands = self.configuration[self.current_mode[1]][CONFIGURATION_KEY_B5][CONFIGURATION_KEY_COMMANDS]
        for command in commands:
            report_list = self.build_report_list(command)

            for report in report_list:
                self.mkeyboard.write_report(report)

            time.sleep(
                self.configuration[self.current_mode[1]][CONFIGURATION_KEY_B5][CONFIGURATION_KEY_COMMAND_INTERVAL]
            )

        return True

    def _process_mk_b6(self):
        """
        Process MK_B6 Command

        :return:
        """
        logging.debug("Processing MK_B6 Command")

        commands = self.configuration[self.current_mode[1]][CONFIGURATION_KEY_B6][CONFIGURATION_KEY_COMMANDS]
        for command in commands:
            report_list = self.build_report_list(command)

            for report in report_list:
                self.mkeyboard.write_report(report)

            time.sleep(
                self.configuration[self.current_mode[1]][CONFIGURATION_KEY_B6][CONFIGURATION_KEY_COMMAND_INTERVAL]
            )

        return True

    def _process_mk_b7(self):
        """
        Process MK_B7 Command

        :return:
        """
        logging.debug("Processing MK_B7 Command")

        commands = self.configuration[self.current_mode[1]][CONFIGURATION_KEY_B7][CONFIGURATION_KEY_COMMANDS]
        for command in commands:
            report_list = self.build_report_list(command)

            for report in report_list:
                self.mkeyboard.write_report(report)

            time.sleep(
                self.configuration[self.current_mode[1]][CONFIGURATION_KEY_B7][CONFIGURATION_KEY_COMMAND_INTERVAL]
            )

        return True

    def _process_mk_b8(self):
        """
        Process MK_B8 Command

        :return:
        """
        logging.debug("Processing MK_B8 Command")

        commands = self.configuration[self.current_mode[1]][CONFIGURATION_KEY_B8][CONFIGURATION_KEY_COMMANDS]
        for command in commands:
            report_list = self.build_report_list(command)

            for report in report_list:
                self.mkeyboard.write_report(report)

            time.sleep(
                self.configuration[self.current_mode[1]][CONFIGURATION_KEY_B8][CONFIGURATION_KEY_COMMAND_INTERVAL]
            )

        return True

    def _process_re_b1(self):
        """
        Process RE_B1 Command

        :return:
        """
        status = STATUS_OK

        logging.debug("Processing RE_B1 Command")

        if self.rotary_encoder_mode == ROTARY_ENCODER_BUTTONS:
            self.rotary_encoder_mode = ROTARY_ENCODER_MODES
        elif self.rotary_encoder_mode == ROTARY_ENCODER_MODES:
            self.rotary_encoder_mode = ROTARY_ENCODER_BUTTONS

        return status

    def _process_re_cw(self):
        """
        Process RE_CW Command

        :return:
        """
        logging.debug("Processing RE_CW Command")

        if self.rotary_encoder_mode == ROTARY_ENCODER_MODES:
            value = self.current_mode[0]
            value += 1

            if value > self._config_modes_max:
                self.current_mode = (self._config_modes_max, self.mode_list[self._config_modes_max - 1])
            else:
                self.current_mode = (value, self.mode_list[value - 1])

            self._update_leds = True

        elif self.rotary_encoder_mode == ROTARY_ENCODER_BUTTONS:
            outer_value = self.buttons_display_indexes[1]
            outer_value += 1

            if outer_value > BUTTONS_INDEXES_MAX:
                self.buttons_display_indexes = (BUTTONS_INDEXES_MAX - 2, BUTTONS_INDEXES_MAX)
            else:
                self.buttons_display_indexes = (outer_value - 2, outer_value)

        self._update_display = True

        return True

    def _process_re_ccw(self):
        """
        Process RE_CCW Command

        :return:
        """
        logging.debug("Processing RE_CCW Command")

        if self.rotary_encoder_mode == ROTARY_ENCODER_MODES:
            value = self.current_mode[0]
            value -= 1

            if value < CONFIG_MODES_MIN:
                self.current_mode = (CONFIG_MODES_MIN, self.mode_list[CONFIG_MODES_MIN - 1])
            else:
                self.current_mode = (value, self.mode_list[value - 1])

            self._update_leds = True

        elif self.rotary_encoder_mode == ROTARY_ENCODER_BUTTONS:
            inner_value = self.buttons_display_indexes[0]
            inner_value -= 1

            if inner_value < BUTTONS_INDEXES_MIN:
                self.buttons_display_indexes = (BUTTONS_INDEXES_MIN, BUTTONS_INDEXES_MIN + 2)
            else:
                self.buttons_display_indexes = (inner_value, inner_value + 2)

        self._update_display = True

        return True

    def _invalid_command(self):
        raise ValueError("Invalid Command")

    def build_command_dictionary(self):
        return {
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

    def update_leds_based_on_mode(self, mode):

        if mode not in self.mode_list:
            logging.debug(f"Chosen mode for LED update - {mode} - is not part of mode_list - {self.mode_list}")
        else:
            # Update LED output mappings and output banks
            self.rgb_driver.set_output_mappings(
                self.configuration[mode][CONFIGURATION_KEY_LEDS][CONFIGURATION_KEY_LED1], 1
            )
            self.rgb_driver.set_output_mappings(
                self.configuration[mode][CONFIGURATION_KEY_LEDS][CONFIGURATION_KEY_LED2], 2
            )
            self.rgb_driver.set_output_mappings(
                self.configuration[mode][CONFIGURATION_KEY_LEDS][CONFIGURATION_KEY_LED3], 3
            )
            self.rgb_driver.set_output_mappings(
                self.configuration[mode][CONFIGURATION_KEY_LEDS][CONFIGURATION_KEY_LED4], 4
            )
            self.rgb_driver.output_bank_a = self.rgb_driver.build_output_bank(BANK_A)
            self.rgb_driver.output_bank_b = self.rgb_driver.build_output_bank(BANK_B)


if __name__ in "__main__":  # pragma: no cover

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
