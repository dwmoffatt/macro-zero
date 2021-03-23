"""
E-Ink Display Module
==========================
"""
import logging
import spidev
import RPi.GPIO as GPIO
from . import RST_PIN, DC_PIN, CS_PIN, BUSY_PIN
from utils import digital_write, digital_read, delay_ms

# Display resolution
EPD_WIDTH = 104
EPD_HEIGHT = 212


class EInk:
    def __init__(self):

        self.SPI = spidev.SpiDev()
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

    def module_init(self):

        GPIO.setup(RST_PIN, GPIO.OUT)
        GPIO.setup(DC_PIN, GPIO.OUT)
        GPIO.setup(CS_PIN, GPIO.OUT)
        GPIO.setup(BUSY_PIN, GPIO.IN)

        # SPI device, bus = 0, device = 0
        self.SPI.open(0, 0)
        self.SPI.max_speed_hz = 4000000
        self.SPI.mode = 0b00

        return 0

    def module_exit(self):
        # logging.debug("spi end")
        self.SPI.close()

        # logging.debug("close 5V, Module enters 0 power consumption ...")
        GPIO.output(RST_PIN, 0)
        GPIO.output(DC_PIN, 0)

        GPIO.cleanup()

    @staticmethod
    def hardware_reset():
        digital_write(RST_PIN, 1)
        delay_ms(200)
        digital_write(RST_PIN, 0)
        delay_ms(5)
        digital_write(RST_PIN, 1)
        delay_ms(200)

    def send_command(self, command):
        digital_write(DC_PIN, 0)
        digital_write(CS_PIN, 0)
        self.SPI.writebytes([command])
        digital_write(CS_PIN, 1)

    def send_data(self, data):
        digital_write(DC_PIN, 1)
        digital_write(CS_PIN, 0)
        self.SPI.writebytes([data])
        digital_write(CS_PIN, 1)

    @staticmethod
    def read_busy():
        # logging.debug("e-Paper busy")
        while digital_read(BUSY_PIN) == 0:  # 0: idle, 1: busy
            delay_ms(100)
        # logging.debug("e-Paper busy release")

    def init(self):
        if self.module_init() != 0:
            return -1

        self.hardware_reset()

        self.send_command(0x06)  # BOOSTER_SOFT_START
        self.send_data(0x17)
        self.send_data(0x17)
        self.send_data(0x17)

        self.send_command(0x04)  # POWER_ON
        self.read_busy()

        self.send_command(0x00)  # PANEL_SETTING
        self.send_data(0x8F)

        self.send_command(0x50)  # VCOM_AND_DATA_INTERVAL_SETTING
        self.send_data(0xF0)

        self.send_command(0x61)  # RESOLUTION_SETTING
        self.send_data(self.width & 0xFF)
        self.send_data(self.height >> 8)
        self.send_data(self.height & 0xFF)
        return 0

    def get_buffer(self, image):
        # logging.debug("bufsiz = ",int(self.width/8) * self.height)
        buf = [0xFF] * (int(self.width / 8) * self.height)
        image_monocolor = image.convert("1")
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        # logging.debug("imwidth = %d, imheight = %d",imwidth,imheight)
        if imwidth == self.width and imheight == self.height:
            logging.debug("Vertical")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        elif imwidth == self.height and imheight == self.width:
            logging.debug("Horizontal")
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buf[int((newx + newy * self.width) / 8)] &= ~(0x80 >> (y % 8))
        return buf

    def display(self, imageblack, imagered):
        self.send_command(0x10)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(imageblack[i])
        # self.send_command(0x92)

        self.send_command(0x13)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(imagered[i])
        # self.send_command(0x92)

        self.send_command(0x12)  # REFRESH
        self.read_busy()

    def clear(self):
        self.send_command(0x10)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)
        self.send_command(0x92)

        self.send_command(0x13)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)
        self.send_command(0x92)

        self.send_command(0x12)  # REFRESH
        self.read_busy()

    def sleep(self):
        self.send_command(0x02)  # POWER_OFF
        self.read_busy()
        self.send_command(0x07)  # DEEP_SLEEP
        self.send_data(0xA5)  # check code

        delay_ms(2000)
        self.module_exit()
