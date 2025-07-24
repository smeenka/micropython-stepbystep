# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== module test_2_servo ...")

import time
from machine import Pin
from dcmotor import Dcmotor
import asyncio


led    = Pin(0, mode=Pin.OUT)

# taak voor het knipperen van de led
async def task_blink():
  while True:
    led.on()
    await asyncio.sleep_ms(100)
    led.off()
    await asyncio.sleep_ms(900)

dcmotor = Dcmotor(8 ,9)  

# Taak voor het testen van de motor
async def task_test_motor():
  dcmotor.setMassa(5)  
  while True:
      print("Motor vooruit")
      dcmotor.setSpeed(99)
      await asyncio.sleep(5)
      print("Motor vrijloop")
      dcmotor.setSpeed(0)
      await asyncio.sleep(3)
      print("Motor achteruit")
      dcmotor.setSpeed(-99)
      await asyncio.sleep(5)
      print("Motor vrijloop")
      dcmotor.setSpeed(0)
      await asyncio.sleep(3)



# definieer de taken die we willen gaan uitvoeren
asyncio.create_task(task_test_motor())
asyncio.create_task(task_blink())

print("Start het programma test_2_2_dcmotor_task")
asyncio.run(dcmotor.task())





