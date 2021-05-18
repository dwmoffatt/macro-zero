"""
M-Keyboard
"""
import logging
import queue
from . import INPUT_LIST_KEY_PIN_NUMBER, RUNNING_ON_PI

if RUNNING_ON_PI:
    import RPi.GPIO as GPIO


MK_COMMAND_MK_B1 = "MK_B1"
MK_COMMAND_MK_B2 = "MK_B2"
MK_COMMAND_MK_B3 = "MK_B3"
MK_COMMAND_MK_B4 = "MK_B4"
MK_COMMAND_MK_B5 = "MK_B5"
MK_COMMAND_MK_B6 = "MK_B6"
MK_COMMAND_MK_B7 = "MK_B7"
MK_COMMAND_MK_B8 = "MK_B8"

NONE_REPORT = b"\x00\x00\x00\x00\x00\x00\x00\x00"

KEY_MOD_LCTRL = b"\x01"
KEY_MOD_LSHIFT = b"\x02"
KEY_MOD_LALT = b"\x04"
KEY_MOD_LMETA = b"\x08"
KEY_MOD_RCTRL = b"\x10"
KEY_MOD_RSHIFT = b"\x20"
KEY_MOD_RALT = b"\x40"
KEY_MOD_RMETA = b"\x80"

KEY_NONE = b"\x00"
KEY_ERR_OVF = b"\x01"  # Keyboard Error Roll Over - used for all slots if too many keys are pressed ("Phantom key")
# KEY_POST_FAIL = b'\x02'
# KEY_ERR_UND = b'\x03'
KEY_A = b"\x04"
KEY_B = b"\x05"
KEY_C = b"\x06"
KEY_D = b"\x07"
KEY_E = b"\x08"
KEY_F = b"\x09"
KEY_G = b"\x0a"
KEY_H = b"\x0b"
KEY_I = b"\x0c"
KEY_J = b"\x0d"
KEY_K = b"\x0e"
KEY_L = b"\x0f"
KEY_M = b"\x10"
KEY_N = b"\x11"
KEY_O = b"\x12"
KEY_P = b"\x13"
KEY_Q = b"\x14"
KEY_R = b"\x15"
KEY_S = b"\x16"
KEY_T = b"\x17"
KEY_U = b"\x18"
KEY_V = b"\x19"
KEY_W = b"\x1a"
KEY_X = b"\x1b"
KEY_Y = b"\x1c"
KEY_Z = b"\x1d"

KEY_1 = b"\x1e"  # Keyboard 1 and !
KEY_2 = b"\x1f"  # Keyboard 2 and @
KEY_3 = b"\x20"  # Keyboard 3 and #
KEY_4 = b"\x21"  # Keyboard 4 and $
KEY_5 = b"\x22"  # Keyboard 5 and %
KEY_6 = b"\x23"  # Keyboard 6 and ^
KEY_7 = b"\x24"  # Keyboard 7 and &
KEY_8 = b"\x25"  # Keyboard 8 and *
KEY_9 = b"\x26"  # Keyboard 9 and (
KEY_0 = b"\x27"  # Keyboard 0 and )

KEY_ENTER = b"\x28"  # Keyboard Return (ENTER)
KEY_ESC = b"\x29"  # Keyboard ESCAPE
KEY_BACKSPACE = b"\x2a"  # Keyboard DELETE (Backspace)
KEY_TAB = b"\x2b"  # Keyboard Tab
KEY_SPACE = b"\x2c"  # Keyboard Spacebar
KEY_MINUS = b"\x2d"  # Keyboard - and _
KEY_EQUAL = b"\x2e"  # Keyboard = and +
KEY_LEFTBRACE = b"\x2f"  # Keyboard [ and {
KEY_RIGHTBRACE = b"\x30"  # Keyboard ] and }
KEY_BACKSLASH = b"\x31"  # Keyboard \ and |
KEY_HASHTILDE = b"\x32"  # Keyboard Non-US # and ~
KEY_SEMICOLON = b"\x33"  # Keyboard ; and :
KEY_APOSTROPHE = b"\x34"  # Keyboard ' and "
KEY_GRAVE = b"\x35"  # Keyboard ` and ~
KEY_COMMA = b"\x36"  # Keyboard , and <
KEY_DOT = b"\x37"  # Keyboard . and >
KEY_SLASH = b"\x38"  # Keyboard / and ?
KEY_CAPSLOCK = b"\x39"  # Keyboard Caps Lock

