# This uses one shift register to control the segments, and gpio pins to select the digit
# Shift Register = Shift Register 8-Bit - 74HC595 
# 7 segment = COM-09481

import RPi.GPIO as gpio
from time import sleep, gmtime, strftime

LED_ON = gpio.LOW
LED_OFF = gpio.HIGH

class Shifter():

    inputB     = 18
    clock      = 23
    clearPin   = 24
    disablePin = 22

    digit1     = 17
    digit2     = 14 #txd 
    digit3     = 25
    digit4     = 4
    colon      = 15 #rxd

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

    def digitOn(self, digit):
        if digit == 1:
            gpio.output(Shifter.digit1, gpio.HIGH)
        elif digit == 2:
            gpio.output(Shifter.digit2, gpio.HIGH)
        elif digit == 3:
            gpio.output(Shifter.digit3, gpio.HIGH)
        elif digit == 4:
            gpio.output(Shifter.digit4, gpio.HIGH)
        elif digit == "colon":
            gpio.output(Shifter.colon, gpio.HIGH)

    def digitOff(self, digit):
        if digit == 1:
            gpio.output(Shifter.digit1, gpio.LOW)
        elif digit == 2:
            gpio.output(Shifter.digit2, gpio.LOW)
        elif digit == 3:
            gpio.output(Shifter.digit3, gpio.LOW)
        elif digit == 4:
            gpio.output(Shifter.digit4, gpio.LOW)
        elif digit == "colon":
            gpio.output(Shifter.colon, gpio.LOW)
    
    def setNumber(self, digit, number):
        Shifter.digitOn(self, digit)
        Shifter.setValue(self, Shifter.char_map[number])
        sleep(.0025)
        Shifter.setValue(self, Shifter.char_map[" "])
        Shifter.digitOff(self, digit)

    def setValue(self,value):
        #disable output while shifting
        Shifter.disable(self)
        for v in reversed(value):
            if (v):
                gpio.output(Shifter.inputB, LED_ON)
            else:
                gpio.output(Shifter.inputB, LED_OFF)
            
            Shifter.tick(self);
       
        #trigger RCLK
        Shifter.tick(self)
        Shifter.enable(self)

    def setString(self, string, colon):
        Shifter.setNumber(self, 1, string[0])
        Shifter.setNumber(self, 2, string[1])
        Shifter.setNumber(self, 3, string[2])
        Shifter.setNumber(self, 4, string[3])
        if (colon):
            Shifter.digitOn(self, "colon")
        else:
            Shifter.digitOff(self, "colon")

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

        gpio.setup(Shifter.digit1, gpio.OUT)
        gpio.output(Shifter.digit1, gpio.LOW)

        gpio.setup(Shifter.digit2, gpio.OUT)
        gpio.output(Shifter.digit2, gpio.LOW)

        gpio.setup(Shifter.digit3, gpio.OUT)
        gpio.output(Shifter.digit3, gpio.LOW)

        gpio.setup(Shifter.digit4, gpio.OUT)
        gpio.output(Shifter.digit4, gpio.LOW)

        gpio.setup(Shifter.colon, gpio.OUT)
        gpio.output(Shifter.colon, gpio.LOW)

def main():
    gpio.setmode(gpio.BCM)
    shifter=Shifter()
    running=True

    shifter.disable()

    while running==True:
        try:
            shifter.setString(strftime("%M%S", gmtime()), True)
        except KeyboardInterrupt:
            running=False
            shifter.setValue([0,0,0,0,0,0,0,0])

if __name__=="__main__":
    main()

