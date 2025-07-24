# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== test_3_1_robot_simple ...")

import time
from machine import Pin
from r2d2 import R2d2
import asyncio

r2d2 = R2d2(8 ,9, 10, 11)  


# Test Taak 
async def task_test_r2d2():
    r2d2.setMassa(1)
    while True:
        print("vooruit")
        r2d2.move(99, 99)
        await asyncio.sleep(5)
        print("Linksom")
        r2d2.move(99, 0)
        await asyncio.sleep(5)
        print("Achteruit")
        r2d2.move(-99, -99)
        await asyncio.sleep(5)
        print("Rechtsom")
        r2d2.move(-99, 0)
        await asyncio.sleep(5)


led    = Pin(0, mode=Pin.OUT)

# taak voor het knipperen van de led
async def task_blink():
  while True:
    led.value(1)
    await asyncio.sleep_ms(100)
    led.value(0)
    await asyncio.sleep_ms(900)

# definieer de taken die we willen gaan uitvoeren
asyncio.create_task(task_test_r2d2())
asyncio.create_task(task_blink())

print("Start de asyncio loop")
asyncio.run(r2d2.task())






