# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== bt_terminal ...")

from machine import UART, Pin
import time
import select
import sys
import asyncio

event_blink = asyncio.Event()

led    = Pin(16, mode=Pin.OUT)
bt_led = Pin(28, mode=Pin.OUT)


# Set up the poll object
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

# setup the uart to which the bluetooth module is connected
uart = UART(1, 115200)

# Taak met 3 parameters: de led die we besturen, de aan tijd en de uit tijd
async def task_blink_led():
    while True:
        led.value(1)
        await asyncio.sleep_ms(100)
        led.value(0)
        await asyncio.sleep_ms(900)


# taak voor knipperen van een led als een regel is ontvangen van bluetooth
async def task_bt_blink():
  print("Start taak task_bt_blink")  
  while True:
    # wait until the bluetooth task does recieve a line
    await event_blink.wait()
    event_blink.clear()
    bt_led.value(1)
    await asyncio.sleep_ms(10)
    bt_led.value(0)

#taak voor het ontvangen van regels van de computer
async def task_receive_computer():
    while True:
        await asyncio.sleep_ms(10)
        poll_results = poll_obj.poll(1) # how long it will wait for message before looping again (in milliseconds)
        if poll_results:
          # Read the data from stdin (read data coming from PC)
          data = sys.stdin.readline()
          # Write the data to the input file
          sys.stdout.write("received data: " + data )
          uart.write(data)


#taak voor het ontvangen van regels van de bluetooth module
async def task_receive_bluetooth():
    while True:
        await asyncio.sleep_ms(10)
        if uart.any() > 0:
            event_blink.set()
            buffer = uart.read()
            if buffer and len(buffer)> 0:
                line = ""
                try:
                    # vertaal de nummers in de buffer naar karakters
                    line = buffer.decode('utf-8')
                except:
                    for c in buffer:
                        line = "%s - %2x"%(line,c)
                    line ="%s\n"%line    
                sys.stdout.write(line)
                # bekijk het laatste karakter in de buffer     
                eol = buffer[-1]
                if eol == 13 or eol == 10:
                    sys.stdout.write("\n")

    
# definieer de taken die we willen gaan uitvoeren
asyncio.create_task(task_bt_blink())
asyncio.create_task(task_receive_computer())
asyncio.create_task(task_receive_bluetooth())

print("Start de bluetooth terminal of de dabble app op de telefoon")

asyncio.run(task_blink_led())


