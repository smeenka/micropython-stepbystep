# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== module test_7_ultrasoon_motorcontrol ...")

import time
from machine import Pin
from hcsr04 import HCSR04
import asyncio
from r2d2 import R2d2
from bluetooth import Bluetooth

# bluetooth module verbonden met Grove port 3. Dit is uart nummer 1
bt = Bluetooth(1)


# rp2040 board
r2d2 = R2d2(8 ,9, 10, 11)

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
    await asyncio.sleep_ms(100)
    distance = sensor.distance_mm()
    #print('Distance:', distance, 'mm')    

async def task_robot():
    print("start taak task_robot")
    global r2d2
    global distance
    r2d2.setMassa(1)
    draaien = False
   
    while True:
        await asyncio.sleep_ms(100)
        if draaien:
            if distance > 1000:   # indien aand het draaienachteruit aan het rijden en de afstand is groter dan 30 cm ga weer voortuit rijden
                draaien = False
                r2d2.move(0,0) # robot langzaam tot stilstand
                await asyncio.sleep(1)
                print("Vooruit")
                draaien = False
        else:    
            if distance < 300:   # indien vooruit aan het rijden en de afstand is kleiner dan 10 cm, ga achteruit rijden
                r2d2.move(0,0) # robot langzaam tot stilstand
                await asyncio.sleep(1)
                draaien = True
                print("Zoek nieuwe richting")
                r2d2.move(50,-50) # motor langzaam draaien
            else:
                r2d2.move(98,98)

asyncio.create_task(task_distance())
asyncio.create_task(task_distance_blink())
asyncio.create_task(r2d2.task())
asyncio.create_task(task_robot())

# start de taak die de batterij niveau stuurt naar de app
asyncio.create_task(bt.task())

print("Start het programma test_6_2_ultrasoon_robot")
asyncio.run(task_blink())

