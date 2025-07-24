# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("Loading test_serial ...")
# Created by Anton Smeenk

import uos as os
import sys
import utime as time
import machine
from machine import Pin, PWM

import logging
logging.setGlobal(logging.DEBUG)


from machine import Pin
from neopixel import NeoPixel

pin = Pin(27, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, 25)   # create NeoPixel driver on GPIO0 for 8 pixels
np[0] = (255, 255, 255) # set the first pixel to white
np.write()              # write data to all pixels
r, g, b = np[0]         # get first pixel colour


def sweep():
    for i in range (1, 26):
        np[i] = (100,100,100)
        np[i-1] = (2,2,2)
        np.write()
        time.sleep_ms(100)


while True:
    sweep()