# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== test_4_2_bluetooth_tasks ...")

import time
from machine import Pin
import asyncio
from dabble import Dabble, Gamepad

# Elke led is een IO pin in ouput mode (kan stroom leveren)
led0    = Pin(0, mode=Pin.OUT)
# bluetooth module verbonden met Grove port 3. Dit is uart nummer 1
dabble = Dabble(1)
gamepad = Gamepad(dabble)
led    = Pin(0, mode=Pin.OUT)

# taak voor het knipperen van de led als heartbeat van het programma
async def task_blink():
  print("Start taak task_blink")  
  while True:
    led0.on()
    await asyncio.sleep_ms(100)
    led0.off()
    await asyncio.sleep_ms(900)


# taak voor het wachten op een BT regel en deze omzetting in een commando
# De taak zal andere taken wakker maken met de event.set()
async def task_command():
  print("Start taak task_command")
  while True:
    # zorg dat andere taken ook tijd krijgen
    await asyncio.sleep_ms(100)
    if gamepad.buttonPressed():
       if gamepad.isStart():
          print("start")
       if gamepad.isSelect():
          print("select")
       if gamepad.isSquare():
          print("vierkant")
       if gamepad.isTriangle():
          print("driehoek")
       if gamepad.isCircle():
          print("cirkel")
       if gamepad.isCross():
          print("kruisje")


# definieer de taken die we willen gaan uitvoeren
asyncio.create_task(task_command())
# start de taak dabble verbinding verzorgt
asyncio.create_task(dabble.task())

print("Start het programma test_4_2_bluetooth_tasks")
asyncio.run(task_blink())
