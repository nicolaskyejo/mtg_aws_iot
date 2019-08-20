#!/usr/bin/env python3


import RPi.GPIO as gpio
import time


count = 10
led_pin = 17


gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(led_pin, gpio.OUT)
for i in range(count):
    print('LED ON! ')
    gpio.output(led_pin, gpio.HIGH)
    time.sleep(1)
    print('LED OFF! ')
    gpio.output(led_pin, gpio.LOW)
    time.sleep(1)

gpio.cleanup()
