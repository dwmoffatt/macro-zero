"""
Power Switch Over Supercap Module
"""
import logging
import RPi.GPIO as GPIO
import queue
from . import INPUT_LIST_KEY_PIN_NUMBER


class PSO:
    def __init__(self, input_list=None, thread_lock=None, que=None):
        self.input_list = input_list
        self.thread_lock = thread_lock
        self.que = que

    def module_init(self):
        logging.info("Initializing Power Switch Over Module")

        # Setup I/O as Input
        GPIO.setup(self.input_list[0][INPUT_LIST_KEY_PIN_NUMBER], GPIO.IN)

        # Attach event to FALLING edge of I/O
        GPIO.add_event_detect(
            self.input_list[0][INPUT_LIST_KEY_PIN_NUMBER], GPIO.FALLING, callback=self.pso_switch_over, bouncetime=200
        )

    def module_close(self):
        logging.info("Closing Power Switch Over Module")

        # De-attach event from I/O
        GPIO.remove_event_detect(self.input_list[0][INPUT_LIST_KEY_PIN_NUMBER])

    def pso_switch_over(self, channel):
        logging.info("Power switch over!!! Device running off supercaps")

        self.thread_lock.acquire()
        try:
            self.que.put_nowait("PSO")
        except queue.Full:
            logging.exception("Que is full when adding PSO")
        finally:
            self.thread_lock.release()