KEY_F1 = b"\x3a"  # Keyboard F1
KEY_F2 = b"\x3b"  # Keyboard F2
KEY_F3 = b"\x3c"  # Keyboard F3
KEY_F4 = b"\x3d"  # Keyboard F4
KEY_F5 = b"\x3e"  # Keyboard F5
KEY_F6 = b"\x3f"  # Keyboard F6
KEY_F7 = b"\x40"  # Keyboard F7
KEY_F8 = b"\x41"  # Keyboard F8
KEY_F9 = b"\x42"  # Keyboard F9
KEY_F10 = b"\x43"  # Keyboard F10
KEY_F11 = b"\x44"  # Keyboard F11
KEY_F12 = b"\x45"  # Keyboard F12

KEY_SYSRQ = b"\x46"  # Keyboard Print Screen
KEY_SCROLLLOCK = b"\x47"  # Keyboard Scroll Lock
KEY_PAUSE = b"\x48"  # Keyboard Pause
KEY_INSERT = b"\x49"  # Keyboard Insert
KEY_HOME = b"\x4a"  # Keyboard Home
KEY_PAGEUP = b"\x4b"  # Keyboard Page Up
KEY_DELETE = b"\x4c"  # Keyboard Delete Forward
KEY_END = b"\x4d"  # Keyboard End
KEY_PAGEDOWN = b"\x4e"  # Keyboard Page Down
KEY_RIGHT = b"\x4f"  # Keyboard Right Arrow
KEY_LEFT = b"\x50"  # Keyboard Left Arrow
KEY_DOWN = b"\x51"  # Keyboard Down Arrow
KEY_UP = b"\x52"  # Keyboard Up Arrow

KEY_NUMLOCK = b"\x53"  # Keyboard Num Lock and Clear
KEY_KPSLASH = b"\x54"  # Keypad /
KEY_KPASTERISK = b"\x55"  # Keypad *
KEY_KPMINUS = b"\x56"  # Keypad -
KEY_KPPLUS = b"\x57"  # Keypad +
KEY_KPENTER = b"\x58"  # Keypad ENTER
KEY_KP1 = b"\x59"  # Keypad 1 and End
KEY_KP2 = b"\x5a"  # Keypad 2 and Down Arrow
KEY_KP3 = b"\x5b"  # Keypad 3 and PageDn
KEY_KP4 = b"\x5c"  # Keypad 4 and Left Arrow
KEY_KP5 = b"\x5d"  # Keypad 5
KEY_KP6 = b"\x5e"  # Keypad 6 and Right Arrow
KEY_KP7 = b"\x5f"  # Keypad 7 and Home
KEY_KP8 = b"\x60"  # Keypad 8 and Up Arrow
KEY_KP9 = b"\x61"  # Keypad 9 and Page Up
KEY_KP0 = b"\x62"  # Keypad 0 and Insert
KEY_KPDOT = b"\x63"  # Keypad . and Delete

KEY_102ND = b"\x64"  # Keyboard Non-US \ and |
KEY_COMPOSE = b"\x65"  # Keyboard Application
KEY_POWER = b"\x66"  # Keyboard Power
KEY_KPEQUAL = b"\x67"  # Keypad =

KEY_F13 = b"\x68"  # Keyboard F13
KEY_F14 = b"\x69"  # Keyboard F14
KEY_F15 = b"\x6a"  # Keyboard F15
KEY_F16 = b"\x6b"  # Keyboard F16
KEY_F17 = b"\x6c"  # Keyboard F17
KEY_F18 = b"\x6d"  # Keyboard F18
KEY_F19 = b"\x6e"  # Keyboard F19
KEY_F20 = b"\x6f"  # Keyboard F20
KEY_F21 = b"\x70"  # Keyboard F21
KEY_F22 = b"\x71"  # Keyboard F22
KEY_F23 = b"\x72"  # Keyboard F23
KEY_F24 = b"\x73"  # Keyboard F24

