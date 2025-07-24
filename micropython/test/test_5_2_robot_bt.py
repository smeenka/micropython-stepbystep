# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== test_5_2_robot_bt ...")

import time
from machine import Pin
from bluetooth import Bluetooth
from r2d2 import R2d2
import asyncio

robot = R2d2(8 ,9, 10, 11)  

# bluetooth module verbonden met Grove port 3. Dit is uart nummer 1
bt = Bluetooth(1)

led    = Pin(0, mode=Pin.OUT)
bt_led = Pin(1, mode=Pin.OUT)

event_blink = asyncio.Event()

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
  while True:
    # zorg dat andere taken ook tijd krijgen
    await asyncio.sleep_ms(10)
    line =  bt.readline()
    if line:
      as_string = bt.line2string(line)
      print("Inkomende string:%s"%as_string)             
      if as_string and len(as_string) == 6:
          sign = 1 if as_string[0]=='F' else -1
          
          speed = as_string[1:3] 
          links = int(speed) * sign
          rechts = links
          
          draaien = as_string[4:6]
          draaien = int(draaien) 
          
          linksom = 2 if as_string[3] == 'L' else -2
          draaien = draaien * linksom
          links =  links + draaien
          rechts = rechts - draaien
              
          print("Inkomende string:%s speed:%s  draaien: %s"%(as_string, speed,draaien))             
          robot.move(links,rechts)    
      else:
          print("Onbekende regel:%s"%as_string)



# definieer de taken die we willen gaan uitvoeren
asyncio.create_task(task_bt_receive())
asyncio.create_task(task_bt_blink())
asyncio.create_task(robot.task())

# start de taak die de batterij niveau stuurt naar de app
asyncio.create_task(bt.task())

print("Start het programma test_5_2_robot_bt")
print("Zet de app BT Car Controller in advanced mode!")
asyncio.run(task_blink())



