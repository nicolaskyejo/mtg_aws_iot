#!/usr/bin/env python3


import RPi.GPIO as gpio
from time import sleep


bcm_pin_number = 6


def on_push_down(channel):
	print('Button pushed') # callback 1


gpio.setmode(gpio.BCM)
gpio.setup(bcm_pin_number, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.add_event_detect(bcm_pin_number, gpio.RISING)
gpio.add_event_callback(bcm_pin_number, callback=on_push_down)
sleep(10)
gpio.cleanup()