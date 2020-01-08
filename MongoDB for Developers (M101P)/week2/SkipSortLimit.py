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
	query = {}

	try:
		cursor = stories.find(query).sort("created_utc", pymongo.DESCENDING).skip(3).limit(1)

		# we're using tuples !!
		# cursor = 	stories.find(query).sort([("created_utc", , pymongo.ASCENDING), ("ups", pymongo.DESCENDING)])

	except Exception as e:
		print("unexpected error", type(e), e)

	for doc in cursor :
		print(doc)

find()