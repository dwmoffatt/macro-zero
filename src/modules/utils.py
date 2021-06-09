"""
Utility functions
=======================
"""

import time
from . import RUNNING_ON_PI

if RUNNING_ON_PI:  # pragma: no cover
    import RPi.GPIO as GPIO


def digital_write(pin, value):  # pragma: no cover
    GPIO.output(pin, value)


def digital_read(pin):  # pragma: no cover
    return GPIO.input(pin)


def delay_ms(delaytime):  # pragma: no cover
    time.sleep(delaytime / 1000.0)


def set_bit(value, bit_index):

    # TODO: Verify value

    # bit_index needs to be type int
    if not isinstance(bit_index, int):
        raise TypeError("bit_index needs to be type int")

    return value | (1 << bit_index)


def unset_bit(value, bit_index):

    # TODO: Verify value

    # bit_index needs to be type int
    if not isinstance(bit_index, int):
        raise TypeError("bit_index needs to be type int")

    return value & ~(1 << bit_index)
