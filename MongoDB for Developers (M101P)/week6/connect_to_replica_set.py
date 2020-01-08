import pymongo
import os

#connection = pymongo.MongoClient()
'seeds list'
connection = pymongo.MongoClient(host=["mongodb://localhost:27017",
									   "mongodb://localhost:27018",
									   "mongodb://localhost:27019"], replicaSet="m101", w=1, j=True)

db = connection.test
people = db.people

try:
	print ("inserting")
	people.insert_one({"name":"Andrew Erlichson", "favorite_color":"blue"})
	print ("inserting")
	people.insert_one({"name":"Richard Krueter", "favorite_color":"red"})
	print ("inserting")
	people.insert_one({"name":"Dwight Merriman", "favorite_color":"green"})
except Exception as e :
	print("unexpected error", type(e), e )

print("completed the inserts")       