KEY_OPEN = b"\x74"  # Keyboard Execute
KEY_HELP = b"\x75"  # Keyboard Help
KEY_PROPS = b"\x76"  # Keyboard Menu
KEY_FRONT = b"\x77"  # Keyboard Select
KEY_STOP = b"\x78"  # Keyboard Stop
KEY_AGAIN = b"\x79"  # Keyboard Again
KEY_UNDO = b"\x7a"  # Keyboard Undo
KEY_CUT = b"\x7b"  # Keyboard Cut
KEY_COPY = b"\x7c"  # Keyboard Copy
KEY_PASTE = b"\x7d"  # Keyboard Paste
KEY_FIND = b"\x7e"  # Keyboard Find
KEY_MUTE = b"\x7f"  # Keyboard Mute
KEY_VOLUMEUP = b"\x80"  # Keyboard Volume Up
KEY_VOLUMEDOWN = b"\x81"  # Keyboard Volume Down

KEY_LEFTCTRL = b"\xe0"  # Keyboard Left Control
KEY_LEFTSHIFT = b"\xe1"  # Keyboard Left Shift
KEY_LEFTALT = b"\xe2"  # Keyboard Left Alt
KEY_LEFTMETA = b"\xe3"  # Keyboard Left GUI
KEY_RIGHTCTRL = b"\xe4"  # Keyboard Right Control
KEY_RIGHTSHIFT = b"\xe5"  # Keyboard Right Shift
KEY_RIGHTALT = b"\xe6"  # Keyboard Right Alt
KEY_RIGHTMETA = b"\xe7"  # Keyboard Right GUI

KEY_MEDIA_PLAYPAUSE = b"\xe8"
KEY_MEDIA_STOPCD = b"\xe9"
KEY_MEDIA_PREVIOUSSONG = b"\xea"
KEY_MEDIA_NEXTSONG = b"\xeb"
KEY_MEDIA_EJECTCD = b"\xec"
KEY_MEDIA_VOLUMEUP = b"\xed"
KEY_MEDIA_VOLUMEDOWN = b"\xee"
KEY_MEDIA_MUTE = b"\xef"
KEY_MEDIA_WWW = b"\xf0"
KEY_MEDIA_BACK = b"\xf1"
KEY_MEDIA_FORWARD = b"\xf2"
KEY_MEDIA_STOP = b"\xf3"
KEY_MEDIA_FIND = b"\xf4"
KEY_MEDIA_SCROLLUP = b"\xf5"
KEY_MEDIA_SCROLLDOWN = b"\xf6"
KEY_MEDIA_EDIT = b"\xf7"
KEY_MEDIA_SLEEP = b"\xf8"
KEY_MEDIA_COFFEE = b"\xf9"
KEY_MEDIA_REFRESH = b"\xfa"
KEY_MEDIA_CALC = b"\xfb"

MODIFIER_LOOKUP = [
    KEY_NONE,
    KEY_MOD_LCTRL,
    KEY_MOD_LSHIFT,
    KEY_MOD_LALT,
    KEY_MOD_LMETA,
    KEY_MOD_RCTRL,
    KEY_MOD_RSHIFT,
    KEY_MOD_RALT,
    KEY_MOD_RMETA,
]

MODIFIER_NEEDED = [
    "!",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "(",
    ")",
]

SCAN_CODE_LOOKUP = {
    " ": KEY_SPACE,
    "a": KEY_A,
    "b": KEY_B,
    "c": KEY_C,
    "d": KEY_D,
    "e": KEY_E,
    "f": KEY_F,
    "g": KEY_G,
    "h": KEY_H,
    "i": KEY_I,
    "j": KEY_J,
    "k": KEY_K,
    "l": KEY_L,
    "m": KEY_M,
    "n": KEY_N,
    "o": KEY_O,
    "p": KEY_P,
    "q": KEY_Q,
    "r": KEY_R,
    "s": KEY_S,
    "t": KEY_T,
    "u": KEY_U,
    "v": KEY_V,
    "w": KEY_W,
    "x": KEY_X,
    "y": KEY_Y,
    "z": KEY_Z,
    "1": KEY_1,
    "2": KEY_2,
    "3": KEY_3,
    "4": KEY_4,
    "5": KEY_5,
    "6": KEY_6,
    "7": KEY_7,
    "8": KEY_8,
    "9": KEY_9,
    "0": KEY_0,
    "!": KEY_1,
    "@": KEY_2,
    "#": KEY_3,
    "$": KEY_4,
    "%": KEY_5,
    "^": KEY_6,
    "&": KEY_7,
    "*": KEY_8,
    "(": KEY_8,
    ")": KEY_0,
    "F1": KEY_F1,
    "F2": KEY_F2,
    "F3": KEY_F3,
    "F4": KEY_F4,
    "F5": KEY_F5,
    "F6": KEY_F6,
    "F7": KEY_F7,
    "F8": KEY_F8,
    "F9": KEY_F9,
    "F10": KEY_F10,
    "F11": KEY_F11,
    "F12": KEY_F12,
    "Enter": KEY_ENTER,
}


