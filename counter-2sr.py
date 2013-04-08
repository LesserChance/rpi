# This uses two shift registers to control the segments and digit
# Shift Register = Shift Register 8-Bit - 74HC595 
# 7 segment = COM-09481

import RPi.GPIO as gpio
from time import sleep, gmtime, strftime
from datetime import datetime

LED_ON = gpio.LOW
LED_OFF = gpio.HIGH

class Shifter():

    inputB     = 18
    clock      = 23
    clearPin   = 24
    disablePin = 22

    char_map   = {
        " ":[0,0,0,0,0,0,0,0],
        "1":[0,1,1,0,0,0,0,0],
        "2":[1,1,0,1,1,0,1,0],
        "3":[1,1,1,1,0,0,1,0],
        "4":[0,1,1,0,0,1,1,0],
        "5":[1,0,1,1,0,1,1,0],
        "6":[1,0,1,1,1,1,1,0],
        "7":[1,1,1,0,0,0,0,0],
        "8":[1,1,1,1,1,1,1,0],
        "9":[1,1,1,0,0,1,1,0],
        "0":[1,1,1,1,1,1,0,0]
    }

    def __init__(self):
        self.setupBoard()

    def enable(self):
        gpio.output(Shifter.disablePin, gpio.LOW)

    def disable(self):
        gpio.output(Shifter.disablePin, gpio.HIGH)
    
    def tick(self):
        gpio.output(Shifter.clock,gpio.HIGH)
        gpio.output(Shifter.clock,gpio.LOW)

    def digitOn(self, digit, colon):
        if digit == 1:
            self.output([0,1,1,1,colon,0,0,0])
        elif digit == 2:
            self.output([1,0,1,1,colon,0,0,0])
        elif digit == 3:
            self.output([1,1,0,1,colon,0,0,0])
        elif digit == 4:
            self.output([1,1,1,0,colon,0,0,0])

    def setValue(self, digit, value, colon):
        #disable output while shifting
        Shifter.disable(self)
        
        #value
        Shifter.output(self, Shifter.char_map[value]);
        
        #digit
        Shifter.digitOn(self, digit, colon)        
       
        #trigger RCLK
        Shifter.tick(self)
        Shifter.enable(self)
        sleep(.0025)

    def output(self,value):
        for v in reversed(value):
            if (v):
                gpio.output(Shifter.inputB, LED_ON)
            else:
                gpio.output(Shifter.inputB, LED_OFF)
            
            Shifter.tick(self);

    def setString(self, string, colon):
        Shifter.setValue(self, 1, string[0], colon)
        Shifter.setValue(self, 2, string[1], colon)
        Shifter.setValue(self, 3, string[2], colon)
        Shifter.setValue(self, 4, string[3], colon)

    def clear(self):
        gpio.output(Shifter.clearPin, gpio.LOW)
        gpio.output(Shifter.clearPin, gpio.HIGH)

    def setupBoard(self):
        gpio.setup(Shifter.disablePin, gpio.OUT)
        gpio.output(Shifter.disablePin, gpio.LOW)

        gpio.setup(Shifter.inputB, gpio.OUT)
        gpio.output(Shifter.inputB, gpio.LOW)

        gpio.setup(Shifter.clock, gpio.OUT)
        gpio.output(Shifter.clock, gpio.LOW)

        gpio.setup(Shifter.clearPin, gpio.OUT)
        gpio.output(Shifter.clearPin, gpio.HIGH)

def main():
    gpio.setmode(gpio.BCM)
    shifter=Shifter()
    running=True

    shifter.disable()

    while running==True:
        try:
            now=datetime.now()
            if (now.microsecond < 500000):
                shifter.setString(strftime("%M%S", gmtime()), 1)
            else:
                shifter.setString(strftime("%M%S", gmtime()), 0)

        except KeyboardInterrupt:
            running=False

if __name__=="__main__":
    main()

