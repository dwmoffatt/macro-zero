"""
modules
=============

Holds basic properties used by device
"""

import os

INPUT_LIST_KEY_INPUT_TYPE = "InputType"
INPUT_LIST_KEY_PIN_NUMBER = "PinNumber"
INPUT_TYPE_BUTTON = "Button"
INPUT_TYPE_SWITCH = "Switch"
INPUT_TYPE_ROTARY_ENCODER_CLK = "Rotary Encoder Clock"
INPUT_TYPE_ROTARY_ENCODER_DIR = "Rotary Encoder Direction"

# Pin definition by the board IO
DC_PIN = 18
RST_PIN = 22
PSO_PIN = 16
MK_B1_PIN = 29
MK_B2_PIN = 31
MK_B3_PIN = 33
MK_B4_PIN = 35
MK_B5_PIN = 37
MK_B6_PIN = 36
MK_B7_PIN = 38
MK_B8_PIN = 40
RE_SW_PIN = 11
RE_DR_PIN = 15
RE_CLK_PIN = 13

__version__ = "0.000.1"

path = os.path.dirname(__file__)
"""Path to StockWatcher package directory."""

fonts_path = os.path.join(path, f"fonts{os.sep}")
"""Path to fonts directory."""
