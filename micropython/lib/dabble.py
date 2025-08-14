# ---------------------------------#
# Learning Micropython             #
# Author: Anton Smeenk             #
# License: Creative Commons sy-sa  #
# ---------------------------------#

print("== Loading module dabble ...")

from machine import UART, Pin 
import time
import asyncio
import math
 
DABBLE_ID    = const(0x00)
GAMEPAD_ID   = const(0x01)
TERMINAL_ID  = const(0x02)
PINMONITOR_ID= const(0x03)
LEDCONTROL_ID= const(0x0A)
 
class Dabble:
    """ A simple class for receiving and sending charaters via a bluettooth module
    """
    def __init__(self, uart_nr= 0, led = 28):
        """ Creates a new bluetooth Object."""
        self.uart = UART(uart_nr, 115200)
        self.buffer = None
        self.pages = {}
        self.registerPage(0, self)
        if led:
            self.led =Pin(led, mode=Pin.OUT)
        else:
            self.led = None
    
    def registerPage(self, page_id, page):
        print("Register id:%s"%page_id)
        self.pages[page_id] = page
            
    def handlePage(self, subPage, function, data):
        # function for hanling page zero, the dabble page
        # print ("sub:%s func:%s data:%s"%(subPage, function,data))
        pass

    def parseBuffer(self, buffer):
        """ Assume only a multiple of full frames are received """
        for i in range(0,len(buffer)):
            if buffer[i] == 0xFF:
                if len(buffer) < i + 4:
                    print("Reject buffer, buffer to small")
                    return
                dataLen = buffer[i+4]    
                if len(buffer) < i + 4 + dataLen:
                    print("Reject buffer, buffer to small")
                    return
                pageId = buffer[i+1]
                subPage = buffer[i+2]
                function = buffer[i+3]
                data = buffer[i+5: i+5+dataLen]
                i = i + 5 + dataLen
                page = None
                try:
                    page = self.pages[pageId]
                except:
                    print("No page with id:%s registered"%pageId)
                try:
                    page.handlePage(subPage, function, data)
                except Exception as e:
                    print("Error handling page", e)
                    

    async def task(self) :
        while True:
            await asyncio.sleep_ms(10)
            if self.led:
                self.led.value(0)
            buffer = self.uart.read()
            if buffer:
                if self.led:
                    self.led.value(1)
                self.parseBuffer(buffer)
                

class Gamepad:
    def __init__(self, dabble):
        """ Creates a new bluetooth Object."""
        self.dabble = dabble
        dabble.registerPage(GAMEPAD_ID, self)
        self.buttons = 0
        self.speed = 0
        self.direction = 0
        self.angle = 0
        self.radius = 0
     
    def handlePage(self, subPage, function, data):
        self.buttons = data[0]
        speed = 0
        steer = 0
        if subPage == 1:
            if data[1] & 2 == 2:
                speed = -85
            elif data[1] & 1 == 1:
                speed = 85
            if data[1] & 4 == 4:
                steer = -85
            elif data[1] & 8 == 8:
                steer = 85
        elif subPage ==2 or subPage == 3:
            self.angle = data[1] >>3
            self.radius = data[1] & 0x7
            radius = 100 * (self.radius) / 8
            angle = math.pi * self.angle / 12
            steer = math.floor(radius * math.cos(angle))
            speed = math.floor(radius * math.sin(angle))
        self.speed = speed
        self.direction = steer
            
    def snelheid(self):
        return self.speed
        
    def richting(self):
        return self.direction
    def hoek(self):
        return self.angle
    def straal(self):
        return self.radius
    def buttonPressed(self):
        return self.buttons > 0
    def isStart(self):
        return self.buttons & 1 == 1
    def isSelect(self):
        return self.buttons & 2 == 2
    def isSquare(self):
        return self.buttons & 32 == 32
    def isTriangle(self):
        return self.buttons & 4 == 4
    def isCircle(self):
        return self.buttons & 8 == 8
    def isCross(self):
        return self.buttons & 16 == 16
   

if __name__ == "__main__":
    dabble = Dabble(1)


 
                                