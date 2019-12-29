import boto3
import configparser
import os
import json
config = configparser.ConfigParser()
config.read('dl.cfg')


aws_key = os.environ['AWS_ACCESS_KEY_ID']=config.get('CREDENTIALS','AWS_ACCESS_KEY_ID')
aws_secret = os.environ['AWS_SECRET_ACCESS_KEY']=config.get('CREDENTIALS','AWS_SECRET_ACCESS_KEY')


# client = boto3.client(
#     's3',
#     # Hard coded strings as credentials, not recommended.
#     aws_access_key_id=aws_key,
#     aws_secret_access_key=aws_secret
# )

# client.upload_file(Bucket='dend-capstone', Filename='raw_data/I94addr.json')

# json.load(s3.Object('dend-capstone', 'raw_data/I94addr.json').get()['Body'])
    
def upload_to_s3():
    
#     client = boto3.client('s3')
#     s3 = boto3.resource('s3')
#     client.upload_file(Bucket="dend-capstone", Key='us_ports/us_ports.json', Filename=json.load(s3.Object('dend-capstone', 'raw_data/I94addr.json').get()['Body']))
    
    lookup_files = ['raw_data/I94addr.json', 'raw_data/airlines_iata_codes.json', 'raw_data/I94port.json', 'raw_data/I94res.json']
    files_mapping = {
        'raw_data/I94addr.json' : 'us_states/us_states.json',
        'raw_data/airlines_iata_codes.json' : 'airlines_iata/airlines_iata.json',
        'raw_data/I94port.json' : 'us_ports/us_ports.json',
        'raw_data/I94res.json' : 'countries/countries.json'
    }
    #copy_source = {'Bucket': 'dend-capstone', 'Key': 'raw_data/I94addr.json'}
    s3 = boto3.client('s3')
    
    for file in lookup_files:
        print(file)
        print(files_mapping.get(file, ""))
        copy_source = {'Bucket': 'dend-capstone', 'Key': file}
        s3.copy_object(CopySource=copy_source, Bucket='dend-capstone', Key=files_mapping.get(file, ""))


def list_s3():
    s3 = boto3.client('s3')
    all_objects = s3.list_objects(Bucket = 'dend-capstone',Delimiter='/')
    
    obj_list = [ obj["Prefix"] for obj in all_objects.get("CommonPrefixes", "") ]
    
    for i in obj_list:
        print(i)
    
#     if len(obj_list) != 8:
#         raise ValueError(f"Data quality check failed. We got {len(obj_list)} objects in our S3 data lake, we expect 8")
#     else :
#         logging.info(f"Data quality on S3 data lake check passed with 8 objects")


list_s3()