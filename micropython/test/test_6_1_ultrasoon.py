# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== module test_6_1_ultrasoon ...")

import time
from machine import Pin
from hcsr04 import HCSR04
import asyncio

distance = 250

# taak voor het knipperen van de led als heartbeat van het programma
async def task_blink():
  led    = Pin(0, mode=Pin.OUT)
  print("Start taak task_blink")  
  while True:
    led.on()
    await asyncio.sleep_ms(100)
    led.off()
    await asyncio.sleep_ms(900)

# taak voor knipperen van een led die de afstand aangeeft
async def task_distance_blink():
  print("Start taak distance_blink")
  distance_led = Pin(16, mode=Pin.OUT)
  global distance
  while True:
    await asyncio.sleep_ms(distance//2)
    distance_led.value(1)
    await asyncio.sleep_ms(10)
    distance_led.value(0)

async def task_distance():
  print("Start taak distance")
  # Ultrasoon sensor verbonden aan groveconnector 6
  sensor = HCSR04(trigger_pin=26, echo_pin=27)
  global distance
  while True:
    await asyncio.sleep_ms(200)
    distance = sensor.distance_mm()
    print('Distance:', distance, 'mm')    


# definieer de taken die we willen gaan uitvoeren
asyncio.create_task(task_distance())
asyncio.create_task(task_distance_blink())

print("Start het programma test_6_1_ultrasoon")
asyncio.run(task_blink())



