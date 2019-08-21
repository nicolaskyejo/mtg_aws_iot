#!/usr/bin/env python3


from guizero import App, Text, PushButton, Picture
from picamera import PiCamera


def cap():
    #camera.start_preview()
    camera.capture('/home/pi/Desktop/mtg_aws_iot/exercises/captest.jpeg')
    camera.stop_preview()


# camera = PiCamera()
# camera.rotation = 180
# camera.resolution = (1920, 1080)
# camera.start_preview()

camera = PiCamera()
camera.rotation = 180
camera.resolution = (400, 400)
app = App('Camera capture', 800, 480)
# message = Text(app, "Picture taken")
camera.start_preview()
new_pic = PushButton(app, cap, text='New Picture')
app.display()
