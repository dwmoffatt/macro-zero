"""
M-Keyboard
"""
import logging
import RPi.GPIO as GPIO
import queue
from . import INPUT_LIST_KEY_PIN_NUMBER


class MKeyboard:
    def __init__(self, input_list=None, thread_lock=None, que=None):
        self.input_list = input_list
        self.thread_lock = thread_lock
        self.que = que

    def module_init(self):
        logging.info("Initializing Rotary Encoder Module")

        # Setup I/O as Inputs Pull Up & attach events to RISING edge of I/O
        for i in range(0, len(self.input_list)):
            GPIO.setup(self.input_list[i][INPUT_LIST_KEY_PIN_NUMBER], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(
                self.input_list[i][INPUT_LIST_KEY_PIN_NUMBER], GPIO.RISING, callback=self.btn_release, bouncetime=200
            )

    def module_close(self):
        logging.info("Closing Rotary Encoder Module")

        # De-attach events from I/O
        for i in range(0, len(self.input_list)):
            GPIO.remove_event_detect(self.input_list[i][INPUT_LIST_KEY_PIN_NUMBER])

    def btn_release(self, channel):
        button = 0
        for i in range(0, len(self.input_list)):
            if self.input_list[i][INPUT_LIST_KEY_PIN_NUMBER] == channel:
                button = i + 1

        logging.info(f"Button {button} released")

        self.thread_lock.acquire()
        try:
            self.que.put_nowait(f"B{button}")
        except queue.Full:
            logging.exception(f"Que is full when adding B{button}")
        finally:
            self.thread_lock.release()
