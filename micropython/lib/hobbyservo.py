# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== Loading module hobbyservo ...")

from machine import Pin, PWM
 
class HobbyServo:
    """ A simple class for controlling a servo with the Raspberry Pi Pico.
 
    Attributes:
 
        minVal: An integer denoting the minimum duty value for the servo motor.
 
        maxVal: An integer denoting the maximum duty value for the servo motor.
 
    """
 
    def __init__(self, pin: int, limits = 750, center=1500):
        """ Creates a new Servo Object.
 
        args:
            pin (int): integer denoting the number of the GPIO pin
  
        """
 
        pin = Pin(pin, Pin.OUT)
        self.servo = PWM(pin)    
        self.servo.freq(50)
        self.limitH = center + limits
        self.limitL = center - limits
        self.center = center
 
    def deinit(self):
        """ Deinitializes the underlying PWM object.
 
        """
        self.servo.deinit()
 
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
 
     
    def setAngle(self, angle: int):
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
        
        delta = self.center -self.limitL
        target = self.limitL + (angle * delta / 90 )
        self.setTarget(target)
        
 
    def setSpeed(self, speed: int):
        """ Speed is a value between -9 and 9 """
        if speed < -9:
            speed = -9
        elif speed > 9:
            speed = 9
        target = self.center + 50 * speed
        self.setTarget(target)
 
    def middle(self):
        """ Moves the servo to the middle.
        """
        self.setTarget(self.center)
 
    def getPosition(self):
        return self.target    


if __name__ == "__main__":
    
  import utime
 
  
  def testPosition():        
      s1 = HobbyServo(7, 750, 1500)       # Servo pin is connected to pin 7
      for i in range(5):
          print("Turn left sync ...")
          s1.setTarget(900 )
          utime.sleep(1)
          for i in range(s1.limitL, s1.limitH + 100,100):
              s1.setTarget(i)
              utime.sleep(0.5)
          utime.sleep(2)
          print("Turn right sync ...")
          for i in range(s1.limitH, s1.limitL - 100,-100):
              s1.setTarget(i)
              utime.sleep(0.5)
          utime.sleep(2)
          print("Middle position ...")
          s1.setTarget(1500)
          utime.sleep(2)
      
  def testAngle():        
      s1 = HobbyServo(7, 750, 1500)       # Servo pin is connected to pin 7
      for i in range(5):
          print("Turn left ...")
          utime.sleep(1)
          for i in range(0,190, 10):
              s1.setAngle(i)
              utime.sleep(0.5)
          utime.sleep(2)
          print("Turn right ...")
          for i in range(180, -10 , -10):
              s1.setAngle(i)
              utime.sleep(0.5)
          utime.sleep(2)
          print("Middle position ...")
          s1.setAngle(90)
          utime.sleep(2)

  def testSpeed():        
      s1 = HobbyServo(17, 750, 1425)       # Servo pin is connected to pin 17
      for i in range(5):
          print("Backwards  slow ...")
          s1.setSpeed(-1)
          utime.sleep(2)

          print("Backwards  fast ...")
          s1.setSpeed(-9)
          utime.sleep(2)
          print("Stop ...")
          s1.setSpeed(0)
          utime.sleep(2)

          print("Forward slow ...")
          s1.setSpeed(1)
          utime.sleep(2)

          print("Forward fast ...")
          s1.setSpeed(9)
          utime.sleep(2)

          print("Stop ...")
          s1.setSpeed(0)
          utime.sleep(2)


  #testPosition()
  #testAngle()
  testSpeed()
  
                                
                                