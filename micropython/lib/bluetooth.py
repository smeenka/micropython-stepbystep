# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== Loading module bluetooth ...")

from machine import UART, Pin, ADC
import time
import asyncio
 
class Bluetooth:
    """ A simple class for receiving and sending charaters via a bluettooth module
    """
    def __init__(self, uart_nr= 0):
        """ Creates a new bluetooth Object."""
        self.uart = UART(uart_nr, 115200)
    
    def hasData(self):
        return self.uart.any() > 0
 
    # readline will block until there is a newline (13) is received
    def readline(self):
        """ Return None if no line is received. 
        Is a line is received then return line as a buffer ) 
        """
        line = self.uart.readline()
        if line:
            return line
        else:
            return None

    def line2string(self, line):
        """ Change byte buffer into a string"""    
        if line:
          return line.strip().decode("utf-8")
        else:
           return None

    def getCharacter(self):
        # haal het karakter op uit de uart buffer
        buffer = self.uart.read(1)
        # vertaal de nummers in de buffer naar karakters
        return buffer.decode('utf-8')

    def getNumber(self):
        # haal het karakter op uit de uart buffer
        buffer = self.uart.read(1)
        return buffer[0]

    def setBattery(self, battery):
       self.uart.write("BAT:%s\n"%battery)

    def setSpeed(self, speed):
       self.uart.write("SPEED :%s\n"%speed)


    async def task(self) :
        adc =  ADC(Pin(29))
        while True:
            await asyncio.sleep(5)
            batt = adc.read_u16() # read the raw value
            batt = batt / 65535   # convert to fraction of 1
            batt = 2 * 3.3 * batt # multiply with analog reference and compensate for internal divider
            batt = batt - 3.00    # transform to percentage 3 volt = 0% 4.2 volt = 100 %
            batt = 100 * batt / 1.20
            batt = int(batt)      # transform to integer
            self.setBattery(batt)   



if __name__ == "__main__":
    
    bt = Bluetooth(uart_nr = 1)
    
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
          as_string = bt.line2string(line)
          if line:
              print("Regel:", as_string)

    #test_char()
    #test_line()
    
    async def task_bt_receive():
      while True:
        await asyncio.sleep_ms(200)
        line = bt.readline()
        # wacht totdat er een regel is ontvangen via bluetooth
        if line:
            as_string = bt.line2string(line)
            print("Regel:", as_string)


    # definieer de taken die we willen gaan uitvoeren
    print("Test de coroutine wait4line")
    asyncio.create_task(task_bt_receive())
    asyncio.run(bt.task())


 
                                