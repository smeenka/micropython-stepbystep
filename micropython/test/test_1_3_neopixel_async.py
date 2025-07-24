# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== test_1_3_neopixel_async ...")

import time
from machine import Pin
from neopixel import NeoPixel 
from asyncio import sleep_ms, create_task, run
from buzzer import Buzzer

# maak een neopixel obect van 2 pixels, verbonden met pin 18
neo = NeoPixel(Pin(18), 2)

# Taak met 3 parameters: de led die we besturen, de aan tijd en de uit tijd
async def task_blink_led():
    led    = Pin(0, mode=Pin.OUT)
    while True:
        led.value(1)
        await sleep_ms(100)
        led.value(0)
        await sleep_ms(900)

# Taak met 3 parameters: de led die we besturen, de aan tijd en de uit tijd
async def task_neopixel(neoIndex, wachttijdMs):
    global neo
    index = 0
    while True:
        if index == 0:
            pixel = (0, 0, 0)
        elif index == 1:
            pixel = (0, 0, 100)
        elif index == 2:
            pixel = (0, 100, 0)
        elif index == 3:
            pixel = (0, 100, 100)
        elif index == 4:
            pixel = (100, 0, 0)
        elif index == 5:
            pixel = (100, 0, 100)
        elif index == 6:
            pixel = (100, 100, 0)
        elif index == 7:
            pixel = (100, 100, 100)
        index += 1
        if index > 7:
            index = 0
        neo[neoIndex] = pixel
        neo.write()
        await sleep_ms(wachttijdMs)


async def task_sirene():
    buzzer = Buzzer()
    freq = 100
    while True:
        await sleep_ms(10)
        freq += 2
        if freq > 1000:
            freq = 100
        buzzer.setTone(freq)
        
    

# definieer de taken die we willen gaan uitvoeren
create_task(task_neopixel(0, 1000))
create_task(task_neopixel(1, 1500))
create_task(task_sirene())

print("Start het programma test_1_3_neopixel_async (voor altijd)")
run(task_blink_led())






