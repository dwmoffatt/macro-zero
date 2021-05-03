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

SCAN_CODE_LOOKUP = {
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

    @staticmethod
    def _verify_report(report):
        """
        Verify that a report is the correct format

        First byte is modifier
        Second Byte is reserved, always 0x00
        Next 6 Bytes are scan codes, 0x00 is no key press

        ex. b'\0x02\0x00\0x04\x00\0x00\0x00\0x00\0x00' = A

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
        Second Byte is reserved, always 0x00
        Next 6 Bytes are scan codes, 0x00 is no key press

        ex. b'\0x02\0x00\0x04\x00\0x00\0x00\0x00\0x00' = A

        :param report: a bytes
        :return:
        """
        self._verify_report(report)

        with open("/dev/hidg0", "rb+") as fd:
            fd.write(report)