class MKeyboard:
    def __init__(self, input_list=None, thread_lock=None, que=None):
        self._input_list = input_list
        self._thread_lock = thread_lock
        self._que = que

    def module_init(self):
        logging.info("Initializing mKeyboard Module")

        # Setup I/O as Inputs Pull Up & attach events to RISING edge of I/O
        for i in range(0, len(self._input_list)):
            GPIO.setup(self._input_list[i][INPUT_LIST_KEY_PIN_NUMBER], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(
                self._input_list[i][INPUT_LIST_KEY_PIN_NUMBER], GPIO.RISING, callback=self.btn_release, bouncetime=200
            )

    def module_close(self):
        logging.info("Closing mKeyboard Module")

        # De-attach events from I/O
        for i in range(0, len(self._input_list)):
            GPIO.remove_event_detect(self._input_list[i][INPUT_LIST_KEY_PIN_NUMBER])

    def btn_release(self, channel):
        button = 0
        for i in range(0, len(self._input_list)):
            if self._input_list[i][INPUT_LIST_KEY_PIN_NUMBER] == channel:
                button = i + 1

        logging.info(f"mKeyboard Button {button} released")

        self._thread_lock.acquire()
        try:
            self._que.put_nowait(f"MK_B{button}")
        except queue.Full:
            logging.exception(f"Que is full when adding MK_B{button}")
        finally:
            self._thread_lock.release()

    def build_report(self, value):
        """
        Generate byte report for given value

        :param value: the value we want to convert into a report
        :return report: byte report for given value
        """
        is_upper = False

        if value is None:
            return NONE_REPORT

        # Check if modifier is needed
        if value in MODIFIER_NEEDED:
            report = KEY_MOD_LSHIFT
        elif len(value) == 1 and value.isalpha() and value.isupper():
            report = KEY_MOD_LSHIFT
            is_upper = True
        else:
            report = KEY_NONE

        report += KEY_NONE

        if is_upper:
            report += SCAN_CODE_LOOKUP.get(value.lower()) + (KEY_NONE * 5)
        else:
            report += SCAN_CODE_LOOKUP.get(value) + (KEY_NONE * 5)

        self._verify_report(report)

        return report

    @staticmethod
    def _verify_report(report):
        """
        Verify that a report is the correct format

        First byte is modifier
        Second Byte is reserved, always = b"\x00
        Next 6 Bytes are scan codes, = b"\x00 is no key press

        ex. b"\x02\x00\x04\x00\x00\x00\x00\x00" = A

        :param report: bytes
        :return: True on successful report verification or throws Exception
        """
        # Verify length of bytes
        if len(report) != 8:
            raise ValueError("Report needs to be 8 bytes long")

        # Check first byte is an accepted modifier
        if report[0:1] not in MODIFIER_LOOKUP:
            raise ValueError("First byte in report needs to be accepted modified")

        # Check second byte is x00
        if report[1:2] != KEY_NONE:
            raise ValueError("Second byte in report needs to be x00")

        return True

    def write_report(self, report):
        """
        Writes key report to USB Device

        First byte is modifier
        Second Byte is reserved, always = b"\x00
        Next 6 Bytes are scan codes, = b"\x00 is no key press

        ex. b"\x02\x00\x04\x00\x00\x00\x00\x00" = A

        :param report: a bytes
        :return:
        """
        self._verify_report(report)

        with open("/dev/hidg0", "rb+") as fd:
            fd.write(report)
