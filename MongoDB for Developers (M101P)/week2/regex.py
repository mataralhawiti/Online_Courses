import pymongo
import sys

# create connection to mongod
connection = pymongo.MongoClient("mongodb://localhost")


# get db handle
db = connection.reddit

# collection
stories = db.stories


def find() :
	# query >> dicct
	query = {"title" : {"$regex" : "policies", "$options":"i"}}
	projection = {"title":1, "_id":0}

	try:
		cursor = stories.find(query, projection)
	except Exception as e:
		print("unexpected error", type(e), e)

	for doc in cursor :
		print(doc)

find()