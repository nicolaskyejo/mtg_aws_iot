#!/usr/bin/env python3
"""A script for sending email with an attachment using gmail. The variables 'sender, receiver, passw' are read from a text file"""


import email.encoders
import smtplib
import email
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText


secretfile = '/home/pi/secrets.txt'
filename = "cards_detected.txt"

if __name__ == '__main__':
    with open(secretfile, 'r') as f: 
        sender = f.readline().strip()
        receiver = f.readline().strip()
        passw = f.readline().strip()

    msg = MIMEMultipart()
    msg["Subject"] = datetime.now().strftime("%A %B %d %Y @ %H:%M:%S")
    msg["From"] = sender
    msg["To"] = receiver
    text = MIMEText("Updated Deck List")
    msg.attach(text)

    with open(filename, 'r') as f:
        attachment = MIMEText(f.read())
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)           
        msg.attach(attachment)

    # access Gmail account and send email
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(sender,passw)
    server.sendmail(sender,receiver, msg.as_string())
    server.quit()

