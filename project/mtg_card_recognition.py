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
import requests
import time
import csv
import json
import webbrowser
import sys
import email_attachment_send # our script for sending email
from PIL import Image
from picamera import PiCamera


button_switch_pin_number = 6
led_pin = 17
path = './card_images/'

def grayscale(input):
    """Converts image to grayscale and returns a byte array"""
    color_im = Image.open(input)
    bw = color_im.convert('L')
    imgByte_array = io.BytesIO()
    bw.save(imgByte_array, format='JPEG') # FORMAT
    return imgByte_array.getvalue()
    
def blink():
    """Blinks the LED once"""
    gpio.output(led_pin, gpio.HIGH)
    time.sleep(2)
    gpio.output(led_pin, gpio.LOW)


def on_push_down():
    """On pressing the switch down a picture will be taken
    Returns the file path for the picture taken"""
    filename = datetime.datetime.now().isoformat()[:-7].replace(':','-') + '.jpeg' # Make Linux/Windows compatible files
    filepath = path + filename
    camera.capture(filepath)
    return filepath
    
    
def parser_and_saver(response):
    """Parses the response and saves the result"""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            print(item["Text"]) # for debugging
            print(f'{item["Confidence"]:.2f}') # for debugging
            if item['Confidence'] < 50: break # if confidence is less than 50% don't continue
            try:
                set_code, price, img_url = scryfall_request(item["Text"])
                blink() # Blink LED when a valid card has been found
            except TypeError:
                break 

            with open('cards_detected.txt', 'a+') as f:
                f.write(f"{item['Text']} ({set_code})\n")
            with open('cards.csv', 'a+') as f:
                fieldnames = ['card_name', 'set', 'price (Euro)']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                # writer.writeheader()
                writer.writerow({'card_name': item['Text'], 'set': set_code,'price (Euro)': price})
            break    
        

def scryfall_request(card_name):
    """Makes a request to scryfall.com and returns set code, price, and card image url"""
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
        print(price) # for debugging
        print(card_image) # for debugging
        print(set_code) #f or debugging
        webbrowser.open(card_image) # open web browser to check if the card is the same
        return set_code, price, card_image

def graceful_quit():
    """Send email using an imported function and quit the program"""
    camera.stop_preview()
    print('Sending mail & cleaning up...')
    email_attachment_send.send_mail()
    gpio.cleanup()
    sys.exit()
    
    
if __name__ == '__main__':
    textract = boto3.client(
             service_name='textract',
             region_name= 'eu-west-1',
             endpoint_url='https://textract.eu-west-1.amazonaws.com',
    )

    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)
    gpio.setup(button_switch_pin_number, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    gpio.setup(led_pin, gpio.OUT)
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (800, 600)
    camera.start_preview()
            
    while True:
        try:
            gpio.add_event_detect(button_switch_pin_number, gpio.RISING, bouncetime=1000)
            gpio.wait_for_edge(button_switch_pin_number, gpio.FALLING) # wait for switch to be pressed
            if gpio.event_detected(button_switch_pin_number):
                filepath = on_push_down()
                response = textract.detect_document_text(Document={'Bytes': grayscale(filepath)}) # Make connection to AWS Textract and send image
                parser_and_saver(response)
                gpio.remove_event_detect(button_switch_pin_number)
                answer = input('Do you want to continue [Y/N]\n').lower()
                if answer == 'y': continue
                elif answer == 'n': graceful_quit()
                else:
                    print('Assuming answer is No')
                    graceful_quit()
        except KeyboardInterrupt:
            break
                
            
    


