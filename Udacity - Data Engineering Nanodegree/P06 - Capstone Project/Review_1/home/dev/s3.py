import boto3
import configparser
from datetime import datetime
import os
import json

config = configparser.ConfigParser()
config.read('dl.cfg')

# aws_key = os.environ['AWS_ACCESS_KEY_ID']=config.get('CREDENTIALS','AWS_ACCESS_KEY_ID')
# aws_secret = os.environ['AWS_SECRET_ACCESS_KEY']=config.get('CREDENTIALS','AWS_SECRET_ACCESS_KEY')

os.environ['AWS_ACCESS_KEY_ID']=config.get('CREDENTIALS','AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY']=config.get('CREDENTIALS','AWS_SECRET_ACCESS_KEY')


# client = boto3.client(
#     's3',
#     aws_access_key_id=aws_key,
#     aws_secret_access_key=aws_secret
# )


s3 = boto3.resource('s3')
bucket = s3.Bucket('dend-capstone')
