from gpiozero import *
from picamera import *
from time import *
from guizero import *

def take_picture():
    global output
    output = strftime("/home/pi/Desktop/image-%d-%m %H:%M:%S.png", gmtime())
    for i in range(3):
        sleep(1)
        camera.capture(output)

take_pic_btn = Button(25)
take_pic_btn.when_pressed = take_picture

camera = PiCamera()
camera.resolution = (1920, 800)

output = ""

app = App("My Pi Booth", width=320, height=240)
app.tk.attributes("-fullscreen", True)
camera.start_preview(alpha=255)
message = Text(app, "Text above button")
new_pic = PushButton(app, take_picture, text="Text on button")
app.display()
