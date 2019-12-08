# MTG AWS IoT
![project in action](in_action.png?raw=true)

A quick small project for detecting Magic the Gathering cards
using Amazon's [Textract](https://aws.amazon.com/textract/) service.

## Requirements
* Python 3.6+
* An Amazon account - AWS free tier is enough
* [AWS CLI](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) - for setting up auth credentials
* Raspberry pi  (tested on model 3B+)
* [Camera Module](https://www.raspberrypi.org/products/camera-module-v2/)
* A button switch - [example](https://www.adafruit.com/product/367)

### Steps
* Set up the Raspberry pi roughly as shown
![setup](humble_setup.jpg?raw=true)
use BCM pin numbers ([pinout](https://pinout.xyz/))
* If you plan to control the pi in headless mode (e.g. VNC server),
enable direct capture mode ([instructions](https://www.raspberrypi.org/forums/viewtopic.php?t=216356#p1330535))
* Install dependencies 
```
git clone https://github.com/nicolaskyejo/mtg_aws_iot.git
cd mtg_aws_iot/project
pip install -r requirements.txt
```
* Run mtg_card_recognition.py

### Possible Improvements
* Use [gpiozero](https://gpiozero.readthedocs.io/)
instead of RPi.GPIO for easier setup
* Use [asyncio](https://docs.python.org/3.6/library/asyncio.html)
for asynchronous features
* Use [sqlite](https://docs.python.org/3.6/library/sqlite3.html)
instead of a text file to save card information
* Use [opencv](https://opencv.org/) to detect card and take a picture automatically
instead of manually pushing the switch down

