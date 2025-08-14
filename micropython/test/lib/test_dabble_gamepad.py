# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== test_dabble_gamepad ...")

import time
from machine import Pin
import asyncio
from dabble import Dabble, Gamepad

# Elke led is een IO pin in ouput mode (kan stroom leveren)
led0    = Pin(0, mode=Pin.OUT)
dabble = Dabble(1)
g = Gamepad(dabble)

# Taak met 3 parameters: de led die we besturen, de aan tijd en de uit tijd
async def task_blink_led():
    while True:
        led0.value(1)
        await asyncio.sleep_ms(100)
        led0.value(0)
        await asyncio.sleep_ms(900)

async def show_task():
    while True:
        await asyncio.sleep_ms(10)
        print("s:%s  r:%s  start:%s  select:%s  square:%s  triangle:%s  circle%s  cross:%s"%( g.snelheid(), g.richting(),g.isStart(), g.isSelect(), g.isSquare(), g.isTriangle(), g.isCircle(), g.isCross()))


# definieer de taken die we willen gaan uitvoeren
asyncio.create_task(task_blink_led())
asyncio.create_task(show_task())
asyncio.run(dabble.task())

    
    
    

        
    
    






