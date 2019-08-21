#!/usr/bin/env python3


import RPi.GPIO as gpio
from time import *
from picamera import PiCamera


bcm_pin_number = 6


def on_push_down(channel):
    camera.capture(strftime("/home/pi/Desktop/mtg_aws_iot/project/image-%d-%m %H:%M:%S.png", gmtime()))
    camera.stop_preview()
    gpio.cleanup()


camera = PiCamera()
camera.rotation = 180
camera.resolution = (800, 600)
camera.start_preview()

gpio.setmode(gpio.BCM)
gpio.setup(bcm_pin_number, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.add_event_detect(bcm_pin_number, gpio.RISING)
gpio.add_event_callback(bcm_pin_number, callback=on_push_down)
sleep(30)

