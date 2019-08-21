#from gpiozero import *
from picamera import *
from time import *
from guizero import *

def take_picture():
    camera.capture(strftime("/home/pi/Desktop/mtg_aws_iot/project/image-%d-%m %H:%M:%S.png", gmtime()))

#take_pic_btn = Button(25)
#take_pic_btn.when_pressed = take_picture

camera = PiCamera()
camera.resolution = (1920, 600)
camera.rotation = 180
camera.contrast = 20


app = App("Picture taker", width=320, height=240)
app.tk.attributes("-fullscreen", True)
camera.start_preview(alpha=255)
message = Text(app, "Take Pictures")
new_pic = PushButton(app, take_picture, text="Snap")
app.display()

