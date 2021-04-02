"""
Rotary Encoder
"""
import logging
import RPi.GPIO as GPIO
import queue
from . import (
    INPUT_LIST_KEY_PIN_NUMBER,
    INPUT_LIST_KEY_INPUT_TYPE,
    INPUT_TYPE_BUTTON,
    INPUT_TYPE_ROTARY_ENCODER_CLK,
    INPUT_TYPE_ROTARY_ENCODER_DIR,
)
from .utils import digital_read


class RotaryEncoder:
    def __init__(self, input_list=None, thread_lock=None, que=None):
        self.input_list = input_list
        self.thread_lock = thread_lock
        self.que = que

        self.button_index = 0
        self.clk_index = 0
        self.dir_index = 0

    def module_init(self):
        logging.info("Initializing Rotary Encoder Module")

        # Setup I/O as Inputs Pull Up
        for i in range(0, len(self.input_list)):
            GPIO.setup(self.input_list[i][INPUT_LIST_KEY_PIN_NUMBER], GPIO.IN, pull_up_down=GPIO.PUD_UP)

            if self.input_list[i][INPUT_LIST_KEY_INPUT_TYPE] == INPUT_TYPE_BUTTON:
                self.button_index = i
                GPIO.add_event_detect(
                    self.input_list[i][INPUT_LIST_KEY_PIN_NUMBER],
                    GPIO.RISING,
                    callback=self.btn_release,
                    bouncetime=200,
                )
            elif self.input_list[i][INPUT_LIST_KEY_INPUT_TYPE] == INPUT_TYPE_ROTARY_ENCODER_CLK:
                self.clk_index = i
                GPIO.add_event_detect(
                    self.input_list[i][INPUT_LIST_KEY_PIN_NUMBER], GPIO.BOTH, callback=self.btn_release
                )
            elif self.input_list[i][INPUT_LIST_KEY_INPUT_TYPE] == INPUT_TYPE_ROTARY_ENCODER_DIR:
                self.dir_index = i

    def module_close(self):
        logging.info("Closing Rotary Encoder Module")

        # De-attach events from I/O
        GPIO.remove_event_detect(self.input_list[self.button_index][INPUT_LIST_KEY_PIN_NUMBER])
        GPIO.remove_event_detect(self.input_list[self.clk_index][INPUT_LIST_KEY_PIN_NUMBER])

    def btn_release(self, channel):

        self.thread_lock.acquire()
        try:
            self.que.put_nowait("RE_B1")
        except queue.Full:
            logging.exception("Que is full when adding RE_B1")
        finally:
            self.thread_lock.release()

    def clk_trigger(self, channel):
        clk_value = digital_read(channel)
        dir_value = digital_read(self.input_list[self.dir_index][INPUT_LIST_KEY_PIN_NUMBER])

        if clk_value == dir_value:
            value = "RE_CW"
        else:
            value = "RE_CCW"

        self.thread_lock.acquire()
        try:
            self.que.put_nowait(value)
        except queue.Full:
            logging.exception(f"Que is full when adding {value}")
        finally:
            self.thread_lock.release()
