# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== Loading module dcmotor ...")

from machine import Pin, PWM
import asyncio

MAX_U16 = 65535 
 
class Dcmotor:
    """ A simple class for controlling a servo with the Raspberry Pi Pico.
 
    Attributes:
 
        minVal: An integer denoting the minimum duty value for the servo motor.
 
        maxVal: An integer denoting the maximum duty value for the servo motor.
 
    """
 
    def __init__(self, pinA:int, pinB:int):
        """ Creates a new Dcmotor Object.
 
        args:
            pinA (int): integer denoting the number of the GPIO A pin
            pinB (int): integer denoting the number of the GPIO B pin
  
        """
        self.mxA = Pin(pinA, Pin.OUT)
        self.mxB = Pin(pinB, Pin.OUT)
        self.pwmA = PWM(self.mxA)    
        self.pwmA.freq(100)
        self.pwmB = PWM(self.mxB)    
        self.pwmB.freq(100)
        self.actual = 0
        self.speed = 0
        self.massa = 5
        self.increment = 5
 
    def setTarget(self, value: int):
        """ Moves the servo to the specified position. 
        args:
             value (int): The servo duty cycle
            1000 is to the left, 1500 is in the middle, 2000 is to the right
            Minimum is 750, maximunm is 2250
            If 0 the servo motor is released
 
        """
        if value < self.limitL:
            value = self.limitL
        elif value > self.limitH:
          value = self.limitH
        
        
        self.target = value
        duty  = int(value * 0xFFFF/ 20_000)  # 20ms is the time of one period (50 hz)
        self.servo.duty_u16(duty)
 
     
    def setSpeed(self, speed: int):
        """ speed is een getal tussen 99 en -99 """
        if speed < -99:
            speed = -99
        elif speed > 99:
            speed = 99
        self.speed = speed
        
 
    def setMassa(self, massa: int):
        """ massa is a value between 1 and 9 """
        if massa < 0:
            massa = 0
        elif massa > 9:
            massa = 9
        self.massa = massa
        if self.massa == 0:
            self.increment = 100
        else:
            self.increment = 10 -  self.massa


    def stop(self):
        self.actual = 0
        self.speed = 0
        
        

    async def task(self) :
        while True:
            await asyncio. sleep_ms(50)
            if self.actual < self.speed:
                self.actual += self.increment
                if self.actual > self.speed:
                    self.actual = self.speed

            if self.actual > self.speed:
                self.actual -= self.increment
                if self.actual < self.speed:
                    self.actual = self.speed

            if self.actual < 0:
                self.pwmA.duty_u16(0)
                self.pwmB.duty_u16(-655 * self.actual)
            elif self.actual > 0:
                self.pwmA.duty_u16(655 * self.actual)
                self.pwmB.duty_u16(0)
            else:
                self.pwmA.duty_u16(65535)
                self.pwmB.duty_u16(65535)
                            




if __name__ == "__main__":
    
  dcmotor = Dcmotor(8 ,9)  
  # Taak met 3 parameters: de led die we besturen, de aan tijd en de uit tijd
  async def task_test_motor():
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

  print("Start de asyncio loop")
  asyncio.run(dcmotor.task())