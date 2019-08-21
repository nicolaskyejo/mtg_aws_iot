#!/usr/bin/env python3


import boto3
import pprint


# Document
documentName = "angrath.jpg"

# Read document content
with open(documentName, 'rb') as document:
    imageBytes = bytearray(document.read())

# Amazon Textract client
textract = boto3.client(
         service_name='textract',
         region_name= 'eu-west-1',
         endpoint_url='https://textract.eu-west-1.amazonaws.com'
)

# Call Amazon Textract
response = textract.detect_document_text(Document={'Bytes': imageBytes})

# pprint.pprint(response)

# Print detected text
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        print (item["Text"])
