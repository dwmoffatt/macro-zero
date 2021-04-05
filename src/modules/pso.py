"""
Power Switch Over Supercap Module
"""
import logging
import RPi.GPIO as GPIO
import queue
from . import INPUT_LIST_KEY_PIN_NUMBER

PSO_COMMAND_PSO = "PSO"


class PSO:
    def __init__(self, input_list=None, thread_lock=None, que=None):
        self._input_list = input_list
        self._thread_lock = thread_lock
        self._que = que

    def module_init(self):
        logging.info("Initializing Power Switch Over Module")

        # Setup I/O as Input
        GPIO.setup(self._input_list[0][INPUT_LIST_KEY_PIN_NUMBER], GPIO.IN)

        # Attach event to FALLING edge of I/O
        GPIO.add_event_detect(
            self._input_list[0][INPUT_LIST_KEY_PIN_NUMBER], GPIO.FALLING, callback=self.pso_switch_over, bouncetime=200
        )

    def module_close(self):
        logging.info("Closing Power Switch Over Module")

        # De-attach event from I/O
        GPIO.remove_event_detect(self._input_list[0][INPUT_LIST_KEY_PIN_NUMBER])

    def pso_switch_over(self, channel):
        logging.info("Power switch over!!! Device running off supercaps")

        self._thread_lock.acquire()
        try:
            self._que.put_nowait(PSO_COMMAND_PSO)
        except queue.Full:
            logging.exception(f"Que is full when adding {PSO_COMMAND_PSO}")
        finally:
            self._thread_lock.release()
