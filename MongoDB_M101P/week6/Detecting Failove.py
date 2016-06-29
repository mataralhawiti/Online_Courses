import pymongo
import os
import time

connection = pymongo.MongoClient(host=["mongodb://localhost:27017",
									   "mongodb://localhost:27018",
									   "mongodb://localhost:27019"], replicaSet="m101", w=1, j=True)

db = connection.mythings
things = db.things


things.delete_many({}) # remove all docs from collection


for i in range (0, 500) :
	try :
		things.insert_one({'_id':i})
		print("inserted document, doc : "+str(i))
		time.sleep(.1)
	except Exception as e :
		print("Exception", type(e), e)

# rs.stepDown() in mongo shell to simulate the failover during write

