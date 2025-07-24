# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== test_1_2_knipper_async ...")

import time
from machine import Pin
from asyncio import sleep_ms, create_task, run

# Elke led is een IO pin in ouput mode (kan stroom leveren)
led0    = Pin(0, mode=Pin.OUT)
led1    = Pin(1, mode=Pin.OUT)
led2    = Pin(2, mode=Pin.OUT)
led3    = Pin(3, mode=Pin.OUT)
led6    = Pin(6, mode=Pin.OUT)
led7    = Pin(7, mode=Pin.OUT)

# Taak met 3 parameters: de led die we besturen, de aan tijd en de uit tijd
async def task_blink_led(led, aan_tijd, uit_tijd):
    while True:
        led.value(1)
        await sleep_ms(aan_tijd)
        led.value(0)
        await sleep_ms(uit_tijd)


# definieer de taken die we willen gaan uitvoeren
create_task(task_blink_led( led1, 100, 1010))
create_task(task_blink_led( led2, 100, 1020))
create_task(task_blink_led( led3, 100, 1030))
#create_task(task_blink_led( led6, 100, 1040))
#create_task(task_blink_led( led7, 100, 1060))

print("Start het programma test_1_1_knipper_async (voor altijd)")
run(task_blink_led( led0, 100, 1000))






