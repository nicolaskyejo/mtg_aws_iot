#!/usr/bin/env python3
"""A simple script that takes pictures of 'Magic the Gathering' game cardswith picamera and sends them to AWS Textract service.
The returned result is parsed and the name of the card is returned
Eventually the result of all cards is saved to a text file and (optionally sent via sms or email)"""

__author__ = 'Nicolas Kyejo, Riya Kaynat'
__license__ = 'GPLv3'


import boto3
import RPi.GPIO as gpio
import io
import datetime
from time import sleep
from PIL import Image
from picamera import PiCamera


bcm_pin_number = 6
img = 'jaya_betterquality.jpg' # for testing
path = '/home/pi/Desktop/mtg_aws_iot/project/card_images/'


def grayscale(input):
    """Converts image to grayscale and returns a byte array"""
    color_im = Image.open(input)
    bw = color_im.convert('L')
    #bw.save(output)
    #with open(documentName, 'rb') as document:
        # imageBytes = bytearray(document.read())
    imgByte_array = io.BytesIO()
    bw.save(imgByte_array, format='JPEG')
    return imgByte_array.getvalue()
    
def blink_when_sending_image():
	"""Blinks the LED once when an image has been sent to AWS"""
	pass


def on_push_down(channel):
    """On pressing the switch down it will do the following"""
    print('Button pushed') # for testing
    filename = datetime.datetime.now().isoformat()[:10] + '.jpeg'
    camera.capture(path + filename)
    
    
def parser_and_saver(response):
    """Parses the response and saves the result"""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            print(item["Text"])
            print(item['Confidence'])
            with open('cards_detected.txt', 'a+') as f:
                f.write(item['Text'] + '\n')
            break    
        
    
if __name__ == '__main__':
    textract = boto3.client(
             service_name='textract',
             region_name= 'eu-west-1',
             endpoint_url='https://textract.eu-west-1.amazonaws.com',
    )

    # gpio.setmode(gpio.BCM)
    # gpio.setup(bcm_pin_number, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    # gpio.add_event_detect(bcm_pin_number, gpio.RISING)
    # gpio.add_event_callback(bcm_pin_number, callback=on_push_down)
    
    # camera = PiCamera()
    # camera.rotation = 180
    # camera.resolution = (1920, 1080)
    # camera.start_preview()
    
    
    # while True:
        # try:
            # print('Ready for next image...')
        # except KeyboardInterrupt:
            # camera.stop_preview()
            # print('Exiting...')
            # gpio.cleanup()
                
            
    response = textract.detect_document_text(Document={'Bytes': grayscale(img)})
    parser_and_saver(response)


