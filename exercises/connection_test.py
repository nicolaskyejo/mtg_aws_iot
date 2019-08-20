#!/usr/bin/env python3


import boto3


session = boto3.Session(profile_name='default')
s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)
    #upload a new file
data = open('test.jpeg', 'rb')
s3.Bucket('kappahehe').put_object(Key='test.jpeg', Body=data)