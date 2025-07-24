# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== test_4_2_bluetooth_tasks ...")

import time
from machine import Pin
import asyncio
from bluetooth import Bluetooth

# bluetooth module verbonden met Grove port 3. Dit is uart nummer 1
bt = Bluetooth(1)
event_blink = asyncio.Event()

led    = Pin(0, mode=Pin.OUT)
bt_led = Pin(1, mode=Pin.OUT)

# taak voor het knipperen van de led als heartbeat van het programma
async def task_blink():
  print("Start taak task_blink")  
  while True:
    led.on()
    await asyncio.sleep_ms(100)
    led.off()
    await asyncio.sleep_ms(900)

# taak voor knipperen van een led als een regel is ontvangen van bluetooth
async def task_bt_blink():
  print("Start taak task_bt_blink")  
  while True:
    # wait until the bluetooth task does recieve a line
    await event_blink.wait()
    event_blink.clear()
    bt_led.value(1)
    await asyncio.sleep_ms(10)
    bt_led.value(0)


# taak voor het wachten op een BT regel en deze omzetting in een commando
# De taak zal andere taken wakker maken met de event.set()
async def task_bt_receive():
  print("Start taak task_bt_receive")
  global command # geef aan dat we de command op regel 20 willen gebruiken
  while True:
    # zorg dat andere taken ook tijd krijgen
    await asyncio.sleep_ms(10)
    line =  bt.readline()
    if line:
      as_string = bt.line2string(line)
      if as_string:
          first_char = as_string[0]
          event_blink.set()
          
          if first_char == "U":
              print("Licht Aan")
          elif first_char == "u":
              print("Licht Uit")
          elif first_char == "Y":
              print("Toeter")
          elif first_char == "F":
              print("Vooruit")
          elif first_char == "S":
              print("Stop")
          elif first_char == "B":
              print("Achteruit")
          elif first_char == "L":
              print("Links draaien")
          elif first_char == "R":
              print("Rechts draaien")
          else:
              print("Onbekend karakter:%s"%first_char)



# definieer de taken die we willen gaan uitvoeren
asyncio.create_task(task_bt_receive())
asyncio.create_task(task_bt_blink())
# start de taak die de batterij niveau stuurt naar de app
asyncio.create_task(bt.task())

print("Start het programma test_4_2_bluetooth_tasks")
asyncio.run(task_blink())
