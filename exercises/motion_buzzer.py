#!/usr/bin/env python3
"""
Copied from
#Author        :alan
#Website       :www.osoyoo.com
"""


import RPi.GPIO as gpio
import time


# set BCM_gpio 17(gpio 0) as PIR pin
PIRPin = 17
# set BCM_gpio 18(gpio 1) as buzzer pin
BuzzerPin = 18


def setup():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    #set BuzzerPin's mode to output,and initial level to HIGH(3.3V)
    gpio.setup(BuzzerPin, gpio.OUT, initial=gpio.HIGH)
    gpio.setup(PIRPin, gpio.IN)


def main():
    print_message()
    while True:
        #read Sw520dPin's level
        if gpio.input(PIRPin) != 0:
            gpio.output(BuzzerPin, gpio.LOW)
            print ('********************')
            print ('*     alarm!     *')
            print ('********************')
            print ('\n')
	    time.sleep(1)
        else:
            gpio.output(BuzzerPin, gpio.HIGH)
            print ('====================')
            print ('=     Not alarm...  =')
            print ('====================')
            print ('\n')
	    time.sleep(1)
            

def destroy():
    """destroy function for clean up everything after the script finished"""
    gpio.output(BuzzerPin, gpio.HIGH) #turn off buzzer
    gpio.cleanup()

if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:
        destroy()
        
