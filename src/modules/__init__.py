"""
modules
=============

Holds basic properties used by device
"""
import os

try:
    import RPi.GPIO as GPIO  # noqa

    RUNNING_ON_PI = True  # pragma: no cover
except RuntimeError:
    RUNNING_ON_PI = False

INPUT_LIST_KEY_INPUT_TYPE = "InputType"
INPUT_LIST_KEY_PIN_NUMBER = "PinNumber"
INPUT_TYPE_BUTTON = "Button"
INPUT_TYPE_SWITCH = "Switch"
INPUT_TYPE_ROTARY_ENCODER_CLK = "Rotary Encoder Clock"
INPUT_TYPE_ROTARY_ENCODER_DIR = "Rotary Encoder Direction"
INPUT_TYPE_DISPLAY_RST = "Display Reset"
INPUT_TYPE_DISPLAY_DC = "Display Data/Command"

# Pin definition by the board IO
DISPLAY_DC_PIN = 18
DISPLAY_RST_PIN = 22
PSO_PIN = 16
MK_B1_PIN = 29
MK_B2_PIN = 31
MK_B3_PIN = 33
MK_B4_PIN = 35
MK_B5_PIN = 37
MK_B6_PIN = 40
MK_B7_PIN = 38
MK_B8_PIN = 36
RE_SW_PIN = 11
RE_DR_PIN = 15
RE_CLK_PIN = 13

__version__ = "0.015.2"

path = os.path.dirname(__file__)
"""Path to modules package directory."""

# Some other nice fonts to try: http://www.dafont.com/bitmap.php
fonts_path = os.path.join(path, f"fonts{os.sep}")
"""Path to fonts directory."""

configs_path = os.path.join(os.path.dirname(path), f"configs{os.sep}")
"""Path to configs directory"""
