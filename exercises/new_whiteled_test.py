#!/usr/bin/env python3


import RPi.GPIO as gpio
import time


led_pin_1 = 17
led_pin_2 = 4


gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(led_pin_1, gpio.OUT)
gpio.setup(led_pin_2, gpio.OUT)
for i in range(2):
    #print('LED ON! ')
    gpio.output(led_pin_1, gpio.HIGH)
    time.sleep(3)
    gpio.output(led_pin_1, gpio.LOW)
    time.sleep(3)
    gpio.output(led_pin_2, gpio.HIGH)
    time.sleep(3)
    gpio.output(led_pin_2, gpio.LOW)
    #print('LED OFF! ')
    
    time.sleep(1)

gpio.cleanup()
