# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== test_2_1_dcmotor_simpel ...")

import time
from machine import Pin

# rp2040-pi-maker board
m1A    = Pin(8, mode=Pin.OUT)
m1B    = Pin(9, mode=Pin.OUT)

# test een dc motor 
def test_dc_motor():
    print("Motor vooruit")
    m1A.value(1)
    m1B.value(0)
    time.sleep(5)
    print("Motor vrijloop")
    m1A.value(1)
    m1B.value(1)
    time.sleep(1)
    print("Motor achteruit")
    m1A.value(0)
    m1B.value(1)
    time.sleep(5)
    print("Motor remmen")
    m1A.value(0)
    m1B.value(0)
    time.sleep(5)



print("Start het programma test_2_1_dcmotor_simpel")
while True:
    test_dc_motor()




