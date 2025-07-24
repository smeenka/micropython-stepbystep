# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== Loading module buzzer ...")

from machine import Pin, PWM, Timer
 
class Buzzer:
    """ A class for generating tones with the buzzer. """
 
    def __init__(self, pin: int = 22):
        """ Creates a new Servo Object.
 
        args:
            pin (int): integer denoting the number of the GPIO pin
  
        """
 
        pin = Pin(pin, Pin.OUT)
        self.buzzer = PWM(pin)    
 
    def mute(self, t = 0):
        self.buzzer.duty_u16(0)
 
    def setTone(self, freq: int, duration: int = 0):
        """ Set the frequency and the time for the tone
        args:

        """
        self.buzzer.freq(freq)
        self.buzzer.duty_u16(3_000)
        if duration > 0:
            timer = Timer(-1)
            timer.init(mode=Timer.ONE_SHOT, period=duration, callback = self.mute)

if __name__ == "__main__":
    
  import utime as time

  buzzer = Buzzer()  
  
  
  def test3tones(t1, t2):
      for i in range(0, 3):
          buzzer.setTone(800, t1)
          time.sleep_ms(t2)
      time.sleep_ms(500)    
    
  def testSOS():
      while True:
        test3tones(100, 200)
        test3tones(300,600)
        test3tones(100,200)
        time.sleep(2)    

  testSOS()
  
                                
                                