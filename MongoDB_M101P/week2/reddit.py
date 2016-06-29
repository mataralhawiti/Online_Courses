import sys
import pymongo
import requests
#import json


# connect to mongod
connection = pymongo.MongoClient("mongodb://localhost")

# get handle to reddit db
db = connection.reddit

# create new collection
tech1 = db.tech1

# request json doc from reddit
request = requests.get("https://www.reddit.com/r/technology/.json")
response = request.json()

'''
with open("/home/matar/mdbclass/reddit1.json") as js :
	js_data = json.load(js)
	#print(js_data)


for item in js_data['data']['children'] :
	tech.insert_one(item['data'])
'''	

for item in response['data']['children'] :
	tech1.insert_one(item['data'])