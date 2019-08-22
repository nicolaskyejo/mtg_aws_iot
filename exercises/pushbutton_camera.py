#!/usr/bin/env python3


import RPi.GPIO as gpio
import datetime
from time import sleep
from picamera import PiCamera


bcm_pin_number = 6
path = '/home/pi/Desktop/mtg_aws_iot/project/card_images/'

def on_push_down():
    filename = datetime.datetime.now().isoformat()[:10] + '.jpeg'
    filepath = path + filename
    camera.capture(filepath)
    camera.stop_preview()
    return filepath


camera = PiCamera()
camera.rotation = 180
camera.resolution = (800, 600)
camera.start_preview()

gpio.setmode(gpio.BCM)
gpio.setup(bcm_pin_number, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.add_event_detect(bcm_pin_number, gpio.RISING, bouncetime=1000)
gpio.wait_for_edge(bcm_pin_number, gpio.FALLING)
if gpio.event_detected(bcm_pin_number):
    #filepath = gpio.add_event_callback(bcm_pin_number, callback=on_push_down)
    filepath = on_push_down()
    print(filepath)
gpio.cleanup()

