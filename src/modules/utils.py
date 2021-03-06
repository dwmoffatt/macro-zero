"""
Utility functions
=======================
"""

import time
from . import RUNNING_ON_PI

if RUNNING_ON_PI:
    import RPi.GPIO as GPIO


def digital_write(pin, value):
    GPIO.output(pin, value)


def digital_read(pin):
    return GPIO.input(pin)


def delay_ms(delaytime):
    time.sleep(delaytime / 1000.0)
