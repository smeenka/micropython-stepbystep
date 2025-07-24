# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== test_4_1_bluetooth_simpel ...")

from bluetooth import Bluetooth
import time

# bluetooth module verbonden met Grove port 3. Dit is uart nummer 1
bt = Bluetooth(1)


def test_char():
  while True:
      if bt.hasData():
          char = bt.getCharacter()
          print("Ontvangen:", char)
      time.sleep_ms(10)    

def test_line():
  while True:
      time.sleep_ms(10)    
      line =  bt.readline()
      if line:
          print("Regel:", line)

def test_string():
  while True:
      time.sleep_ms(10)    
      line =  bt.readline()
      as_string = bt.line2string(line)
      if line:
          print("Regel:", as_string)

print("Druk op toetsen in de bluetooth app op de telefoon")

#test_char()
#test_line()
test_string()