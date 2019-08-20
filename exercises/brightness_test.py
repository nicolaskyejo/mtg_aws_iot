#!/usr/bin/env python3


from picamera import PiCamera
from time import sleep


camera = PiCamera()
camera.rotation = 180
camera.resolution = (800, 600)
camera.framerate = 15
camera.start_preview()

for i in range(100):
    camera.brightness = i
    sleep(0.5)
camera.stop_preview()
