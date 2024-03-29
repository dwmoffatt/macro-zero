"""
Rotary Encoder
"""
import logging
import queue
from . import (
    INPUT_LIST_KEY_PIN_NUMBER,
    INPUT_LIST_KEY_INPUT_TYPE,
    INPUT_TYPE_BUTTON,
    INPUT_TYPE_ROTARY_ENCODER_CLK,
    INPUT_TYPE_ROTARY_ENCODER_DIR,
    RUNNING_ON_PI,
)
from .utils import digital_read

if RUNNING_ON_PI:  # pragma: no cover
    import RPi.GPIO as GPIO

RE_COMMAND_RE_B1 = "RE_B1"
RE_COMMAND_RE_CW = "RE_CW"
RE_COMMAND_RE_CCW = "RE_CCW"


class RotaryEncoder:
    def __init__(self, input_list=None, thread_lock=None, que=None):
        self._input_list = input_list
        self._thread_lock = thread_lock
        self._que = que

        self._button_index = 0
        self._clk_index = 0
        self._dir_index = 0

    def module_init(self):
        logging.info("Initializing Rotary Encoder Module")

        # Setup I/O as Inputs Pull Up
        for i in range(0, len(self._input_list)):
            if self._input_list[i][INPUT_LIST_KEY_INPUT_TYPE] == INPUT_TYPE_BUTTON:
                self._button_index = i
                GPIO.setup(self._input_list[i][INPUT_LIST_KEY_PIN_NUMBER], GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.add_event_detect(
                    self._input_list[i][INPUT_LIST_KEY_PIN_NUMBER],
                    GPIO.RISING,
                    callback=self.btn_release,
                    bouncetime=200,
                )
            elif self._input_list[i][INPUT_LIST_KEY_INPUT_TYPE] == INPUT_TYPE_ROTARY_ENCODER_CLK:
                self._clk_index = i
                GPIO.setup(self._input_list[i][INPUT_LIST_KEY_PIN_NUMBER], GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.add_event_detect(
                    self._input_list[i][INPUT_LIST_KEY_PIN_NUMBER],
                    GPIO.FALLING,
                    callback=self.clk_trigger,
                    bouncetime=250,
                )
            elif self._input_list[i][INPUT_LIST_KEY_INPUT_TYPE] == INPUT_TYPE_ROTARY_ENCODER_DIR:
                self._dir_index = i
                GPIO.setup(self._input_list[i][INPUT_LIST_KEY_PIN_NUMBER], GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.add_event_detect(
                    self._input_list[i][INPUT_LIST_KEY_PIN_NUMBER],
                    GPIO.FALLING,
                    callback=self.dir_trigger,
                    bouncetime=250,
                )

        return True

    def module_close(self):
        logging.info("Closing Rotary Encoder Module")

        # De-attach events from I/O
        GPIO.remove_event_detect(self._input_list[self._button_index][INPUT_LIST_KEY_PIN_NUMBER])
        GPIO.remove_event_detect(self._input_list[self._clk_index][INPUT_LIST_KEY_PIN_NUMBER])
        GPIO.remove_event_detect(self._input_list[self._dir_index][INPUT_LIST_KEY_PIN_NUMBER])

        return True

    def btn_release(self, channel):

        self._thread_lock.acquire()
        try:
            self._que.put_nowait(RE_COMMAND_RE_B1)
        except queue.Full:
            logging.exception("Que is full when adding RE_B1")
        finally:
            self._thread_lock.release()

    def clk_trigger(self, channel):
        clk_value = digital_read(self._input_list[self._clk_index][INPUT_LIST_KEY_PIN_NUMBER])
        dir_value = digital_read(self._input_list[self._dir_index][INPUT_LIST_KEY_PIN_NUMBER])

        if clk_value == 0 and dir_value == 1:
            value = RE_COMMAND_RE_CW

            self._thread_lock.acquire()
            try:
                self._que.put_nowait(value)
            except queue.Full:
                logging.exception(f"Que is full when adding {value}")
            finally:
                self._thread_lock.release()

    def dir_trigger(self, channel):
        clk_value = digital_read(self._input_list[self._clk_index][INPUT_LIST_KEY_PIN_NUMBER])
        dir_value = digital_read(self._input_list[self._dir_index][INPUT_LIST_KEY_PIN_NUMBER])

        if clk_value == 1 and dir_value == 0:
            value = RE_COMMAND_RE_CCW

            self._thread_lock.acquire()
            try:
                self._que.put_nowait(value)
            except queue.Full:
                logging.exception(f"Que is full when adding {value}")
            finally:
                self._thread_lock.release()
