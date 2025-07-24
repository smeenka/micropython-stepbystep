# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== test_1_1_knipper_led ...")

import time
from machine import Pin

# De led (het lampje) is aangesloten op pin 48 van de microcontroller.
# Maak de pin een output pin.
# een output pin kan stroom leveren, waardoor de led kan gaan branden

led    = Pin(0, mode=Pin.OUT)

# De funktie blink
def blink():
    led.on()
    time.sleep_ms(100)
    led.off()
    time.sleep_ms(500)

print("Start het programma blink (voor altijd)")
while True:
    blink()



