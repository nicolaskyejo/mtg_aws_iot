#!/usr/bin/env python3
"""A simple script that takes pictures of 'Magic the Gathering' game cards with picamera
and sends them to AWS Textract service. The returned result is parsed for the name of the card.
Then an API request to scryfall.com is made to find the card price.
Eventually the result of all cards is saved to a text file and sent via email"""


__author__ = 'Nicolas Kyejo, Riya Kaynat'
__license__ = 'GPLv3'


import boto3
import RPi.GPIO as gpio
import io
import datetime
import time
import csv
import json
import webbrowser
import email_attachment_send # our script for sending email
from PIL import Image
from picamera import PiCamera


bcm_pin_number = 6
path = '/home/pi/Desktop/mtg_aws_iot/project/card_images/'
#img = path + '1.png' # for testing

def grayscale(input):
    """Converts image to grayscale and returns a byte array"""
    color_im = Image.open(input)
    bw = color_im.convert('L')
    imgByte_array = io.BytesIO()
    bw.save(imgByte_array, format='JPEG') # FORMAT
    return imgByte_array.getvalue()
    
def blink_when_sending_image():
    """Blinks the LED once when an image has been sent to AWS"""
    pass


def on_push_down(channel):
    """On pressing the switch down a picture will be taken
    Returns the file path for the picture taken"""
    filename = datetime.datetime.now().isoformat()[:10] + '.jpeg'
    filepath = path + filename
    camera.capture(filepath)
    return filepath
    
    
def parser_and_saver(response):
    """Parses the response and saves the result"""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            print(item["Text"])
            print(f'{item["Confidence"]:.2f}')
            if item['Confidence'] < 50: break # if confidence is less than 50% don't continue
            try:
                set_code, price, img_url = scryfall_request(item["Text"])
            except TypeError:
                break 

            with open('cards_detected.txt', 'a+') as f:
                f.write(item['Text'] + ' ' + set_code + '\n')
            with open('cards.csv', 'a+') as f:
                fieldnames = ['card_name', 'set', 'price (Euro)']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                # writer.writeheader()
                writer.writerow({'card_name': item['Text'], 'set': set_code,'price (Euro)': price})
            break    
        

def scryfall_request(card_name):
    """Makes a request to scryfall.com and returns set code, price, and car image url"""
    url = 'https://api.scryfall.com/cards/named?'
    parameters = {'fuzzy': card_name, 'format': 'json'}

    r = requests.get(url=url, params=parameters)
    if r.status_code == 404:
        print(f'Could not find a card with the name {card_name}')
        return
    else:    
        content = r.json()
        price = content['prices']['eur']
        card_image = content['image_uris']['normal']
        set_code = content['set']
        print(price)
        print(card_image)
        print(set_code)
        webbrowser.open(card_image)
        return set_code, price, card_image


if __name__ == '__main__':
    textract = boto3.client(
             service_name='textract',
             region_name= 'eu-west-1',
             endpoint_url='https://textract.eu-west-1.amazonaws.com',
    )

    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)
    gpio.setup(bcm_pin_number, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (800, 600)
    camera.start_preview()
        
    while True:
        try:
            gpio.add_event_detect(bcm_pin_number, gpio.RISING)
            gpio.add_event_callback(bcm_pin_number, callback=on_push_down) # some way of getting the filepath variable
            response = textract.detect_document_text(Document={'Bytes': grayscale(img)})
            parser_and_saver(response)
            time.sleep(1)
            print('Ready for next image...')
        except KeyboardInterrupt:
            camera.stop_preview()
            print('Sending mail & cleaning up...')
            email_attachment_send.send_mail()
            gpio.cleanup()
                
            
    


