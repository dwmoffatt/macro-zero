"""
E-Ink Display Module
==========================
"""
# import logging
import time
import os
import spidev
import RPi.GPIO as GPIO
from . import RST_PIN, DC_PIN, CS_PIN, BUSY_PIN, fonts_path
from .utils import digital_write, digital_read, delay_ms
from PIL import Image, ImageDraw, ImageFont

# Display resolution
EPD_WIDTH = 104
EPD_HEIGHT = 212


class EInk:
    def __init__(self):

        self.SPI = spidev.SpiDev()
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

        self.font20 = ImageFont.truetype(os.path.join(fonts_path, "Font.ttc"), 20)
        self.font18 = ImageFont.truetype(os.path.join(fonts_path, "Font.ttc"), 18)

    def module_init(self):

        GPIO.setup(RST_PIN, GPIO.OUT)
        GPIO.setup(DC_PIN, GPIO.OUT)
        GPIO.setup(CS_PIN, GPIO.OUT)
        GPIO.setup(BUSY_PIN, GPIO.IN)

        # SPI device, bus = 0, device = 0
        self.SPI.open(0, 0)
        self.SPI.max_speed_hz = 4000000
        self.SPI.mode = 0b00

        self.hardware_reset()

        self.send_command(0x04)  # POWER_ON
        self.read_busy()

        self.send_command(0x00)  # PANEL_SETTING
        self.send_data(0x0F)
        self.send_data(0x89)

        self.send_command(0x61)  # RESOLUTION_SETTING
        self.send_data(0x68)
        self.send_data(0x00)
        self.send_data(0xD4)

        self.send_command(0x50)
        self.send_data(0x77)

    def module_close(self):
        self.send_command(0x02)  # POWER_OFF
        self.read_busy()

        # logging.debug("spi end")
        self.SPI.close()

        # logging.debug("close 5V, Module enters 0 power consumption ...")
        GPIO.output(RST_PIN, 0)
        GPIO.output(DC_PIN, 0)

    @staticmethod
    def hardware_reset():
        digital_write(RST_PIN, 1)
        delay_ms(200)
        digital_write(RST_PIN, 0)
        delay_ms(2)
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

    def read_busy(self):
        # logging.debug("e-Paper busy")
        self.send_command(0x71)
        while digital_read(BUSY_PIN) == 0:  # 0: idle, 1: busy
            self.send_command(0x71)
            delay_ms(100)
        # logging.debug("e-Paper busy release")

    def get_buffer(self, image):
        # logging.debug("bufsiz = ",int(self.width/8) * self.height)
        buf = [0xFF] * (int(self.width / 8) * self.height)
        image_monocolor = image.convert("1")
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        # logging.debug("imwidth = %d, imheight = %d",imwidth,imheight)
        if imwidth == self.width and imheight == self.height:
            # logging.debug("Vertical")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        elif imwidth == self.height and imheight == self.width:
            # logging.debug("Horizontal")
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

        self.send_command(0x13)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(imagered[i])

        self.send_command(0x12)  # REFRESH
        delay_ms(100)
        self.read_busy()

    def clear(self):
        self.send_command(0x10)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)

        self.send_command(0x13)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)

        self.send_command(0x12)  # REFRESH
        delay_ms(100)
        self.read_busy()

    def sleep(self):
        self.send_command(0x50)
        self.send_data(0xF7)
        self.send_command(0x02)  # POWER_OFF
        self.read_busy()
        self.send_command(0x07)  # DEEP_SLEEP
        self.send_data(0xA5)  # check code

        delay_ms(2000)

        GPIO.output(RST_PIN, 0)
        GPIO.output(DC_PIN, 0)

    def test_horizontal_image(self):
        black_image = Image.new("1", (EPD_HEIGHT, EPD_WIDTH), 255)  # 298*126
        ry_image = Image.new("1", (EPD_HEIGHT, EPD_WIDTH), 255)  # 298*126  ryimage: red or yellow image
        drawblack = ImageDraw.Draw(black_image)
        drawry = ImageDraw.Draw(ry_image)
        drawblack.text((10, 0), "hello world", font=self.font20, fill=0)
        drawblack.text((10, 20), "2.13inch e-Paper bc", font=self.font20, fill=0)
        drawblack.text((120, 0), "微雪电子", font=self.font20, fill=0)
        drawblack.line((20, 50, 70, 100), fill=0)
        drawblack.line((70, 50, 20, 100), fill=0)
        drawblack.rectangle((20, 50, 70, 100), outline=0)
        drawry.line((165, 50, 165, 100), fill=0)
        drawry.line((140, 75, 190, 75), fill=0)
        drawry.arc((140, 50, 190, 100), 0, 360, fill=0)
        drawry.rectangle((80, 50, 130, 100), fill=0)
        drawry.chord((85, 55, 125, 95), 0, 360, fill=1)
        self.display(self.get_buffer(black_image), self.get_buffer(ry_image))
        time.sleep(2)

    def test_vertical_image(self):
        black_image = Image.new("1", (EPD_WIDTH, EPD_HEIGHT), 255)  # 126*298
        ry_image = Image.new("1", (EPD_WIDTH, EPD_HEIGHT), 255)  # 126*298
        drawblack = ImageDraw.Draw(black_image)
        drawry = ImageDraw.Draw(ry_image)
        drawblack.text((2, 0), "hello world", font=self.font18, fill=0)
        drawblack.text((2, 20), "2.13 epd b", font=self.font18, fill=0)
        drawblack.text((20, 50), "微雪电子", font=self.font18, fill=0)
        drawblack.line((10, 90, 60, 140), fill=0)
        drawblack.line((60, 90, 10, 140), fill=0)
        drawblack.rectangle((10, 90, 60, 140), outline=0)
        drawry.rectangle((10, 150, 60, 200), fill=0)
        drawry.arc((15, 95, 55, 135), 0, 360, fill=0)
        drawry.chord((15, 155, 55, 195), 0, 360, fill=1)
        self.display(self.get_buffer(black_image), self.get_buffer(ry_image))
        time.sleep(2)
