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

    def line2string(self, buffer):
        """ Change byte buffer into a string"""    
        if buffer:
            line = ""
            try:
                # vertaal de nummers in de buffer naar karakters
                line = buffer.decode('utf-8')
            except:
                line ="data: "
                for c in buffer:
                    line = "%s - %2x"%(line,c)
                line ="%s\n"%line
            return line
                

    def getCharacter(self):
        buffer =  self.uart.read(1)
        # vertaal de nummers in de buffer naar karakters
        result = "."
        try:
            result = buffer.decode('utf-8')
        except:
            pass
        return result

    def getByte(self):
        # haal het karakter op uit de uart buffer
        buffer =  self.uart.read(1)
        return buffer[0]



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
    test_line()
    




 
                                