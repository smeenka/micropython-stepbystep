# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== Loading module dcmotor ...")

from machine import Pin, PWM
import asyncio
from dcmotor import Dcmotor
 
class R2d2:
    """ A robot class for controlling a robot with 2 motors with the Raspberry Pi Pico.
    """
    def __init__(self, m1A:int, m1B:int, m2A:int, m2B: int ):
        """ Creates a new Dcmotor Object."""
        self.motorL = Dcmotor(m1A, m1B)
        self.motorR = Dcmotor(m2A, m2B)

    def move(self, left: int, right:int):
        """ Moves the robot """
        self.motorL.setSpeed(left)
        self.motorR.setSpeed(right)

    def stop(self):
        """ Stops the robot """
        self.motorL.stop()
        self.motorR.stop()


    def setMassa(self, massa:int):
        self.motorL.setMassa(massa)    
        self.motorR.setMassa(massa)    

    async def task(self) :
        asyncio.create_task(self.motorL.task())
        asyncio.create_task(self.motorR.task())
        while True:
            await asyncio.sleep(5)

if __name__ == "__main__":

  r2d2 = R2d2(8 ,9, 10, 11)  
  # Test Taak 
  async def task_test_r2d2():
      r2d2.setMassa(1)
      while True:
          print("vooruit")
          r2d2.move(99, 99)
          await asyncio.sleep(5)
          print("Linksom")
          r2d2.move(99, 0)
          await asyncio.sleep(5)
          print("Achteruit")
          r2d2.move(-99, -99)
          await asyncio.sleep(5)
          print("Rechtsom")
          r2d2.move(-99, 0)
          await asyncio.sleep(5)

  # definieer de taken die we willen gaan uitvoeren
  asyncio.create_task(task_test_r2d2())

  print("Start de asyncio loop")
  asyncio.run(r2d2.task())