import pymongo
import sys


# connect to mongod server on standard port
try :
	connection = pymongo.MongoClient("mongodb://localhost")
	print("new connection has been estbalished")

except Exception as e:
	print ("can't connect ! \n", type(e), "\n", "The exception : ",e)


# attach db
db = connection.m101

# which collection ?
collection = db.funnynumbers


magic = 0

try :
	iter = collection.find()
	print(type(iter))

	for item in iter :
		if((item['value']%3) == 0 ):
			magic = magic + item['value']

except Exception as m :
	print("error", type(m), m)


print("the answer is " + str(int(magic)))