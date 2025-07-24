# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== test_5_1_robot_bt ...")

import time
from machine import Pin
from bluetooth import Bluetooth
from r2d2 import R2d2
from buzzer import Buzzer
from neopixel import NeoPixel

import asyncio

buzzer = Buzzer()

# maak een neopixel obect van 2 pixels, verbonden met pin 18
neo = NeoPixel(Pin(18), 2)

robot = R2d2(8 ,9, 10, 11)  
robot.setMassa(1)

led    = Pin(0, mode=Pin.OUT)
bt_led = Pin(1, mode=Pin.OUT)

# bluetooth module verbonden met Grove port 3. Dit is uart nummer 1
bt = Bluetooth(1)
    
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
  rood = 0
  groen = 0
  blauw = 0
  global command # geef aan dat we de command op regel 20 willen gebruiken
  global neo
  while True:
    # zorg dat andere taken ook tijd krijgen
    await asyncio.sleep_ms(10)
    line =  bt.readline()
    if line:
      as_string = bt.line2string(line)
      if as_string:
          first_char = as_string[0]
          event_blink.set()
          
          if first_char == "V":
              print("Rood Aan")
              rood = 100
          elif first_char == "v":
              print("Rood Uit")
              rood = 0
          elif first_char == "U":
              print("Groen Aan")
              groen = 100
          elif first_char == "u":
              print("Groen uit")
              groen = 0
          elif first_char == "W":
              print("Blauw aan")
              blauw = 100
          elif first_char == "w":
              print("Blauw uit")
              blauw = 0
          elif first_char == "Y":
              print("Toeter")
              buzzer.setTone(400,500)
          elif first_char == "S":
              print("Stop")
              robot.move( 0, 0)
          elif first_char == "B":
              print("Achteruit")
              robot.move( -70, -100)
          elif first_char == "L":
              print("Links draaien")
              robot.move( 40, -50)
          elif first_char == "R":
              print("Rechts draaien")
              robot.move( -40, 50)
          elif first_char == "F":
              print("vooruit")
              robot.move( 70, 100)
          elif first_char == "G":
              print("Schuin Links")
              robot.move( 70, 50)
          elif first_char == "H":
              print("Schuin Rechts")
              robot.move( 35, 100)
          elif first_char == "I":
              print("Achteruit schuin links")
              robot.move( -70, -50)
          elif first_char == "J":
              print("Achteruiit schuin rechts")
              robot.move( -35, -100)
          elif first_char == "S":
              print("Stop")
              robot.stop()
          else:
              print("Onbekend karakter:%s"%first_char)
          neo[0] = (rood, groen, blauw)
          neo[1] = (rood, groen, blauw)
          neo.write()



# definieer de taken die we willen gaan uitvoeren
asyncio.create_task(task_bt_receive())
asyncio.create_task(task_bt_blink())
asyncio.create_task(robot.task())
# start de taak die de batterij niveau stuurt naar de app
asyncio.create_task(bt.task())

print("Start het programma test_5_1_robot_bt")
asyncio.run(task_blink())


