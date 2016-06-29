import pymongo
import os
import time

connection = pymongo.MongoClient(host=["mongodb://localhost:27017",
									   "mongodb://localhost:27018",
									   "mongodb://localhost:27019"], replicaSet="m101", w=1, j=True)

db = connection.mythings
things = db.things




for i in range (0, 500) :
	for retry in range(3) :
		try :
			things.find_one({'_id':i})
			print("read document, doc : "+str(i))
			time.sleep(.1)
			break
		except pymongo.errors.AutoReconnect as e :
			print("Exception", type(e), e)
			print("retry")
			time.sleep(5)



# rs.stepDown() in mongo shell to simulate the failover during write

