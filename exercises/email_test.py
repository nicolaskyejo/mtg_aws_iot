from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import email.encoders
import smtplib
import os
import email
import sys
import time



    # prepare the email
f_time = datetime.now().strftime("%A %B %d %Y @ %H:%M:%S")
msg = MIMEMultipart()
msg["Subject"] = f_time
msg["From"] = "guykool47@gmail.com"
msg["To"] = "kaynat.riya@gmail.com"
text = MIMEText("Test mail")
msg.attach(text)


filename = "cards_detected.txt"
with open(filename, 'r') as f:
    attachment = MIMEText(f.read())
    attachment.add_header('Content-Disposition', 'attachment', filename=filename)           
    msg.attach(attachment)

# access Gmail account and send email
server = smtplib.SMTP("smtp.gmail.com:587")
server.starttls()
server.login("guykool47@gmail.com","")
server.sendmail("guykool47@gmail.com","kaynat.riya@gmail.com", msg.as_string())
server.quit()

