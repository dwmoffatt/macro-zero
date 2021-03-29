"""
M-Keyboard
"""
import logging
import RPi.GPIO as GPIO
import queue


class MKeyboard:
    def __init__(self, input_list=None, thread_lock=None, que=None):
        self.input_list = input_list
        self.thread_lock = thread_lock
        self.que = que

    def module_init(self):
        logging.info("Initializing MKeyboard Module")

        # Setup I/O as Inputs Pull Up
        for i in range(0, len(self.input_list)):
            GPIO.setup(self.input_list[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Attach events to RISING edge of I/O
        for i in range(0, len(self.input_list)):
            GPIO.add_event_detect(self.input_list, GPIO.RISING, callback=self.btn_release, bouncetime=200)

    def module_close(self):
        logging.info("Closing MKeyboard Module")

        # De-attach events from I/O
        for i in range(0, len(self.input_list)):
            GPIO.remove_event_detect(self.input_list)

    def btn_release(self, channel):
        button = self.input_list.index(channel) + 1
        logging.info(f"Button {button} released")

        self.thread_lock.acquire()
        try:
            self.que.put_nowait(f"B{button}")
        except queue.Full:
            logging.exception(f"Que is full when adding B{button}")
        finally:
            self.thread_lock.release()
