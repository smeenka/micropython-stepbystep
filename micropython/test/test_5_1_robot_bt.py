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
import gc
from dabble import Dabble, Gamepad


buzzer = Buzzer()

# maak een neopixel obect van 2 pixels, verbonden met pin 18
neo = NeoPixel(Pin(18), 2)

robot = R2d2(8 ,9, 10, 11)  
robot.setMassa(1)

led0    = Pin(0, mode=Pin.OUT)

# bluetooth module verbonden met Grove port 3. Dit is uart nummer 1
dabble = Dabble(1)
gamepad = Gamepad(dabble)
    

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
  rood = 0
  groen = 0
  blauw = 0
  global command # geef aan dat we de command op regel 20 willen gebruiken
  global neo
  while True:
    # zorg dat andere taken ook tijd krijgen
    await asyncio.sleep_ms(10)
    if gamepad.buttonPressed():
       if gamepad.isStart():
          print("Toeter")
          buzzer.setTone(400,100)
       if gamepad.isSelect():
          print("select")
          buzzer.mute()
       if gamepad.isSquare():
          print("Blauw aan")
          blauw = 100
       if gamepad.isTriangle():
          print("Rood Aan")
          rood = 100
       if gamepad.isCircle():
          print("Groen Aan")
          groen = 100
       if gamepad.isCross():
          print("kruisje")
          rood = 0
          groen = 0
          blauw = 0
      
    richting = gamepad.richting()
    snelheid = gamepad.snelheid()
    links = 0
    rechts = 0

    if richting >= 80 or richting <= -70:
        links = richting // 2
        rechts = richting // -2
    else:
        links = snelheid  + richting // 4 
        rechts= snelheid  - richting // 4
    robot.move(links, rechts)
    neo[0] = (rood, groen, blauw)
    neo[1] = (rood, groen, blauw)
    neo.write()



# definieer de taken die we willen gaan uitvoeren
asyncio.create_task(task_command())
asyncio.create_task(robot.task())
# start de taak die de verbinding verzorgt via bluetooth
asyncio.create_task(dabble.task())
# asyncio.run start de taak runner van het systeem

asyncio.run(task_blink())


