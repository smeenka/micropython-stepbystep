from machine import Pin
import time



green = Pin(0,  Pin.OUT)
red = Pin(46, Pin.OUT)
blue = Pin(45, Pin.OUT)

def show_color(pin, name):
    print("Test kleur:", name)
    pin.off()
    time.sleep_ms(500)
    pin.on()
    time.sleep_ms(500)
  

while True:
  show_color(red, "rood")  
  show_color(green, "groen")  
  show_color(blue, "blauw")  
