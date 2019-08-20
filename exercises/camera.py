#!/usr/bin/env python3


from picamera import PiCamera, Color
from time import sleep


camera = PiCamera()
camera.rotation = 180
#camera.annotate_text = 'test annonate'
camera.resolution = (800, 600)
# camera.framerate = 15
camera.start_preview()
# camera.image_effect = 'colorswap
# camera.annotate_background = Color('blue')
# camera.awb_mode = 'sunlight'
sleep(7)
camera.capture('/home/pi/Desktop/mtg_aws_iot/exercises/jaya.jpg')
camera.stop_preview()