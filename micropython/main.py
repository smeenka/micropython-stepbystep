# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("Loading module main ...")

import os
import sys
import time
import machine  
 
sys.path.append("/lib")


# rp2040 board
led    = machine.Pin(0, mode=machine.Pin.OUT)


def blink(n):
  for i in range(n):
    led.value(0)
    time.sleep_ms(100)
    led.value(1)
    time.sleep_ms(100)


#import wifi
#if not wifi.connectRetry():
#    print("Unable to connect to wifi. Blocking here")
#    blink(1000*1000*1000)

#print("Connected to accespoint")

#if machine.reset_cause() == machine.SOFT_RESET:
#    print ("Soft reset, doing nothing")
#    print('Connected!! network config:', wifi.wlan.ifconfig())

try:
    print ("Starting application")
    blink(10)
    os.chdir('/test')
    import test

except Exception as e:
    print ("Exception:",e)
except  KeyboardInterrupt:
    print ("KeyboardInterrupt")
   





